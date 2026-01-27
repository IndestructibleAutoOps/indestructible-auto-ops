/**
 * 文件實體類型定義
 * 包含文件屬性、分類資訊和狀態標識
 */

export interface FileEntity {
  /** 文件唯一識別碼 */
  id: string;

  /** 原始文件名稱 */
  name: string;

  /** 文件擴展名（小寫） */
  extension: string;

  /** 文件完整路徑 */
  path: string;

  /** 文件相對路徑（相對於監控目錄） */
  relativePath: string;

  /** 文件大小（位元組） */
  size: number;

  /** 文件MIME類型 */
  mimeType: string;

  /** 文件類別分類 */
  category: FileCategory;

  /** 文件子類別 */
  subcategory: string;

  /** 創建時間戳 */
  createdAt: number;

  /** 修改時間戳 */
  modifiedAt: number;

  /** 最後訪問時間戳 */
  accessedAt: number;

  /** 文件標籤 */
  tags: string[];

  /** 用戶自定義名稱 */
  customName?: string;

  /** 文件描述 */
  description?: string;

  /** 狀態標識 */
  status: FileStatus;

  /** 星標等級（1-5） */
  starRating: number;

  /** 是否已加密 */
  isEncrypted: boolean;

  /** 文件雜湊值 */
  hash?: string;
}

export type FileStatus =
  | 'pending'      // 待處理
  | 'classified'   // 已分類
  | 'organized'    // 已整理
  | 'archived'     // 已歸檔
  | 'ignored';     // 已忽略

export type FileCategory =
  | 'document'     // 文檔類
  | 'image'        // 圖片類
  | 'video'        // 視頻類
  | 'audio'        // 音頻類
  | 'archive'      // 壓縮包類
  | 'code'         // 代碼類
  | 'executable'   // 可執行檔
  | 'system'       // 系統檔案
  | 'other';       // 其他

export interface FileCategoryInfo {
  /** 分類名稱 */
  name: string;

  /** 分類顯示名稱 */
  displayName: string;

  /** 分類描述 */
  description: string;

  /** 包含的擴展名 */
  extensions: string[];

  /** 預設目標目錄 */
  targetDirectory: string;

  /** 圖標名稱 */
  icon: string;

  /** 顏色代碼 */
  color: string;
}

export interface DirectoryNode {
  /** 目錄名稱 */
  name: string;

  /** 目錄完整路徑 */
  path: string;

  /** 相對路徑 */
  relativePath: string;

  /** 目錄類型 */
  type: 'folder' | 'file';

  /** 子節點列表 */
  children?: DirectoryNode[];

  /** 文件數量 */
  fileCount: number;

  /** 目錄大小 */
  size: number;

  /** 是否展開 */
  expanded?: boolean;

  /** 選擇狀態 */
  selected?: boolean;
}

export interface ClassificationRule {
  /** 規則唯一識別碼 */
  id: string;

  /** 規則名稱 */
  name: string;

  /** 規則描述 */
  description: string;

  /** 規則優先級（數字越大優先級越高） */
  priority: number;

  /** 是否啟用 */
  enabled: boolean;

  /** 匹配條件 */
  conditions: ClassificationCondition[];

  /** 執行動作 */
  actions: ClassificationAction[];

  /** 創建時間 */
  createdAt: number;

  /** 最後更新時間 */
  updatedAt: number;
}

export interface ClassificationCondition {
  /** 條件類型 */
  type: 'extension' | 'mimeType' | 'size' | 'name' | 'path' | 'date';

  /** 比較運算符 */
  operator: 'equals' | 'contains' | 'startsWith' | 'endsWith' | 'matches' | 'greaterThan' | 'lessThan' | 'between';

  /** 條件值 */
  value: string | number | [number, number];

  /** 邏輯運算符（用於多條件組合） */
  logic?: 'AND' | 'OR';
}

export interface ClassificationAction {
  /** 動作類型 */
  type: 'move' | 'copy' | 'rename' | 'tag' | 'category' | 'ignore';

  /** 動作參數 */
  parameters: Record<string, any>;
}

export interface OrganizationTask {
  /** 任務唯一識別碼 */
  id: string;

  /** 任務名稱 */
  name: string;

  /** 任務描述 */
  description?: string;

  /** 任務狀態 */
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';

  /** 進度百分比 */
  progress: number;

  /** 總文件數 */
  totalFiles: number;

  /** 已處理文件數 */
  processedFiles: number;

  /** 失敗文件數 */
  failedFiles: number;

  /** 創建時間 */
  createdAt: number;

  /** 開始時間 */
  startedAt?: number;

  /** 完成時間 */
  completedAt?: number;

  /** 任務日誌 */
  logs: TaskLog[];
}

export interface TaskLog {
  /** 日誌時間戳 */
  timestamp: number;

  /** 日誌級別 */
  level: 'info' | 'warning' | 'error' | 'success';

  /** 日誌消息 */
  message: string;

  /** 相關文件ID */
  fileId?: string;
}

export interface Statistics {
  /** 總文件數 */
  totalFiles: number;

  /** 總大小（位元組） */
  totalSize: number;

  /** 總目錄數 */
  totalDirectories: number;

  /** 分類統計 */
  categoryStats: Record<FileCategory, CategoryStat>;

  /** 狀態統計 */
  statusStats: Record<FileStatus, number>;

  /** 最近活動 */
  recentActivities: ActivityRecord[];
}

export interface CategoryStat {
  count: number;
  size: number;
  percentage: number;
}

export interface ActivityRecord {
  /** 活動類型 */
  type: 'upload' | 'move' | 'rename' | 'delete' | 'classify' | 'organize';

  /** 活動描述 */
  description: string;

  /** 相關文件數量 */
  fileCount: number;

  /** 時間戳 */
  timestamp: number;
}

export interface ApiResponse<T> {
  /** 響應狀態碼 */
  code: number;

  /** 響應消息 */
  message: string;

  /** 響應數據 */
  data?: T;

  /** 錯誤詳情 */
  error?: string;
}

export interface PaginationParams {
  /** 頁碼（從1開始） */
  page: number;

  /** 每頁數量 */
  pageSize: number;

  /** 排序欄位 */
  sortBy?: string;

  /** 排序方向 */
  sortOrder?: 'asc' | 'desc';
}

export interface FileListResponse {
  /** 文件列表 */
  files: FileEntity[];

  /** 總數 */
  total: number;

  /** 當前頁碼 */
  page: number;

  /** 每頁大小 */
  pageSize: number;

  /** 總頁數 */
  totalPages: number;
}
