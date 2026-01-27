/**
 * 數據庫服務模組
 * 使用SQLite實現輕量級數據存儲
 */

import Database from 'better-sqlite3';
import path from 'path';
import { v4 as uuidv4 } from 'uuid';
import type { FileEntity, ClassificationRule, OrganizationTask, FileCategory } from '../types/index.js';

interface DbFile extends Omit<FileEntity, 'id' | 'createdAt' | 'modifiedAt' | 'accessedAt'> {
  id: string;
  created_at: number;
  modified_at: number;
  accessed_at: number;
  tags: string;
}

interface DbRule extends Omit<ClassificationRule, 'id' | 'createdAt' | 'updatedAt' | 'conditions' | 'actions'> {
  id: string;
  conditions: string;
  actions: string;
  created_at: number;
  updated_at: number;
}

interface DbTask extends Omit<OrganizationTask, 'id' | 'createdAt' | 'startedAt' | 'completedAt' | 'logs'> {
  id: string;
  created_at: number;
  started_at: number | null;
  completed_at: number | null;
  logs: string;
}

export class DatabaseService {
  private db: Database.Database;
  private static instance: DatabaseService | null = null;

  private constructor(dbPath: string) {
    this.db = new Database(dbPath);
    this.initializeTables();
    this.seedDefaultRules();
  }

  public static getInstance(dbPath?: string): DatabaseService {
    if (!DatabaseService.instance) {
      const defaultPath = path.resolve(process.cwd(), 'data', 'fileorganizer.db');
      DatabaseService.instance = new DatabaseService(dbPath || defaultPath);
    }
    return DatabaseService.instance;
  }

  public static resetInstance(): void {
    if (DatabaseService.instance) {
      DatabaseService.instance.close();
      DatabaseService.instance = null;
    }
  }

  private initializeTables(): void {
    const tables = [
      // 文件信息表
      `CREATE TABLE IF NOT EXISTS files (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        extension TEXT NOT NULL,
        path TEXT NOT NULL UNIQUE,
        relative_path TEXT NOT NULL,
        size INTEGER NOT NULL,
        mime_type TEXT NOT NULL,
        category TEXT NOT NULL,
        subcategory TEXT DEFAULT '',
        created_at INTEGER NOT NULL,
        modified_at INTEGER NOT NULL,
        accessed_at INTEGER NOT NULL,
        tags TEXT DEFAULT '[]',
        custom_name TEXT,
        description TEXT,
        status TEXT DEFAULT 'pending',
        star_rating INTEGER DEFAULT 0,
        is_encrypted INTEGER DEFAULT 0,
        hash TEXT
      )`,

      // 分類規則表
      `CREATE TABLE IF NOT EXISTS classification_rules (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        priority INTEGER DEFAULT 0,
        enabled INTEGER DEFAULT 1,
        conditions TEXT NOT NULL,
        actions TEXT NOT NULL,
        created_at INTEGER NOT NULL,
        updated_at INTEGER NOT NULL
      )`,

      // 組織任務表
      `CREATE TABLE IF NOT EXISTS organization_tasks (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'pending',
        progress REAL DEFAULT 0,
        total_files INTEGER DEFAULT 0,
        processed_files INTEGER DEFAULT 0,
        failed_files INTEGER DEFAULT 0,
        created_at INTEGER NOT NULL,
        started_at INTEGER,
        completed_at INTEGER,
        logs TEXT DEFAULT '[]'
      )`,

      // 系統配置表
      `CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        updated_at INTEGER NOT NULL
      )`,

      // 索引優化
      `CREATE INDEX IF NOT EXISTS idx_files_category ON files(category)`,
      `CREATE INDEX IF NOT EXISTS idx_files_status ON files(status)`,
      `CREATE INDEX IF NOT EXISTS idx_files_path ON files(relative_path)`,
      `CREATE INDEX IF NOT EXISTS idx_rules_priority ON classification_rules(priority DESC)`,
      `CREATE INDEX IF NOT EXISTS idx_tasks_status ON organization_tasks(status)`
    ];

    this.db.transaction(() => {
      for (const sql of tables) {
        this.db.prepare(sql).run();
      }
    })();
  }

  private seedDefaultRules(): void {
    const existingRules = this.db.prepare('SELECT COUNT(*) as count FROM classification_rules').get() as { count: number };
    if (existingRules.count > 0) return;

    const defaultRules: Array<Omit<DbRule, 'id' | 'created_at' | 'updated_at'>> = [
      {
        name: '圖片分類',
        description: '自動將圖片文件分類到圖片目錄',
        priority: 100,
        enabled: 1,
        conditions: JSON.stringify([{ type: 'extension', operator: 'equals', value: 'jpg', logic: 'OR' }]),
        actions: JSON.stringify([{ type: 'category', parameters: { category: 'image' } }])
      },
      {
        name: '文檔分類',
        description: '將文檔文件分類到文檔目錄',
        priority: 90,
        enabled: 1,
        conditions: JSON.stringify([{ type: 'extension', operator: 'matches', value: 'doc|pdf|txt|docx|xls|xlsx|ppt|pptx' }]),
        actions: JSON.stringify([{ type: 'category', parameters: { category: 'document' } }])
      },
      {
        name: '代碼分類',
        description: '將源代碼文件分類到代碼目錄',
        priority: 80,
        enabled: 1,
        conditions: JSON.stringify([{ type: 'extension', operator: 'matches', value: 'js|ts|py|java|cpp|c|go|rs|php|rb|swift' }]),
        actions: JSON.stringify([{ type: 'category', parameters: { category: 'code' } }])
      },
      {
        name: '媒體分類',
        description: '將音頻和視頻文件分類到媒體目錄',
        priority: 70,
        enabled: 1,
        conditions: JSON.stringify([{ type: 'extension', operator: 'matches', value: 'mp3|wav|flac|mp4|avi|mkv|mov|wmv' }]),
        actions: JSON.stringify([{ type: 'category', parameters: { category: 'video' } }])
      },
      {
        name: '壓縮包分類',
        description: '將壓縮文件分類到歸檔目錄',
        priority: 60,
        enabled: 1,
        conditions: JSON.stringify([{ type: 'extension', operator: 'matches', value: 'zip|rar|7z|tar|gz|bz2' }]),
        actions: JSON.stringify([{ type: 'category', parameters: { category: 'archive' } }])
      }
    ];

    const insert = this.db.prepare(`
      INSERT INTO classification_rules (id, name, description, priority, enabled, conditions, actions, created_at, updated_at)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    const now = Date.now();
    this.db.transaction(() => {
      for (const rule of defaultRules) {
        insert.run(uuidv4(), rule.name, rule.description, rule.priority, rule.enabled ? 1 : 0, rule.conditions, rule.actions, now, now);
      }
    })();
  }

  // 文件操作方法
  public addFile(file: Omit<FileEntity, 'id' | 'createdAt' | 'modifiedAt' | 'accessedAt'>): FileEntity {
    const id = uuidv4();
    const now = Date.now();

    const stmt = this.db.prepare(`
      INSERT INTO files (id, name, extension, path, relative_path, size, mime_type, category, subcategory, created_at, modified_at, accessed_at, tags, custom_name, description, status, star_rating, is_encrypted, hash)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    stmt.run(
      id, file.name, file.extension, file.path, file.relativePath, file.size,
      file.mimeType, file.category, file.subcategory || '', now, now, now,
      JSON.stringify(file.tags), file.customName, file.description,
      file.status, file.starRating, file.isEncrypted ? 1 : 0, file.hash
    );

    return this.getFileById(id)!;
  }

  public updateFile(id: string, updates: Partial<FileEntity>): FileEntity | null {
    const allowedFields = [
      'name', 'category', 'subcategory', 'tags', 'custom_name',
      'description', 'status', 'star_rating', 'hash'
    ];

    const setClause: string[] = [];
    const values: any[] = [];

    for (const [key, value] of Object.entries(updates)) {
      const snakeKey = key.replace(/([A-Z])/g, '_$1').toLowerCase();
      if (allowedFields.includes(snakeKey) || key === 'tags') {
        if (key === 'tags') {
          setClause.push('tags = ?');
          values.push(JSON.stringify(value));
        } else {
          setClause.push(`${snakeKey} = ?`);
          values.push(value);
        }
      }
    }

    if (setClause.length === 0) return this.getFileById(id);

    setClause.push('modified_at = ?');
    values.push(Date.now());
    values.push(id);

    const stmt = this.db.prepare(`UPDATE files SET ${setClause.join(', ')} WHERE id = ?`);
    stmt.run(...values);

    return this.getFileById(id);
  }

  public deleteFile(id: string): boolean {
    const stmt = this.db.prepare('DELETE FROM files WHERE id = ?');
    const result = stmt.run(id);
    return result.changes > 0;
  }

  public getFileById(id: string): FileEntity | null {
    const row = this.db.prepare('SELECT * FROM files WHERE id = ?').get(id) as DbFile | undefined;
    if (!row) return null;
    return this.mapDbFileToEntity(row);
  }

  public getFileByPath(path: string): FileEntity | null {
    const row = this.db.prepare('SELECT * FROM files WHERE path = ?').get(path) as DbFile | undefined;
    if (!row) return null;
    return this.mapDbFileToEntity(row);
  }

  public getFiles(filters?: {
    category?: FileCategory;
    status?: string;
    search?: string;
    tags?: string[];
  }, pagination?: { page: number; pageSize: number; sortBy?: string; sortOrder?: 'asc' | 'desc' }): { files: FileEntity[]; total: number } {
    let whereClause = '1=1';
    const params: any[] = [];

    if (filters?.category) {
      whereClause += ' AND category = ?';
      params.push(filters.category);
    }

    if (filters?.status) {
      whereClause += ' AND status = ?';
      params.push(filters.status);
    }

    if (filters?.search) {
      whereClause += ' AND (name LIKE ? OR custom_name LIKE ? OR description LIKE ?)';
      const searchPattern = `%${filters.search}%`;
      params.push(searchPattern, searchPattern, searchPattern);
    }

    if (filters?.tags && filters.tags.length > 0) {
      const tagConditions = filters.tags.map(() => 'tags LIKE ?').join(' AND ');
      whereClause += ` AND ${tagConditions}`;
      for (const tag of filters.tags) {
        params.push(`%"${tag}"%`);
      }
    }

    const countStmt = this.db.prepare(`SELECT COUNT(*) as total FROM files WHERE ${whereClause}`);
    const { total } = countStmt.get(...params) as { total: number };

    let orderClause = 'modified_at DESC';
    if (pagination?.sortBy) {
      const order = pagination.sortOrder === 'asc' ? 'ASC' : 'DESC';
      orderClause = `${pagination.sortBy} ${order}`;
    }

    const offset = ((pagination?.page || 1) - 1) * (pagination?.pageSize || 20);
    const limit = pagination?.pageSize || 20;

    const stmt = this.db.prepare(`
      SELECT * FROM files WHERE ${whereClause} ORDER BY ${orderClause} LIMIT ? OFFSET ?
    `);

    const rows = stmt.all(...params, limit, offset) as DbFile[];

    return {
      files: rows.map(row => this.mapDbFileToEntity(row)),
      total
    };
  }

  public getAllFiles(): FileEntity[] {
    const rows = this.db.prepare('SELECT * FROM files ORDER BY modified_at DESC').all() as DbFile[];
    return rows.map(row => this.mapDbFileToEntity(row));
  }

  private mapDbFileToEntity(row: DbFile): FileEntity {
    return {
      id: row.id,
      name: row.name,
      extension: row.extension,
      path: row.path,
      relativePath: row.relative_path,
      size: row.size,
      mimeType: row.mime_type,
      category: row.category as FileCategory,
      subcategory: row.subcategory,
      createdAt: row.created_at,
      modifiedAt: row.modified_at,
      accessedAt: row.accessed_at,
      tags: JSON.parse(row.tags || '[]'),
      customName: row.custom_name || undefined,
      description: row.description || undefined,
      status: row.status as any,
      starRating: row.star_rating,
      isEncrypted: row.is_encrypted === 1,
      hash: row.hash || undefined
    };
  }

  // 分類規則操作方法
  public getClassificationRules(): ClassificationRule[] {
    const rows = this.db.prepare(`
      SELECT * FROM classification_rules ORDER BY priority DESC, created_at DESC
    `).all() as DbRule[];

    return rows.map(row => this.mapDbRuleToEntity(row));
  }

  public getEnabledRules(): ClassificationRule[] {
    const rows = this.db.prepare(`
      SELECT * FROM classification_rules WHERE enabled = 1 ORDER BY priority DESC
    `).all() as DbRule[];

    return rows.map(row => this.mapDbRuleToEntity(row));
  }

  public addClassificationRule(rule: Omit<ClassificationRule, 'id' | 'createdAt' | 'updatedAt'>): ClassificationRule {
    const id = uuidv4();
    const now = Date.now();

    const stmt = this.db.prepare(`
      INSERT INTO classification_rules (id, name, description, priority, enabled, conditions, actions, created_at, updated_at)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    stmt.run(
      id, rule.name, rule.description, rule.priority, rule.enabled ? 1 : 0,
      JSON.stringify(rule.conditions), JSON.stringify(rule.actions), now, now
    );

    return this.getClassificationRuleById(id)!;
  }

  public updateClassificationRule(id: string, updates: Partial<ClassificationRule>): ClassificationRule | null {
    const stmt = this.db.prepare(`
      UPDATE classification_rules SET name = ?, description = ?, priority = ?, enabled = ?, conditions = ?, actions = ?, updated_at = ? WHERE id = ?
    `);

    const now = Date.now();
    stmt.run(
      updates.name, updates.description, updates.priority, updates.enabled ? 1 : 0,
      JSON.stringify(updates.conditions), JSON.stringify(updates.actions), now, id
    );

    return this.getClassificationRuleById(id);
  }

  public deleteClassificationRule(id: string): boolean {
    const stmt = this.db.prepare('DELETE FROM classification_rules WHERE id = ?');
    const result = stmt.run(id);
    return result.changes > 0;
  }

  private getClassificationRuleById(id: string): ClassificationRule | null {
    const row = this.db.prepare('SELECT * FROM classification_rules WHERE id = ?').get(id) as DbRule | undefined;
    if (!row) return null;
    return this.mapDbRuleToEntity(row);
  }

  private mapDbRuleToEntity(row: DbRule): ClassificationRule {
    return {
      id: row.id,
      name: row.name,
      description: row.description || '',
      priority: row.priority,
      enabled: row.enabled === 1,
      conditions: JSON.parse(row.conditions),
      actions: JSON.parse(row.actions),
      createdAt: row.created_at,
      updatedAt: row.updated_at
    };
  }

  // 任務操作方法
  public createTask(task: Omit<OrganizationTask, 'id' | 'createdAt' | 'logs'>): OrganizationTask {
    const id = uuidv4();
    const now = Date.now();

    const stmt = this.db.prepare(`
      INSERT INTO organization_tasks (id, name, description, status, progress, total_files, processed_files, failed_files, created_at, started_at, completed_at, logs)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    stmt.run(
      id, task.name, task.description, task.status, task.progress,
      task.totalFiles, task.processedFiles, task.failedFiles, now,
      task.startedAt || null, task.completedAt || null, JSON.stringify(task.logs)
    );

    return this.getTaskById(id)!;
  }

  public updateTask(id: string, updates: Partial<OrganizationTask>): OrganizationTask | null {
    const setClause: string[] = [];
    const values: any[] = [];

    if (updates.status !== undefined) {
      setClause.push('status = ?');
      values.push(updates.status);
    }

    if (updates.progress !== undefined) {
      setClause.push('progress = ?');
      values.push(updates.progress);
    }

    if (updates.processedFiles !== undefined) {
      setClause.push('processed_files = ?');
      values.push(updates.processedFiles);
    }

    if (updates.failedFiles !== undefined) {
      setClause.push('failed_files = ?');
      values.push(updates.failedFiles);
    }

    if (updates.startedAt !== undefined) {
      setClause.push('started_at = ?');
      values.push(updates.startedAt);
    }

    if (updates.completedAt !== undefined) {
      setClause.push('completed_at = ?');
      values.push(updates.completedAt);
    }

    if (updates.logs !== undefined) {
      setClause.push('logs = ?');
      values.push(JSON.stringify(updates.logs));
    }

    if (setClause.length === 0) return this.getTaskById(id);

    values.push(id);
    const stmt = this.db.prepare(`UPDATE organization_tasks SET ${setClause.join(', ')} WHERE id = ?`);
    stmt.run(...values);

    return this.getTaskById(id);
  }

  public getTaskById(id: string): OrganizationTask | null {
    const row = this.db.prepare('SELECT * FROM organization_tasks WHERE id = ?').get(id) as DbTask | undefined;
    if (!row) return null;
    return this.mapDbTaskToEntity(row);
  }

  public getTasks(status?: string): OrganizationTask[] {
    let rows: DbTask[];

    if (status) {
      rows = this.db.prepare('SELECT * FROM organization_tasks WHERE status = ? ORDER BY created_at DESC').all(status) as DbTask[];
    } else {
      rows = this.db.prepare('SELECT * FROM organization_tasks ORDER BY created_at DESC').all() as DbTask[];
    }

    return rows.map(row => this.mapDbTaskToEntity(row));
  }

  private mapDbTaskToEntity(row: DbTask): OrganizationTask {
    return {
      id: row.id,
      name: row.name,
      description: row.description || '',
      status: row.status as any,
      progress: row.progress,
      totalFiles: row.total_files,
      processedFiles: row.processed_files,
      failedFiles: row.failed_files,
      createdAt: row.created_at,
      startedAt: row.started_at || undefined,
      completedAt: row.completed_at || undefined,
      logs: JSON.parse(row.logs || '[]')
    };
  }

  // 統計方法
  public getStatistics() {
    const totalFiles = this.db.prepare('SELECT COUNT(*) as count FROM files').get() as { count: number };
    const totalSize = this.db.prepare('SELECT COALESCE(SUM(size), 0) as size FROM files').get() as { size: number };
    const categoryStats = this.db.prepare(`
      SELECT category, COUNT(*) as count, COALESCE(SUM(size), 0) as size
      FROM files GROUP BY category
    `).all() as Array<{ category: string; count: number; size: number }>;
    const statusStats = this.db.prepare(`
      SELECT status, COUNT(*) as count FROM files GROUP BY status
    `).all() as Array<{ status: string; count: number }>;

    return {
      totalFiles: totalFiles.count,
      totalSize: totalSize.size,
      categoryStats: categoryStats.reduce((acc, stat) => {
        acc[stat.category as FileCategory] = {
          count: stat.count,
          size: stat.size,
          percentage: totalFiles.count > 0 ? (stat.count / totalFiles.count) * 100 : 0
        };
        return acc;
      }, {} as Record<string, { count: number; size: number; percentage: number }>),
      statusStats: statusStats.reduce((acc, stat) => {
        acc[stat.status as any] = stat.count;
        return acc;
      }, {} as Record<string, number>)
    };
  }

  // 配置操作方法
  public getSetting(key: string): string | null {
    const row = this.db.prepare('SELECT value FROM settings WHERE key = ?').get(key) as { value: string } | undefined;
    return row?.value || null;
  }

  public setSetting(key: string, value: string): void {
    const stmt = this.db.prepare(`
      INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, ?)
    `);
    stmt.run(key, value, Date.now());
  }

  public close(): void {
    this.db.close();
  }
}
