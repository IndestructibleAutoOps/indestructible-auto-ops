/**
 * 文件組織服務
 * 負責文件移動、重命名、目錄結構管理
 */

import fs from 'fs/promises';
import path from 'path';
import { v4 as uuidv4 } from 'uuid';
import type { FileEntity, OrganizationTask, TaskLog, FileCategory } from '../types/index.js';
import { ClassificationEngine, CATEGORY_CONFIG } from './classification.js';

interface OrganizeOptions {
  /** 監控目錄 */
  watchDirectory: string;

  /** 目標目錄 */
  targetDirectory: string;

  /** 是否保留原始目錄結構 */
  preserveStructure: boolean;

  /** 是否覆蓋已存在的文件 */
  overwriteExisting: boolean;

  /** 自定義分類映射 */
  categoryMapping?: Record<FileCategory, string>;

  /** 排除的文件模式 */
  excludePatterns?: string[];

  /** 文件大小限制（位元組） */
  maxFileSize?: number;

  /** 最小文件大小（位元組） */
  minFileSize?: number;
}

interface ProgressCallback {
  (progress: number, currentFile: string, status: string): void;
}

export class FileOrganizationService {
  private watchDirectory: string;
  private targetDirectory: string;
  private classificationEngine: ClassificationEngine;
  private currentTask: OrganizationTask | null = null;
  private progressCallback: ProgressCallback | null = null;

  constructor(options: OrganizeOptions) {
    this.watchDirectory = path.resolve(options.watchDirectory);
    this.targetDirectory = path.resolve(options.targetDirectory);
    this.classificationEngine = new ClassificationEngine();

    // 確保目標目錄存在
    this.ensureDirectory(this.targetDirectory);
  }

  /**
   * 確保目錄存在
   */
  private async ensureDirectory(dirPath: string): Promise<void> {
    try {
      await fs.access(dirPath);
    } catch {
      await fs.mkdir(dirPath, { recursive: true });
    }
  }

  /**
   * 設置進度回調
   */
  public setProgressCallback(callback: ProgressCallback): void {
    this.progressCallback = callback;
  }

  /**
   * 掃描目錄中的所有文件
   */
  public async scanDirectory(dirPath?: string): Promise<FileEntity[]> {
    const scanPath = dirPath || this.watchDirectory;
    const files: FileEntity[] = [];

    try {
      const entries = await fs.readdir(scanPath, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(scanPath, entry.name);

        if (entry.isDirectory()) {
          // 遞歸掃描子目錄
          const subFiles = await this.scanDirectory(fullPath);
          files.push(...subFiles);
        } else if (entry.isFile()) {
          // 處理文件
          const file = await this.analyzeFile(fullPath);
          if (file) {
            files.push(file);
          }
        }
      }
    } catch (error) {
      console.error('掃描目錄失敗:', error);
    }

    return files;
  }

  /**
   * 分析單個文件
   */
  public async analyzeFile(filePath: string): Promise<FileEntity | null> {
    try {
      const stats = await fs.stat(filePath);
      const filename = path.basename(filePath);
      const relativePath = path.relative(this.watchDirectory, filePath);
      const extension = this.classificationEngine.extractExtension(filename).toLowerCase();

      // 獲取MIME類型
      const mimeType = this.getMimeType(filePath, extension);

      // 智能分類
      const category = this.classificationEngine.classifySmart(filename, mimeType, stats.size);

      const file: FileEntity = {
        id: uuidv4(),
        name: filename,
        extension: extension,
        path: filePath,
        relativePath: relativePath,
        size: stats.size,
        mimeType: mimeType,
        category: category,
        subcategory: '',
        createdAt: stats.birthtimeMs,
        modifiedAt: stats.mtimeMs,
        accessedAt: stats.atimeMs,
        tags: [],
        status: 'pending',
        starRating: 0,
        isEncrypted: false
      };

      return file;
    } catch (error) {
      console.error('分析文件失敗:', filePath, error);
      return null;
    }
  }

  /**
   * 獲取文件的MIME類型
   */
  private getMimeType(filePath: string, extension: string): string {
    const mimeTypes: Record<string, string> = {
      // 圖片
      'jpg': 'image/jpeg',
      'jpeg': 'image/jpeg',
      'png': 'image/png',
      'gif': 'image/gif',
      'bmp': 'image/bmp',
      'svg': 'image/svg+xml',
      'webp': 'image/webp',
      'ico': 'image/x-icon',
      'tif': 'image/tiff',
      'tiff': 'image/tiff',

      // 視頻
      'mp4': 'video/mp4',
      'avi': 'video/x-msvideo',
      'mkv': 'video/x-matroska',
      'mov': 'video/quicktime',
      'wmv': 'video/x-ms-wmv',
      'flv': 'video/x-flv',
      'webm': 'video/webm',

      // 音頻
      'mp3': 'audio/mpeg',
      'wav': 'audio/wav',
      'flac': 'audio/flac',
      'aac': 'audio/aac',
      'ogg': 'audio/ogg',
      'wma': 'audio/x-ms-wma',
      'm4a': 'audio/x-m4a',

      // 文檔
      'pdf': 'application/pdf',
      'doc': 'application/msword',
      'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'xls': 'application/vnd.ms-excel',
      'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'ppt': 'application/vnd.ms-powerpoint',
      'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
      'txt': 'text/plain',
      'csv': 'text/csv',
      'md': 'text/markdown',
      'markdown': 'text/markdown',

      // 壓縮
      'zip': 'application/zip',
      'rar': 'application/x-rar-compressed',
      '7z': 'application/x-7z-compressed',
      'tar': 'application/x-tar',
      'gz': 'application/gzip',
      'bz2': 'application/x-bzip2',

      // 代碼
      'js': 'application/javascript',
      'ts': 'application/typescript',
      'jsx': 'text/javascript',
      'tsx': 'text/typescript',
      'vue': 'text/html',
      'py': 'text/x-python',
      'java': 'text/x-java',
      'c': 'text/x-c',
      'cpp': 'text/x-c++',
      'cs': 'text/x-csharp',
      'go': 'text/x-go',
      'rs': 'text/x-rust',
      'rb': 'text/x-ruby',
      'php': 'text/x-php',
      'swift': 'text/x-swift',
      'kt': 'text/x-kotlin',
      'lua': 'text/x-lua',
      'sh': 'application/x-sh',
      'bash': 'application/x-sh',
      'json': 'application/json',
      'xml': 'application/xml',
      'html': 'text/html',
      'css': 'text/css',

      // 可執行
      'exe': 'application/x-msdownload',
      'dll': 'application/x-executable',
      'so': 'application/x-executable',
      'dylib': 'application/x-executable',

      // 默認
      '': 'application/octet-stream'
    };

    return mimeTypes[extension.toLowerCase()] || 'application/octet-stream';
  }

  /**
   * 執行文件組織任務
   */
  public async organizeFiles(
    files: FileEntity[],
    options: {
      createDateFolders?: boolean;
      createCategoryFolders?: boolean;
      prefixFiles?: boolean;
      suffixTimestamp?: boolean;
    } = {}
  ): Promise<{ success: FileEntity[]; failed: Array<{ file: FileEntity; error: string }> }> {
    const success: FileEntity[] = [];
    const failed: Array<{ file: FileEntity; error: string }> = [];
    const total = files.length;
    let processed = 0;

    for (const file of files) {
      try {
        // 計算目標路徑
        const targetPath = await this.calculateTargetPath(file, options);

        // 確保目標目錄存在
        await this.ensureDirectory(path.dirname(targetPath));

        // 移動或複製文件
        await this.moveFile(file.path, targetPath);

        // 更新文件資訊
        file.path = targetPath;
        file.relativePath = path.relative(this.watchDirectory, targetPath);
        file.status = 'organized';

        success.push(file);

        // 更新進度
        processed++;
        const progress = Math.round((processed / total) * 100);

        if (this.progressCallback) {
          this.progressCallback(progress, file.name, '處理中');
        }
      } catch (error) {
        failed.push({
          file,
          error: error instanceof Error ? error.message : '未知錯誤'
        });

        file.status = 'pending';
      }
    }

    return { success, failed };
  }

  /**
   * 計算目標路徑
   */
  private async calculateTargetPath(
    file: FileEntity,
    options: {
      createDateFolders?: boolean;
      createCategoryFolders?: boolean;
      prefixFiles?: boolean;
      suffixTimestamp?: boolean;
    }
  ): Promise<string> {
    let targetPath = this.targetDirectory;

    // 按分類創建目錄
    if (options.createCategoryFolders !== false) {
      const categoryInfo = CATEGORY_CONFIG[file.category];
      targetPath = path.join(targetPath, categoryInfo?.targetDirectory || 'others');
    }

    // 按日期創建目錄
    if (options.createDateFolders) {
      const date = new Date(file.modifiedAt);
      const dateFolder = date.toISOString().split('T')[0].replace(/-/g, '');
      targetPath = path.join(targetPath, dateFolder);
    }

    // 生成文件名
    let fileName = file.name;

    if (options.prefixFiles) {
      const prefix = file.category.toUpperCase().slice(0, 3);
      fileName = `${prefix}_${fileName}`;
    }

    if (options.suffixTimestamp) {
      const timestamp = Date.now();
      const ext = this.classificationEngine.extractExtension(fileName);
      const baseName = this.classificationEngine.extractBaseName(fileName);
      fileName = `${baseName}_${timestamp}.${ext}`;
    }

    targetPath = path.join(targetPath, fileName);

    return targetPath;
  }

  /**
   * 移動文件
   */
  private async moveFile(sourcePath: string, targetPath: string): Promise<void> {
    try {
      // 檢查目標文件是否存在
      try {
        await fs.access(targetPath);
        // 如果存在，添加時間戳後綴
        const ext = path.extname(targetPath);
        const baseName = path.basename(targetPath, ext);
        const timestamp = Date.now();
        const newPath = path.join(path.dirname(targetPath), `${baseName}_${timestamp}${ext}`);
        await fs.rename(sourcePath, newPath);
      } catch {
        // 目標不存在，直接移動
        await fs.rename(sourcePath, targetPath);
      }
    } catch (error) {
      // 如果移動失敗，嘗試複製後刪除
      await fs.copyFile(sourcePath, targetPath);
      await fs.unlink(sourcePath);
    }
  }

  /**
   * 重命名文件
   */
  public async renameFile(file: FileEntity, newName: string): Promise<FileEntity> {
    const directory = path.dirname(file.path);
    const newPath = path.join(directory, newName);

    await fs.rename(file.path, newPath);

    file.name = newName;
    file.path = newPath;
    file.relativePath = path.relative(this.watchDirectory, newPath);
    file.modifiedAt = Date.now();
    file.status = 'organized';

    return file;
  }

  /**
   * 批量重命名文件
   */
  public async batchRename(
    files: FileEntity[],
    namePattern: string
  ): Promise<{ success: FileEntity[]; failed: Array<{ file: FileEntity; error: string }> }> {
    const success: FileEntity[] = [];
    const failed: Array<{ file: FileEntity; error: string }> = [];

    for (let i = 0; i < files.length; i++) {
      try {
        const file = files[i];
        const ext = this.classificationEngine.extractExtension(file.name);
        const baseName = this.classificationEngine.extractBaseName(file.name);

        // 替換模式中的佔位符
        let newName = namePattern
          .replace('{name}', baseName)
          .replace('{ext}', ext)
          .replace('{i}', String(i + 1).padStart(3, '0'))
          .replace('{date}', new Date().toISOString().slice(0, 10));

        // 確保有正確的擴展名
        if (!newName.endsWith(`.${ext}`)) {
          newName = `${newName}.${ext}`;
        }

        const renamedFile = await this.renameFile(file, newName);
        success.push(renamedFile);
      } catch (error) {
        failed.push({
          file,
          error: error instanceof Error ? error.message : '未知錯誤'
        });
      }
    }

    return { success, failed };
  }

  /**
   * 創建目錄結構
   */
  public async createDirectoryStructure(
    structure: Array<{ path: string; type: 'file' | 'directory' }>
  ): Promise<void> {
    const createdPaths = new Set<string>();

    for (const item of structure) {
      const fullPath = path.join(this.targetDirectory, item.path);

      if (createdPaths.has(fullPath)) continue;

      try {
        if (item.type === 'directory') {
          await fs.mkdir(fullPath, { recursive: true });
        } else {
          await fs.mkdir(path.dirname(fullPath), { recursive: true });
        }
        createdPaths.add(fullPath);
      } catch (error) {
        console.error('創建目錄失敗:', fullPath, error);
      }
    }
  }

  /**
   * 生成預設目錄結構
   */
  public generateDefaultStructure(): Array<{ path: string; type: 'file' | 'directory' }> {
    const structure: Array<{ path: string; type: 'file' | 'directory' }> = [];

    // 添加各分類目錄
    for (const category of Object.values(CATEGORY_CONFIG)) {
      if (category.targetDirectory !== 'others') {
        structure.push({ path: category.targetDirectory, type: 'directory' });
      }
    }

    // 添加額外目錄
    structure.push({ path: 'temp', type: 'directory' });
    structure.push({ path: 'backup', type: 'directory' });

    return structure;
  }

  /**
   * 獲取當前任務狀態
   */
  public getCurrentTask(): OrganizationTask | null {
    return this.currentTask;
  }

  /**
   * 取消當前任務
   */
  public async cancelTask(): Promise<void> {
    if (this.currentTask) {
      this.currentTask.status = 'cancelled';
      this.currentTask = null;
    }
  }
}

/**
 * 創建文件組織服務實例
 */
export function createOrganizationService(options: OrganizeOptions): FileOrganizationService {
  return new FileOrganizationService(options);
}
