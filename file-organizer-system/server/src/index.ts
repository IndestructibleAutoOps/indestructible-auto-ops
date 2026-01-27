/**
 * 文件整理系統 - 服務器入口
 */

import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import fs from 'fs/promises';

import filesRouter from './routes/files.js';
import rulesRouter from './routes/rules.js';
import tasksRouter from './routes/tasks.js';
import { DatabaseService } from './services/database.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3001;

// 初始化數據庫
const dbPath = path.resolve(process.cwd(), 'data', 'fileorganizer.db');
const dbDir = path.dirname(dbPath);
await fs.mkdir(dbDir, { recursive: true });
DatabaseService.getInstance(dbPath);

// 中間件
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 靜態文件服務
app.use('/uploads', express.static(path.resolve(process.cwd(), 'uploads')));

// API路由
app.use('/api/files', filesRouter);
app.use('/api/rules', rulesRouter);
app.use('/api/tasks', tasksRouter);

// 健康檢查
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// 統計接口
app.get('/api/statistics', (req, res) => {
  try {
    const db = DatabaseService.getInstance();
    const stats = db.getStatistics();

    res.json({
      code: 200,
      message: '獲取成功',
      data: stats
    });
  } catch (error) {
    console.error('獲取統計信息失敗:', error);
    res.status(500).json({
      code: 500,
      message: '獲取統計信息失敗',
      error: error instanceof Error ? error.message : '未知錯誤'
    });
  }
});

// 錯誤處理
app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Server Error:', err);
  res.status(500).json({
    code: 500,
    message: '服務器錯誤',
    error: err.message
  });
});

// 啟動服務器
app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   文件整理系統服務器已啟動                                   ║
║                                                            ║
║   本地地址: http://localhost:${PORT}                          ║
║   API地址:   http://localhost:${PORT}/api                    ║
║                                                            ║
║   可用端點:                                                 ║
║   - GET  /api/files           文件列表                      ║
║   - POST /api/files/upload    上傳文件                      ║
║   - GET  /api/rules           分類規則                      ║
║   - POST /api/tasks/organize  創建任務                      ║
║   - GET  /api/statistics      統計信息                      ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
  `);
});

// 優雅退出
process.on('SIGTERM', () => {
  console.log('收到 SIGTERM 信號，正在關閉服務器...');
  DatabaseService.resetInstance();
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('收到 SIGINT 信號，正在關閉服務器...');
  DatabaseService.resetInstance();
  process.exit(0);
});

export default app;
