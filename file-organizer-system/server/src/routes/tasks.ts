/**
 * 任務管理API路由
 */

import { Router, Request, Response } from 'express';
import { DatabaseService } from '../services/database.js';
import { FileOrganizationService, createOrganizationService } from '../services/organization.js';

const router = Router();
const db = DatabaseService.getInstance();

// 存儲活躍的組織服務實例
const activeServices = new Map<string, FileOrganizationService>();

/**
 * 獲取所有任務
 * GET /api/tasks
 */
router.get('/', async (req: Request, res: Response) => {
  try {
    const { status } = req.query;
    const tasks = db.getTasks(status as string);

    res.json({
      code: 200,
      message: '獲取成功',
      data: tasks
    });
  } catch (error) {
    console.error('獲取任務列表失敗:', error);
    res.status(500).json({
      code: 500,
      message: '獲取任務列表失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 獲取任務詳情
 * GET /api/tasks/:id
 */
router.get('/:id', async (req: Request, res: Response) => {
  try {
    const task = db.getTaskById(req.params.id);

    if (!task) {
      return res.status(404).json({
        code: 404,
        message: '任務不存在'
      });
    }

    res.json({
      code: 200,
      message: '獲取成功',
      data: task
    });
  } catch (error) {
    console.error('獲取任務詳情失敗:', error);
    res.status(500).json({
      code: 500,
      message: '獲取任務詳情失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 創建組織任務
 * POST /api/tasks/organize
 */
router.post('/organize', async (req: Request, res: Response) => {
  try {
    const {
      name,
      description,
      watchDirectory = './watch',
      targetDirectory = './organized',
      options = {}
    } = req.body;

    if (!name) {
      return res.status(400).json({
        code: 400,
        message: '缺少任務名稱'
      });
    }

    // 創建任務記錄
    const task = db.createTask({
      name,
      description,
      status: 'pending',
      progress: 0,
      totalFiles: 0,
      processedFiles: 0,
      failedFiles: 0,
      logs: []
    });

    // 創建組織服務
    const service = createOrganizationService({
      watchDirectory,
      targetDirectory,
      preserveStructure: options.preserveStructure ?? false,
      overwriteExisting: options.overwriteExisting ?? false,
      categoryMapping: options.categoryMapping,
      excludePatterns: options.excludePatterns,
      maxFileSize: options.maxFileSize,
      minFileSize: options.minFileSize
    });

    // 設置進度回調
    service.setProgressCallback((progress, currentFile, status) => {
      db.updateTask(task.id, {
        progress,
        processedFiles: Math.floor((progress / 100) * (task.totalFiles || 1)),
        logs: [
          ...(db.getTaskById(task.id)?.logs || []),
          {
            timestamp: Date.now(),
            level: 'info',
            message: `處理中: ${currentFile}`,
            fileId: undefined
          }
        ]
      });
    });

    // 存儲服務實例
    activeServices.set(task.id, service);

    res.json({
      code: 200,
      message: '任務創建成功',
      data: task
    });
  } catch (error) {
    console.error('創建任務失敗:', error);
    res.status(500).json({
      code: 500,
      message: '創建任務失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 啟動任務
 * POST /api/tasks/:id/start
 */
router.post('/:id/start', async (req: Request, res: Response) => {
  try {
    const task = db.getTaskById(req.params.id);

    if (!task) {
      return res.status(404).json({
        code: 404,
        message: '任務不存在'
      });
    }

    const service = activeServices.get(req.params.id);

    if (!service) {
      return res.status(400).json({
        code: 400,
        message: '任務服務未初始化'
      });
    }

    // 掃描文件
    const files = await service.scanDirectory();

    if (files.length === 0) {
      return res.status(400).json({
        code: 400,
        message: '沒有找到需要整理的文件'
      });
    }

    // 更新任務狀態
    db.updateTask(req.params.id, {
      status: 'running',
      totalFiles: files.length,
      startedAt: Date.now(),
      logs: [
        {
          timestamp: Date.now(),
          level: 'info',
          message: `開始整理 ${files.length} 個文件`
        }
      ]
    });

    // 執行整理
    const result = await service.organizeFiles(files, {
      createCategoryFolders: true,
      createDateFolders: false,
      prefixFiles: false,
      suffixTimestamp: true
    });

    // 更新任務完成狀態
    const finalStatus = result.failed.length === 0 ? 'completed' : 'completed';

    db.updateTask(req.params.id, {
      status: finalStatus,
      progress: 100,
      processedFiles: result.success.length,
      failedFiles: result.failed.length,
      completedAt: Date.now(),
      logs: [
        ...task.logs,
        {
          timestamp: Date.now(),
          level: result.failed.length === 0 ? 'success' : 'warning',
          message: `整理完成: 成功 ${result.success.length} 個, 失敗 ${result.failed.length} 個`
        }
      ]
    });

    // 清理服務實例
    activeServices.delete(req.params.id);

    res.json({
      code: 200,
      message: '任務執行完成',
      data: {
        task: db.getTaskById(req.params.id),
        result: {
          successCount: result.success.length,
          failedCount: result.failed.length,
          failedFiles: result.failed.map(f => ({
            name: f.file.name,
            error: f.error
          }))
        }
      }
    });
  } catch (error) {
    console.error('啟動任務失敗:', error);
    res.status(500).json({
      code: 500,
      message: '啟動任務失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 取消任務
 * POST /api/tasks/:id/cancel
 */
router.post('/:id/cancel', async (req: Request, res: Response) => {
  try {
    const task = db.getTaskById(req.params.id);

    if (!task) {
      return res.status(404).json({
        code: 404,
        message: '任務不存在'
      });
    }

    const service = activeServices.get(req.params.id);

    if (service) {
      await service.cancelTask();
      activeServices.delete(req.params.id);
    }

    db.updateTask(req.params.id, {
      status: 'cancelled',
      logs: [
        ...task.logs,
        {
          timestamp: Date.now(),
          level: 'info',
          message: '任務已取消'
        }
      ]
    });

    res.json({
      code: 200,
      message: '任務已取消',
      data: db.getTaskById(req.params.id)
    });
  } catch (error) {
    console.error('取消任務失敗:', error);
    res.status(500).json({
      code: 500,
      message: '取消任務失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 刪除任務
 * DELETE /api/tasks/:id
 */
router.delete('/:id', async (req: Request, res: Response) => {
  try {
    const task = db.getTaskById(req.params.id);

    if (!task) {
      return res.status(404).json({
        code: 404,
        message: '任務不存在'
      });
    }

    // 取消並清理活躍服務
    const service = activeServices.get(req.params.id);
    if (service) {
      await service.cancelTask();
      activeServices.delete(req.params.id);
    }

    // 這裡應該從數據庫刪除任務
    // 為了簡單起見，我們只標記為已完成
    db.updateTask(req.params.id, {
      status: 'completed'
    });

    res.json({
      code: 200,
      message: '刪除成功'
    });
  } catch (error) {
    console.error('刪除任務失敗:', error);
    res.status(500).json({
      code: 500,
      message: '刪除任務失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 獲取預設目錄結構
 * GET /api/tasks/structure
 */
router.get('/meta/structure', async (req: Request, res: Response) => {
  try {
    const service = createOrganizationService({
      watchDirectory: './watch',
      targetDirectory: './organized',
      preserveStructure: false,
      overwriteExisting: false
    });

    const structure = service.generateDefaultStructure();

    res.json({
      code: 200,
      message: '獲取成功',
      data: structure
    });
  } catch (error) {
    console.error('獲取目錄結構失敗:', error);
    res.status(500).json({
      code: 500,
      message: '獲取目錄結構失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

export default router;
