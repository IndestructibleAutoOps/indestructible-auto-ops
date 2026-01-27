/**
 * 分類規則API路由
 */

import { Router, Request, Response } from 'express';
import { DatabaseService } from '../services/database.js';
import { ClassificationEngine } from '../services/classification.js';

const router = Router();
const db = DatabaseService.getInstance();
const classificationEngine = new ClassificationEngine();

/**
 * 獲取所有分類規則
 * GET /api/rules
 */
router.get('/', async (req: Request, res: Response) => {
  try {
    const rules = db.getClassificationRules();

    res.json({
      code: 200,
      message: '獲取成功',
      data: rules
    });
  } catch (error) {
    console.error('獲取分類規則失敗:', error);
    res.status(500).json({
      code: 500,
      message: '獲取分類規則失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 創建分類規則
 * POST /api/rules
 */
router.post('/', async (req: Request, res: Response) => {
  try {
    const { name, description, priority, enabled, conditions, actions } = req.body;

    if (!name || !conditions || !actions) {
      return res.status(400).json({
        code: 400,
        message: '缺少必要參數'
      });
    }

    const rule = db.addClassificationRule({
      name,
      description: description || '',
      priority: priority || 0,
      enabled: enabled !== false,
      conditions,
      actions,
      createdAt: Date.now(),
      updatedAt: Date.now()
    });

    // 更新分類引擎的規則
    const allRules = db.getEnabledRules();
    classificationEngine.setRules(allRules);

    res.json({
      code: 200,
      message: '創建成功',
      data: rule
    });
  } catch (error) {
    console.error('創建分類規則失敗:', error);
    res.status(500).json({
      code: 500,
      message: '創建分類規則失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 更新分類規則
 * PUT /api/rules/:id
 */
router.put('/:id', async (req: Request, res: Response) => {
  try {
    const { name, description, priority, enabled, conditions, actions } = req.body;

    const updates: any = {};
    if (name !== undefined) updates.name = name;
    if (description !== undefined) updates.description = description;
    if (priority !== undefined) updates.priority = priority;
    if (enabled !== undefined) updates.enabled = enabled;
    if (conditions !== undefined) updates.conditions = conditions;
    if (actions !== undefined) updates.actions = actions;

    const rule = db.updateClassificationRule(req.params.id, updates);

    if (!rule) {
      return res.status(404).json({
        code: 404,
        message: '規則不存在'
      });
    }

    // 更新分類引擎的規則
    const allRules = db.getEnabledRules();
    classificationEngine.setRules(allRules);

    res.json({
      code: 200,
      message: '更新成功',
      data: rule
    });
  } catch (error) {
    console.error('更新分類規則失敗:', error);
    res.status(500).json({
      code: 500,
      message: '更新分類規則失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 刪除分類規則
 * DELETE /api/rules/:id
 */
router.delete('/:id', async (req: Request, res: Response) => {
  try {
    const success = db.deleteClassificationRule(req.params.id);

    if (!success) {
      return res.status(404).json({
        code: 404,
        message: '規則不存在'
      });
    }

    // 更新分類引擎的規則
    const allRules = db.getEnabledRules();
    classificationEngine.setRules(allRules);

    res.json({
      code: 200,
      message: '刪除成功'
    });
  } catch (error) {
    console.error('刪除分類規則失敗:', error);
    res.status(500).json({
      code: 500,
      message: '刪除分類規則失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 測試分類規則
 * POST /api/rules/:id/test
 */
router.post('/:id/test', async (req: Request, res: Response) => {
  try {
    const { filename, mimeType, size } = req.body;

    if (!filename) {
      return res.status(400).json({
        code: 400,
        message: '缺少文件名稱'
      });
    }

    const rule = db.getClassificationRuleById(req.params.id);

    if (!rule) {
      return res.status(404).json({
        code: 404,
        message: '規則不存在'
      });
    }

    // 評估規則
    const engine = new ClassificationEngine([rule]);
    const category = engine.classifySmart(filename, mimeType, size);

    res.json({
      code: 200,
      message: '測試成功',
      data: {
        filename,
        mimeType,
        size,
        matchedCategory: category,
        targetDirectory: engine.getTargetDirectory(category)
      }
    });
  } catch (error) {
    console.error('測試分類規則失敗:', error);
    res.status(500).json({
      code: 500,
      message: '測試分類規則失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

/**
 * 切換規則啟用狀態
 * PATCH /api/rules/:id/toggle
 */
router.patch('/:id/toggle', async (req: Request, res: Response) => {
  try {
    const rule = db.getClassificationRuleById(req.params.id);

    if (!rule) {
      return res.status(404).json({
        code: 404,
        message: '規則不存在'
      });
    }

    const updated = db.updateClassificationRule(req.params.id, {
      enabled: !rule.enabled
    });

    // 更新分類引擎的規則
    const allRules = db.getEnabledRules();
    classificationEngine.setRules(allRules);

    res.json({
      code: 200,
      message: '狀態切換成功',
      data: updated
    });
  } catch (error) {
    console.error('切換規則狀態失敗:', error);
    res.status(500).json({
      code: 500,
      message: '切換規則狀態失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

export default router;
