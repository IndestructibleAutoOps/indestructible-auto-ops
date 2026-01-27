/**
 * 文件分類引擎
 * 基於擴展名、MIME類型和自定義規則的智能分類系統
 */

import type { FileCategory, FileCategoryInfo, ClassificationRule, ClassificationCondition, ClassificationAction } from '../types/index.js';

/**
 * 預設分類配置
 */
export const CATEGORY_CONFIG: Record<FileCategory, FileCategoryInfo> = {
  document: {
    name: 'document',
    displayName: '文檔',
    description: '文本文档、Office文档、PDF等',
    extensions: ['doc', 'docx', 'docm', 'dot', 'dotx', 'dotm', 'xls', 'xlsx', 'xlsm', 'xlsb', 'ppt', 'pptx', 'pptm', 'pdf', 'txt', 'rtf', 'odt', 'ods', 'odp', 'csv', 'xml', 'json', 'yaml', 'yml', 'md', 'markdown', 'rst', 'tex', 'wpd', 'wps'],
    targetDirectory: 'documents',
    icon: 'FileText',
    color: '#3498db'
  },
  image: {
    name: 'image',
    displayName: '圖片',
    description: '圖片、照片、圖形文件',
    extensions: ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp', 'ico', 'tif', 'tiff', 'psd', 'ai', 'eps', 'raw', 'cr2', 'nef', 'arw', 'dng', 'heic', 'heif', 'avif', 'jxl'],
    targetDirectory: 'images',
    icon: 'Image',
    color: '#9b59b6'
  },
  video: {
    name: 'video',
    displayName: '視頻',
    description: '視頻、電影、動畫文件',
    extensions: ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'm4v', 'mpg', 'mpeg', 'm2v', '3gp', '3g2', 'rm', 'rmvb', 'vob', 'ogv', 'divx', 'xvid', 'm2ts', 'mts', 'ts'],
    targetDirectory: 'videos',
    icon: 'Video',
    color: '#e74c3c'
  },
  audio: {
    name: 'audio',
    displayName: '音頻',
    description: '音樂、語音、音效文件',
    extensions: ['mp3', 'wav', 'flac', 'aac', 'ogg', 'wma', 'm4a', 'aiff', 'aif', 'opus', 'ac3', 'dts', 'alac', 'mid', 'midi', 'amr', 'ape', 'ra', 'cue'],
    targetDirectory: 'audio',
    icon: 'Music',
    color: '#1abc9c'
  },
  archive: {
    name: 'archive',
    displayName: '壓縮包',
    description: '壓縮文件、歸檔文件',
    extensions: ['zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'xz', 'lzma', 'z', 'tgz', 'tbz2', 'txz', 'lz', 'lzh', 'arj', 'cab', 'iso', 'img', 'dmg', 'rpm', 'deb'],
    targetDirectory: 'archives',
    icon: 'Archive',
    color: '#f39c12'
  },
  code: {
    name: 'code',
    displayName: '代碼',
    description: '源代碼、腳本、配置文件',
    extensions: ['js', 'ts', 'jsx', 'tsx', 'vue', 'svelte', 'py', 'java', 'c', 'cpp', 'cxx', 'cc', 'h', 'hpp', 'hxx', 'cs', 'go', 'rs', 'rb', 'php', 'swift', 'kt', 'kts', 'scala', 'r', 'R', 'm', 'lua', 'pl', 'pm', 'perl', 'sh', 'bash', 'zsh', 'ps1', 'bat', 'cmd', 'dockerfile', 'makefile', 'cmake', 'gradle', 'yaml', 'yml', 'xml', 'json', 'ini', 'conf', 'config', 'env', 'gitignore', 'eslintrc', 'prettierrc'],
    targetDirectory: 'code',
    icon: 'Code',
    color: '#2ecc71'
  },
  executable: {
    name: 'executable',
    displayName: '可執行檔',
    description: '可執行程序、安裝包',
    extensions: ['exe', 'msi', 'dmg', 'app', 'deb', 'rpm', 'apk', 'ipa', 'xap', 'appx', 'appxbundle', 'jar', 'class', 'dll', 'so', 'dylib', 'bin', 'out'],
    targetDirectory: 'executables',
    icon: 'Cpu',
    color: '#e67e22'
  },
  system: {
    name: 'system',
    displayName: '系統檔案',
    description: '系統文件、隱藏文件',
    extensions: ['sys', 'dll', 'ocx', 'drv', 'vxd', 'fon', 'ttf', 'otf', 'fon', 'cur', 'ani', 'lnk', 'ini', 'inf', 'cat', 'cab', 'hlp', 'chm'],
    targetDirectory: 'system',
    icon: 'Settings',
    color: '#95a5a6'
  },
  other: {
    name: 'other',
    displayName: '其他',
    description: '未分類的文件',
    extensions: [],
    targetDirectory: 'others',
    icon: 'File',
    color: '#bdc3c7'
  }
};

/**
 * MIME類型映射表
 */
const MIME_TYPE_MAP: Record<string, FileCategory> = {
  // 文檔類
  'application/pdf': 'document',
  'application/msword': 'document',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'document',
  'application/vnd.ms-excel': 'document',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'document',
  'application/vnd.ms-powerpoint': 'document',
  'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'document',
  'text/plain': 'document',
  'text/csv': 'document',
  'text/markdown': 'document',
  'application/rtf': 'document',

  // 圖片類
  'image/jpeg': 'image',
  'image/png': 'image',
  'image/gif': 'image',
  'image/bmp': 'image',
  'image/svg+xml': 'image',
  'image/webp': 'image',
  'image/tiff': 'image',
  'image/x-icon': 'image',

  // 視頻類
  'video/mp4': 'video',
  'video/x-msvideo': 'video',
  'video/x-matroska': 'video',
  'video/quicktime': 'video',
  'video/webm': 'video',
  'video/x-ms-wmv': 'video',
  'video/x-flv': 'video',

  // 音頻類
  'audio/mpeg': 'audio',
  'audio/wav': 'audio',
  'audio/flac': 'audio',
  'audio/aac': 'audio',
  'audio/ogg': 'audio',
  'audio/x-m4a': 'audio',
  'audio/webm': 'audio',

  // 壓縮類
  'application/zip': 'archive',
  'application/x-rar-compressed': 'archive',
  'application/x-7z-compressed': 'archive',
  'application/x-tar': 'archive',
  'application/gzip': 'archive',
  'application/x-bzip2': 'archive',

  // 代碼類
  'application/javascript': 'code',
  'text/javascript': 'code',
  'application/typescript': 'code',
  'text/typescript': 'code',
  'text/x-python': 'code',
  'application/x-python': 'code',
  'text/x-java': 'code',
  'text/x-c': 'code',
  'text/x-c++': 'code',
  'text/x-csharp': 'code',
  'application/json': 'code',
  'application/xml': 'code',
  'text/xml': 'code',
  'text/css': 'code',
  'text/html': 'code',

  // 可執行類
  'application/x-msdownload': 'executable',
  'application/x-executable': 'executable',
  'application/x-sh': 'executable'
};

export class ClassificationEngine {
  private rules: ClassificationRule[];

  constructor(rules: ClassificationRule[] = []) {
    this.rules = rules;
  }

  /**
   * 更新分類規則
   */
  public setRules(rules: ClassificationRule[]): void {
    this.rules = [...rules].sort((a, b) => b.priority - a.priority);
  }

  /**
   * 根據文件名分類
   */
  public classifyByName(filename: string): FileCategory {
    const ext = this.extractExtension(filename).toLowerCase();

    for (const category of Object.keys(CATEGORY_CONFIG) as FileCategory[]) {
      if (CATEGORY_CONFIG[category].extensions.includes(ext)) {
        return category;
      }
    }

    return 'other';
  }

  /**
   * 根據MIME類型分類
   */
  public classifyByMimeType(mimeType: string): FileCategory {
    const normalizedMime = mimeType.toLowerCase().trim();

    // 精確匹配
    if (MIME_TYPE_MAP[normalizedMime]) {
      return MIME_TYPE_MAP[normalizedMime];
    }

    // 前綴匹配
    const prefix = normalizedMime.split('/')[0];
    const prefixMap: Record<string, FileCategory> = {
      'image': 'image',
      'video': 'video',
      'audio': 'audio',
      'text': 'document',
      'application': 'other'
    };

    if (prefixMap[prefix]) {
      return prefixMap[prefix];
    }

    return 'other';
  }

  /**
   * 智能分類（綜合多個維度）
   */
  public classifySmart(filename: string, mimeType?: string, size?: number): FileCategory {
    // 首先根據MIME類型分類
    if (mimeType) {
      const mimeCategory = this.classifyByMimeType(mimeType);
      if (mimeCategory !== 'other') {
        return mimeCategory;
      }
    }

    // 根據文件名分類
    const nameCategory = this.classifyByName(filename);
    if (nameCategory !== 'other') {
      return nameCategory;
    }

    // 檢查應用自定義規則
    const customCategory = this.applyCustomRules(filename, mimeType, size);
    if (customCategory) {
      return customCategory;
    }

    return 'other';
  }

  /**
   * 提取文件擴展名
   */
  public extractExtension(filename: string): string {
    const parts = filename.split('.');
    return parts.length > 1 ? parts.pop() || '' : '';
  }

  /**
   * 提取文件名（不含擴展名）
   */
  public extractBaseName(filename: string): string {
    const ext = this.extractExtension(filename);
    return ext ? filename.slice(0, -ext.length - 1) : filename;
  }

  /**
   * 判斷是否為圖片文件
   */
  public isImage(filename: string, mimeType?: string): boolean {
    const category = this.classifySmart(filename, mimeType);
    return category === 'image';
  }

  /**
   * 判斷是否為文檔文件
   */
  public isDocument(filename: string, mimeType?: string): boolean {
    const category = this.classifySmart(filename, mimeType);
    return category === 'document';
  }

  /**
   * 判斷是否為視頻文件
   */
  public isVideo(filename: string, mimeType?: string): boolean {
    const category = this.classifySmart(filename, mimeType);
    return category === 'video';
  }

  /**
   * 判斷是否為音頻文件
   */
  public isAudio(filename: string, mimeType?: string): boolean {
    const category = this.classifySmart(filename, mimeType);
    return category === 'audio';
  }

  /**
   * 判斷是否為壓縮文件
   */
  public isArchive(filename: string, mimeType?: string): boolean {
    const category = this.classifySmart(filename, mimeType);
    return category === 'archive';
  }

  /**
   * 判斷是否為代碼文件
   */
  public isCode(filename: string, mimeType?: string): boolean {
    const category = this.classifySmart(filename, mimeType);
    return category === 'code';
  }

  /**
   * 獲取所有可用的分類
   */
  public getCategories(): FileCategoryInfo[] {
    return Object.values(CATEGORY_CONFIG);
  }

  /**
   * 獲取特定分類的資訊
   */
  public getCategoryInfo(category: FileCategory): FileCategoryInfo | undefined {
    return CATEGORY_CONFIG[category];
  }

  /**
   * 獲取分類的目標目錄
   */
  public getTargetDirectory(category: FileCategory): string {
    return CATEGORY_CONFIG[category]?.targetDirectory || 'others';
  }

  /**
   * 應用自定義分類規則
   */
  private applyCustomRules(filename: string, mimeType?: string, size?: number): FileCategory | null {
    for (const rule of this.rules) {
      if (!rule.enabled) continue;

      if (this.evaluateRuleConditions(rule.conditions, filename, mimeType, size)) {
        for (const action of rule.actions) {
          if (action.type === 'category') {
            return action.parameters.category as FileCategory;
          }
        }
      }
    }

    return null;
  }

  /**
   * 評估規則條件
   */
  private evaluateRuleConditions(
    conditions: ClassificationCondition[],
    filename: string,
    mimeType?: string,
    size?: number
  ): boolean {
    if (conditions.length === 0) return false;

    const results = conditions.map(condition => {
      return this.evaluateCondition(condition, filename, mimeType, size);
    });

    // 第一個條件決定邏輯運算符
    const logic = conditions[0].logic || 'AND';

    if (logic === 'AND') {
      return results.every(r => r);
    } else {
      return results.some(r => r);
    }
  }

  /**
   * 評估單個條件
   */
  private evaluateCondition(
    condition: ClassificationCondition,
    filename: string,
    mimeType?: string,
    size?: number
  ): boolean {
    let valueToCompare: string | number | undefined;

    switch (condition.type) {
      case 'extension':
        valueToCompare = this.extractExtension(filename).toLowerCase();
        break;
      case 'mimeType':
        valueToCompare = mimeType?.toLowerCase();
        break;
      case 'name':
        valueToCompare = filename.toLowerCase();
        break;
      case 'path':
        valueToCompare = filename.toLowerCase();
        break;
      case 'size':
        valueToCompare = size;
        break;
      case 'date':
        valueToCompare = Date.now();
        break;
      default:
        return false;
    }

    if (valueToCompare === undefined) return false;

    return this.compareValues(valueToCompare, condition.operator, condition.value);
  }

  /**
   * 比較值
   */
  private compareValues(
    actual: string | number,
    operator: ClassificationCondition['operator'],
    expected: string | number | [number, number]
  ): boolean {
    switch (operator) {
      case 'equals':
        if (typeof actual === 'string' && typeof expected === 'string') {
          return actual.toLowerCase() === expected.toLowerCase();
        }
        return actual === expected;

      case 'contains':
        if (typeof actual === 'string' && typeof expected === 'string') {
          return actual.toLowerCase().includes(expected.toLowerCase());
        }
        return false;

      case 'startsWith':
        if (typeof actual === 'string' && typeof expected === 'string') {
          return actual.toLowerCase().startsWith(expected.toLowerCase());
        }
        return false;

      case 'endsWith':
        if (typeof actual === 'string' && typeof expected === 'string') {
          return actual.toLowerCase().endsWith(expected.toLowerCase());
        }
        return false;

      case 'matches':
        if (typeof actual === 'string' && typeof expected === 'string') {
          try {
            const regex = new RegExp(expected, 'i');
            return regex.test(actual);
          } catch {
            return false;
          }
        }
        return false;

      case 'greaterThan':
        return typeof actual === 'number' && typeof expected === 'number' && actual > expected;

      case 'lessThan':
        return typeof actual === 'number' && typeof expected === 'number' && actual < expected;

      case 'between':
        if (typeof actual === 'number' && Array.isArray(expected)) {
          return actual >= expected[0] && actual <= expected[1];
        }
        return false;

      default:
        return false;
    }
  }

  /**
   * 生成文件建議的新路徑
   */
  public suggestNewPath(
    filename: string,
    category: FileCategory,
    targetDirectory?: string
  ): string {
    const baseName = this.extractBaseName(filename);
    const extension = this.extractExtension(filename);
    const baseDirectory = targetDirectory || this.getTargetDirectory(category);

    const newFilename = `${baseName}_${Date.now()}.${extension}`;
    return `${baseDirectory}/${newFilename}`;
  }

  /**
   * 批量分類文件
   */
  public batchClassify(
    files: Array<{ name: string; mimeType?: string; size?: number }>
  ): Map<string, FileCategory> {
    const results = new Map<string, FileCategory>();

    for (const file of files) {
      const category = this.classifySmart(file.name, file.mimeType, file.size);
      results.set(file.name, category);
    }

    return results;
  }
}

/**
 * 創建預設分類規則
 */
export function createDefaultClassificationRules(): ClassificationRule[] {
  return [
    {
      id: 'rule-images',
      name: '圖片分類',
      description: '自動將圖片文件分類到圖片目錄',
      priority: 100,
      enabled: true,
      conditions: [
        {
          type: 'extension',
          operator: 'matches',
          value: 'jpg|jpeg|png|gif|bmp|svg|webp|tiff?|ico|psd|ai|eps'
        }
      ],
      actions: [
        {
          type: 'category',
          parameters: { category: 'image' }
        }
      ],
      createdAt: Date.now(),
      updatedAt: Date.now()
    },
    {
      id: 'rule-documents',
      name: '文檔分類',
      description: '將文檔文件分類到文檔目錄',
      priority: 90,
      enabled: true,
      conditions: [
        {
          type: 'extension',
          operator: 'matches',
          value: 'docx?|xlsx?|pptx?|pdf|txt|csv|md|markdown|rtf|od[tsfp]|xml|json|yaml|yml'
        }
      ],
      actions: [
        {
          type: 'category',
          parameters: { category: 'document' }
        }
      ],
      createdAt: Date.now(),
      updatedAt: Date.now()
    },
    {
      id: 'rule-code',
      name: '代碼分類',
      description: '將源代碼文件分類到代碼目錄',
      priority: 80,
      enabled: true,
      conditions: [
        {
          type: 'extension',
          operator: 'matches',
          value: 'js|ts|jsx|tsx|vue|py|java|c|cpp|cs|go|rs|rb|php|swift|kt|scala|lua|perl|sh|bash'
        }
      ],
      actions: [
        {
          type: 'category',
          parameters: { category: 'code' }
        }
      ],
      createdAt: Date.now(),
      updatedAt: Date.now()
    },
    {
      id: 'rule-media',
      name: '媒體分類',
      description: '將音頻和視頻文件分類到媒體目錄',
      priority: 70,
      enabled: true,
      conditions: [
        {
          type: 'extension',
          operator: 'matches',
          value: 'mp3|wav|flac|aac|ogg|wma|m4a|mp4|avi|mkv|mov|wmv|webm|flv'
        }
      ],
      actions: [
        {
          type: 'category',
          parameters: { category: 'video' }
        }
      ],
      createdAt: Date.now(),
      updatedAt: Date.now()
    },
    {
      id: 'rule-archives',
      name: '壓縮包分類',
      description: '將壓縮文件分類到歸檔目錄',
      priority: 60,
      enabled: true,
      conditions: [
        {
          type: 'extension',
          operator: 'matches',
          value: 'zip|rar|7z|tar|gz|bz2|xz|lzma|tgz|tbz2|iso|dmg'
        }
      ],
      actions: [
        {
          type: 'category',
          parameters: { category: 'archive' }
        }
      ],
      createdAt: Date.now(),
      updatedAt: Date.now()
    }
  ];
}
