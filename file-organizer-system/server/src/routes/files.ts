/**
 * 文件管理API路由
 */

import { Router, Request, Response } from 'express';
import multer from 'multer';
import path from 'path';
import { v4 as uuidv4 } from 'uuid';
import { DatabaseService } from '../services/database.js';
import { ClassificationEngine } from '../services/classification.js';

const router = Router();
const db = DatabaseService.getInstance();
const classificationEngine = new ClassificationEngine();

// 配置 multer 用於文件上傳
const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    const uploadDir = path.resolve(process.cwd(), 'uploads');
    try {
      await import('fs/promises').then(fs => fs.mkdir(uploadDir, { recursive: true }));
      cb(null, uploadDir);
    } catch (error) {
      cb(error as Error, uploadDir);
    }
  },
  filename: (req, file, cb) => {
    const uniqueName = `${uuidv4()}${path.extname(file.originalname)}`;
    cb(null, uniqueName);
  }
});

const upload = multer({
  storage,
  limits: {
    fileSize: 100 * 1024 * 1024, // 100MB
    files: 20
  }
});

/**
 * 獲取文件列表
 * GET /api/files
 */
router.get('/', async (req: Request, res: Response) => {
  try {
    const {
      page = '1',
      pageSize = '20',
      sortBy = 'modifiedAt',
      sortOrder = 'desc',
      category,
      status,
      search
    } = req.query;

    const filters = {
      category: category as any,
      status: status as string,
      search: search as string
    };

    const pagination = {
      page: parseInt(page as string),
      pageSize: parseInt(pageSize as string),
      sortBy: sortBy as string,
      sortOrder: sortOrder as 'asc' | 'desc'
    };

    const result = db.getFiles(filters, pagination);

    res.json({
      code: 200,
      message: '獲取成功',
      data: {
        files: result.files,
        total: result.total,
        page: pagination.page,
        pageSize: pagination.pageSize,
        totalPages: Math.ceil(result.total / pagination.pageSize)
      }
    });
  } catch (error) {
    console.error('獲取文件列表失敗:', error);
    res.status(500).json({
      code: 500,
      message: '獲取文件列表失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 獲取文件詳情
 * GET /api/files/:id
 */
router.get('/:id', async (req: Request, res: Response) => {
  try {
    const file = db.getFileById(req.params.id);

    if (!file) {
      return res.status(404).json({
        code: 404,
        message: '文件不存在'
      });
    }

    res.json({
      code: 200,
      message: '獲取成功',
      data: file
    });
  } catch (error) {
    console.error('獲取文件詳情失敗:', error);
    res.status(500).json({
      code: 500,
      message: '獲取文件詳情失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 上傳文件
 * POST /api/files/upload
 */
router.post('/upload', upload.array('files', 20), async (req: Request, res: Response) => {
  try {
    const files = req.files as Express.Multer.File[];
    const uploadedFiles: any[] = [];

    for (const file of files) {
      const extension = classificationEngine.extractExtension(file.originalname);
      const mimeType = file.mimetype;
      const category = classificationEngine.classifySmart(file.originalname, mimeType, file.size);

      const fileEntity = db.addFile({
        name: file.originalname,
        extension,
        path: file.path,
        relativePath: file.filename,
        size: file.size,
        mimeType,
        category,
        subcategory: '',
        tags: [],
        status: 'pending',
        starRating: 0,
        isEncrypted: false
      });

      uploadedFiles.push(fileEntity);
    }

    res.json({
      code: 200,
      message: '上傳成功',
      data: {
        files: uploadedFiles,
        count: uploadedFiles.length
      }
    });
  } catch (error) {
    console.error('上傳文件失敗:', error);
    res.status(500).json({
      code: 500,
      message: '上傳文件失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 更新文件資訊
 * PUT /api/files/:id
 */
router.put('/:id', async (req: Request, res: Response) => {
  try {
    const { name, category, subcategory, tags, customName, description, status, starRating } = req.body;

    const updates: any = {};
    if (name !== undefined) updates.name = name;
    if (category !== undefined) updates.category = category;
    if (subcategory !== undefined) updates.subcategory = subcategory;
    if (tags !== undefined) updates.tags = tags;
    if (customName !== undefined) updates.customName = customName;
    if (description !== undefined) updates.description = description;
    if (status !== undefined) updates.status = status;
    if (starRating !== undefined) updates.starRating = starRating;

    const file = db.updateFile(req.params.id, updates);

    if (!file) {
      return res.status(404).json({
        code: 404,
        message: '文件不存在'
      });
    }

    res.json({
      code: 200,
      message: '更新成功',
      data: file
    });
  } catch (error) {
    console.error('更新文件失敗:', error);
    res.status(500).json({
      code: 500,
      message: '更新文件失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 刪除文件
 * DELETE /api/files/:id
 */
router.delete('/:id', async (req: Request, res: Response) => {
  try {
    const file = db.getFileById(req.params.id);

    if (!file) {
      return res.status(404).json({
        code: 404,
        message: '文件不存在'
      });
    }

    // 刪除物理文件
    try {
      await import('fs/promises').then(fs => fs.unlink(file.path));
    } catch (error) {
      console.warn('刪除物理文件失敗:', file.path);
    }

    // 刪除數據庫記錄
    db.deleteFile(req.params.id);

    res.json({
      code: 200,
      message: '刪除成功'
    });
  } catch (error) {
    console.error('刪除文件失敗:', error);
    res.status(500).json({
      code: 500,
      message: '刪除文件失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 批量刪除文件
 * POST /api/files/batch-delete
 */
router.post('/batch-delete', async (req: Request, res: Response) => {
  try {
    const { ids } = req.body;

    if (!Array.isArray(ids) || ids.length === 0) {
      return res.status(400).json({
        code: 400,
        message: '無效的文件ID列表'
      });
    }

    const deleted: string[] = [];
    const failed: Array<{ id: string; error: string }> = [];

    for (const id of ids) {
      const file = db.getFileById(id);
      if (!file) {
        failed.push({ id, error: '文件不存在' });
        continue;
      }

      try {
        // 刪除物理文件
        try {
          await import('fs/promises').then(fs => fs.unlink(file.path));
        } catch (e) {
          console.warn('刪除物理文件失敗:', file.path);
        }

        db.deleteFile(id);
        deleted.push(id);
      } catch (error) {
        failed.push({ id, error: error instanceof Error ? error.message : '未知錯誤' });
      }
    }

    res.json({
      code: 200,
      message: '批量刪除完成',
      data: {
        deleted,
        failed,
        total: ids.length,
        successCount: deleted.length,
        failedCount: failed.length
      }
    });
  } catch (error) {
    console.error('批量刪除文件失敗:', error);
    res.status(500).json({
      code: 500,
      message: '批量刪除文件失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 批量更新文件分類
 * POST /api/files/batch-classify
 */
router.post('/batch-classify', async (req: Request, res: Response) => {
  try {
    const { ids, category } = req.body;

    if (!Array.isArray(ids) || ids.length === 0) {
      return res.status(400).json({
        code: 400,
        message: '無效的文件ID列表'
      });
    }

    if (!category) {
      return res.status(400).json({
        code: 400,
        message: '缺少分類參數'
      });
    }

    const updated: any[] = [];
    const failed: Array<{ id: string; error: string }> = [];

    for (const id of ids) {
      const file = db.updateFile(id, { category });
      if (file) {
        updated.push(file);
      } else {
        failed.push({ id, error: '文件不存在或更新失敗' });
      }
    }

    res.json({
      code: 200,
      message: '批量分類完成',
      data: {
        updated,
        failed,
        successCount: updated.length,
        failedCount: failed.length
      }
    });
  } catch (error) {
    console.error('批量分類失敗:', error);
    res.status(500).json({
      code: 500,
      message: '批量分類失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 分析文件
 * POST /api/files/analyze
 */
router.post('/analyze', async (req: Request, res: Response) => {
  try {
    const { path: filePath } = req.body;

    if (!filePath) {
      return res.status(400).json({
        code: 400,
        message: '缺少文件路徑'
      });
    }

    const analysis = {
      extension: classificationEngine.extractExtension(path.basename(filePath)),
      category: classificationEngine.classifySmart(path.basename(filePath)),
      isImage: classificationEngine.isImage(path.basename(filePath)),
      isDocument: classificationEngine.isDocument(path.basename(filePath)),
      isVideo: classificationEngine.isVideo(path.basename(filePath)),
      isAudio: classificationEngine.isAudio(path.basename(filePath)),
      isArchive: classificationEngine.isArchive(path.basename(filePath)),
      isCode: classificationEngine.isCode(path.basename(filePath))
    };

    res.json({
      code: 200,
      message: '分析成功',
      data: analysis
    });
  } catch (error) {
    console.error('分析文件失敗:', error);
    res.status(500).json({
      code: 500,
      message: '分析文件失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 獲取分類配置
 * GET /api/files/categories
 */
router.get('/meta/categories', async (req: Request, res: Response) => {
  try {
    const categories = classificationEngine.getCategories();

    res.json({
      code: 200,
      message: '獲取成功',
      data: categories
    });
  } catch (error) {
    console.error('獲取分類配置失敗:', error);
    res.status(500).json({
      code: 500,
      message: '獲取分類配置失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

export default router;
