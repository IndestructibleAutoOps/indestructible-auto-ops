// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-fabric-storage
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Unified Intelligence Fabric - Fabric Storage
 * Version 19.0.0
 * 
 * 核心：疊加態原生儲存
 * - 檔案不是靜態，而是多版本、多語意、多現實的疊加態節點
 * - 支援版本展開、回溯、對齊、參與推理
 * - 疊加態壓縮與解壓縮
 * - 現實映射與轉換
 */

import { FabricNode, SuperpositionState, NodeVersion, SemanticVariant, RealityVariant } from '../fabric-core';

// ============================================================================
// Type Definitions
// ============================================================================

export interface StorageConfig {
  basePath: string;
  maxVersions: number;
  retentionDays: number;
  compressionLevel: number; // 0-1, 1 = 最高壓縮
  enableVersioning: boolean;
  enableSuperposition: boolean;
}

export interface CompressedSuperposition {
  nodeId: string;
  compressedVersions: CompressedVersion[];
  compressedSemantics: CompressedSemantic[];
  compressedRealities: CompressedReality[];
  compressionRatio: number;
  compressionMethod: string;
  checksum: string;
  timestamp: number;
}

export interface CompressedVersion {
  id: string;
  version: string;
  delta: any; // 增量差異
  timestamp: number;
  size: number;
}

export interface CompressedSemantic {
  id: string;
  semanticType: string;
  confidence: number;
  compressedMeaning: any; // 壓縮後的語意
  timestamp: number;
  size: number;
}

export interface CompressedReality {
  id: string;
  realityId: string;
  compressedAbstraction: any; // 壓縮後的抽象
  timestamp: number;
  size: number;
}

export interface SuperpositionQuery {
  nodeId: string;
  version?: string;
  semanticType?: string;
  realityId?: string;
  since?: number;
  until?: number;
}

export interface SuperpositionOperation {
  type: 'expand' | 'collapse' | 'merge' | 'split' | 'align' | 'transform';
  nodeId: string;
  parameters: any;
  result: any;
  timestamp: number;
}

// ============================================================================
// Fabric Storage Class
// ============================================================================

export class FabricStorage {
  private config: StorageConfig;
  private storageEngine: StorageEngine;
  private compressionEngine: SuperpositionCompressionEngine;
  private versionManager: VersionManager;
  private realityManager: RealityManager;
  private initialized: boolean;
  
  constructor(config?: Partial<StorageConfig>) {
    this.config = {
      basePath: config?.basePath || './fabric-storage',
      maxVersions: config?.maxVersions || 100,
      retentionDays: config?.retentionDays || 365,
      compressionLevel: config?.compressionLevel || 0.8,
      enableVersioning: config?.enableVersioning ?? true,
      enableSuperposition: config?.enableSuperposition ?? true
    };
    
    this.storageEngine = new StorageEngine(this.config);
    this.compressionEngine = new SuperpositionCompressionEngine(this.config);
    this.versionManager = new VersionManager(this.config);
    this.realityManager = new RealityManager(this.config);
    this.initialized = false;
  }
  
  async initialize(): Promise<void> {
    console.log('[Fabric Storage] Initializing superposition-native storage...');
    
    // 初始化儲存引擎
    await this.storageEngine.initialize();
    
    // 初始化壓縮引擎
    await this.compressionEngine.initialize();
    
    // 初始化版本管理器
    await this.versionManager.initialize();
    
    // 初始化現實管理器
    await this.realityManager.initialize();
    
    this.initialized = true;
    console.log('[Fabric Storage] Storage initialized successfully');
  }
  
  // ========================================================================
  // Superposition Operations
  // ========================================================================
  
  async storeSuperposition(node: FabricNode): Promise<void> {
    if (!this.config.enableSuperposition) {
      throw new Error('Superposition storage is disabled');
    }
    
    console.log(`[Fabric Storage] Storing superposition for node ${node.id}`);
    
    // 壓縮疊加態
    const compressed = await this.compressionEngine.compress(node.superposition, node.id);
    
    // 儲存壓縮後的疊加態
    await this.storageEngine.store(node.id, compressed);
    
    console.log(`[Fabric Storage] Superposition stored, compression ratio: ${compressed.compressionRatio}`);
  }
  
  async retrieveSuperposition(nodeId: string): Promise<SuperpositionState | undefined> {
    if (!this.config.enableSuperposition) {
      throw new Error('Superposition storage is disabled');
    }
    
    console.log(`[Fabric Storage] Retrieving superposition for node ${nodeId}`);
    
    // 檢索壓縮的疊加態
    const compressed = await this.storageEngine.retrieve(nodeId);
    
    if (!compressed) {
      return undefined;
    }
    
    // 解壓縮疊加態
    const superposition = await this.compressionEngine.decompress(compressed);
    
    console.log(`[Fabric Storage] Superposition retrieved`);
    return superposition;
  }
  
  async expandSuperposition(nodeId: string, options: {
    version?: string;
    semanticType?: string;
    realityId?: string;
  }): Promise<FabricNode | undefined> {
    console.log(`[Fabric Storage] Expanding superposition for node ${nodeId}`);
    
    // 檢索疊加態
    const superposition = await this.retrieveSuperposition(nodeId);
    
    if (!superposition) {
      return undefined;
    }
    
    // 應用展開選項
    let expanded = { ...superposition };
    
    if (options.version) {
      // 展開特定版本
      expanded.versions = expanded.versions.filter(v => v.version === options.version);
    }
    
    if (options.semanticType) {
      // 展開特定語意類型
      expanded.semantics = expanded.semantics.filter(s => s.semanticType === options.semanticType);
    }
    
    if (options.realityId) {
      // 展開特定現實
      expanded.realities = expanded.realities.filter(r => r.realityId === options.realityId);
    }
    
    // 建構節點
    const node: FabricNode = {
      id: nodeId,
      type: 'file', // 預設類型，實際應從元資料讀取
      layer: 'fabric',
      properties: {},
      superposition: expanded,
      version: expanded.versions[0]?.version || '1.0.0',
      realityId: expanded.realities[0]?.realityId || 'default',
      timestamp: Date.now(),
      projections: []
    };
    
    console.log(`[Fabric Storage] Superposition expanded`);
    return node;
  }
  
  async collapseSuperposition(nodeId: string, options: {
    targetVersion?: string;
    targetSemantic?: string;
    targetReality?: string;
    dominanceStrategy?: 'latest' | 'highest_confidence' | 'most_used';
  }): Promise<SuperpositionState> {
    console.log(`[Fabric Storage] Collapsing superposition for node ${nodeId}`);
    
    // 檢索疊加態
    const superposition = await this.retrieveSuperposition(nodeId);
    
    if (!superposition) {
      throw new Error(`Superposition not found for node ${nodeId}`);
    }
    
    let collapsed = { ...superposition };
    
    // 版本坍縮
    if (options.targetVersion) {
      collapsed.versions = collapsed.versions.filter(v => v.version === options.targetVersion);
    } else if (options.dominanceStrategy === 'latest') {
      collapsed.versions = [collapsed.versions[collapsed.versions.length - 1]];
    }
    
    // 語意坍縮
    if (options.targetSemantic) {
      collapsed.semantics = collapsed.semantics.filter(s => s.semanticType === options.targetSemantic);
    } else if (options.dominanceStrategy === 'highest_confidence') {
      const highest = collapsed.semantics.reduce((a, b) => 
        a.confidence > b.confidence ? a : b
      );
      collapsed.semantics = [highest];
    }
    
    // 現實坍縮
    if (options.targetReality) {
      collapsed.realities = collapsed.realities.filter(r => r.realityId === options.targetReality);
    } else if (options.dominanceStrategy === 'most_used') {
      // 使用預設現實
      const defaultReality = collapsed.realities.find(r => r.realityId === 'default');
      collapsed.realities = defaultReality ? [defaultReality] : collapsed.realities.slice(0, 1);
    }
    
    // 更新主導變體
    collapsed.dominance = collapsed.versions[0]?.id || 'default';
    collapsed.coherence = 1.0; // 坍縮後一致性為 1.0
    
    console.log(`[Fabric Storage] Superposition collapsed`);
    return collapsed;
  }
  
  async mergeSuperpositions(nodeIds: string[], options: {
    mergeStrategy?: 'union' | 'intersection' | 'weighted';
  }): Promise<SuperpositionState> {
    console.log(`[Fabric Storage] Merging superpositions for ${nodeIds.length} nodes`);
    
    // 檢索所有疊加態
    const superpositions = await Promise.all(
      nodeIds.map(id => this.retrieveSuperposition(id))
    );
    
    const validSuperpositions = superpositions.filter(s => s !== undefined) as SuperpositionState[];
    
    if (validSuperpositions.length === 0) {
      throw new Error('No valid superpositions found');
    }
    
    let merged: SuperpositionState;
    
    switch (options.mergeStrategy) {
      case 'union':
        merged = await this.mergeUnion(validSuperpositions);
        break;
      case 'intersection':
        merged = await this.mergeIntersection(validSuperpositions);
        break;
      case 'weighted':
        merged = await this.mergeWeighted(validSuperpositions);
        break;
      default:
        merged = await this.mergeUnion(validSuperpositions);
    }
    
    console.log(`[Fabric Storage] Superpositions merged`);
    return merged;
  }
  
  private async mergeUnion(superpositions: SuperpositionState[]): Promise<SuperpositionState> {
    // 聯合合併：合併所有版本、語意、現實
    const versions = superpositions.flatMap(s => s.versions);
    const semantics = superpositions.flatMap(s => s.semantics);
    const realities = superpositions.flatMap(s => s.realities);
    
    return {
      versions,
      semantics,
      realities,
      coherence: 0.7, // 聯合合併一致性較低
      dominance: versions[0]?.id || 'default',
      compressionLevel: 0.0
    };
  }
  
  private async mergeIntersection(superpositions: SuperpositionState[]): Promise<SuperpositionState> {
    // 交集合併：只保留共同的版本、語意、現實
    if (superpositions.length === 0) {
      return {
        versions: [],
        semantics: [],
        realities: [],
        coherence: 0.0,
        dominance: 'default',
        compressionLevel: 0.0
      };
    }
    
    const first = superpositions[0];
    
    const versions = first.versions.filter(v1 =>
      superpositions.every(s => s.versions.some(v2 => v2.version === v1.version))
    );
    
    const semantics = first.semantics.filter(s1 =>
      superpositions.every(s => s.semantics.some(s2 => s2.semanticType === s1.semanticType))
    );
    
    const realities = first.realities.filter(r1 =>
      superpositions.every(s => s.realities.some(r2 => r2.realityId === r1.realityId))
    );
    
    return {
      versions,
      semantics,
      realities,
      coherence: 1.0, // 交集合併一致性最高
      dominance: versions[0]?.id || 'default',
      compressionLevel: 0.0
    };
  }
  
  private async mergeWeighted(superpositions: SuperpositionState[]): Promise<SuperpositionState> {
    // 加權合併：基於一致性分數加權
    const totalCoherence = superpositions.reduce((sum, s) => sum + s.coherence, 0);
    
    if (totalCoherence === 0) {
      return await this.mergeUnion(superpositions);
    }
    
    const weightedVersions: NodeVersion[] = [];
    const weightedSemantics: SemanticVariant[] = [];
    const weightedRealities: RealityVariant[] = [];
    
    for (const superposition of superpositions) {
      const weight = superposition.coherence / totalCoherence;
      
      for (const version of superposition.versions) {
        weightedVersions.push({
          ...version,
          metadata: {
            ...version.metadata,
            mergeWeight: weight
          }
        });
      }
      
      for (const semantic of superposition.semantics) {
        weightedSemantics.push({
          ...semantic,
          confidence: semantic.confidence * weight
        });
      }
      
      for (const reality of superposition.realities) {
        weightedRealities.push(reality);
      }
    }
    
    return {
      versions: weightedVersions,
      semantics: weightedSemantics,
      realities: weightedRealities,
      coherence: totalCoherence / superpositions.length,
      dominance: weightedVersions[0]?.id || 'default',
      compressionLevel: 0.0
    };
  }
  
  async splitSuperposition(nodeId: string, criteria: {
    byVersion?: boolean;
    bySemantic?: boolean;
    byReality?: boolean;
  }): Promise<Map<string, SuperpositionState>> {
    console.log(`[Fabric Storage] Splitting superposition for node ${nodeId}`);
    
    const superposition = await this.retrieveSuperposition(nodeId);
    
    if (!superposition) {
      throw new Error(`Superposition not found for node ${nodeId}`);
    }
    
    const splits = new Map<string, SuperpositionState>();
    
    // 按版本分割
    if (criteria.byVersion) {
      for (const version of superposition.versions) {
        splits.set(`version-${version.version}`, {
          versions: [version],
          semantics: superposition.semantics,
          realities: superposition.realities,
          coherence: superposition.coherence,
          dominance: version.id,
          compressionLevel: superposition.compressionLevel
        });
      }
    }
    
    // 按語意分割
    if (criteria.bySemantic) {
      for (const semantic of superposition.semantics) {
        splits.set(`semantic-${semantic.semanticType}`, {
          versions: superposition.versions,
          semantics: [semantic],
          realities: superposition.realities,
          coherence: superposition.coherence,
          dominance: semantic.id,
          compressionLevel: superposition.compressionLevel
        });
      }
    }
    
    // 按現實分割
    if (criteria.byReality) {
      for (const reality of superposition.realities) {
        splits.set(`reality-${reality.realityId}`, {
          versions: superposition.versions,
          semantics: superposition.semantics,
          realities: [reality],
          coherence: superposition.coherence,
          dominance: reality.id,
          compressionLevel: superposition.compressionLevel
        });
      }
    }
    
    console.log(`[Fabric Storage] Superposition split into ${splits.size} parts`);
    return splits;
  }
  
  async alignSuperposition(nodeId: string, targetRealityId: string): Promise<SuperpositionState> {
    console.log(`[Fabric Storage] Aligning superposition for node ${nodeId} to reality ${targetRealityId}`);
    
    const superposition = await this.retrieveSuperposition(nodeId);
    
    if (!superposition) {
      throw new Error(`Superposition not found for node ${nodeId}`);
    }
    
    // 對齊到目標現實
    const aligned = await this.realityManager.alignToReality(superposition, targetRealityId);
    
    // 儲存對齊後的疊加態
    // 注意：這裡需要 Fabric 節點來完成儲存，暫時返回對齊結果
    console.log(`[Fabric Storage] Superposition aligned to reality ${targetRealityId}`);
    return aligned;
  }
  
  async transformSuperposition(nodeId: string, transformation: {
    type: 'version_upgrade' | 'semantic_translation' | 'reality_mapping';
    parameters: any;
  }): Promise<SuperpositionState> {
    console.log(`[Fabric Storage] Transforming superposition for node ${nodeId} with type ${transformation.type}`);
    
    const superposition = await this.retrieveSuperposition(nodeId);
    
    if (!superposition) {
      throw new Error(`Superposition not found for node ${nodeId}`);
    }
    
    let transformed = { ...superposition };
    
    switch (transformation.type) {
      case 'version_upgrade':
        transformed = await this.transformVersionUpgrade(transformed, transformation.parameters);
        break;
      case 'semantic_translation':
        transformed = await this.transformSemanticTranslation(transformed, transformation.parameters);
        break;
      case 'reality_mapping':
        transformed = await this.transformRealityMapping(transformed, transformation.parameters);
        break;
      default:
        throw new Error(`Unknown transformation type: ${transformation.type}`);
    }
    
    console.log(`[Fabric Storage] Superposition transformed`);
    return transformed;
  }
  
  private async transformVersionUpgrade(superposition: SuperpositionState, params: any): Promise<SuperpositionState> {
    // 版本升級：為所有版本添加新版本
    const newVersion = {
      id: `${superposition.dominance}-v${Date.now()}`,
      version: params.newVersion || '2.0.0',
      timestamp: Date.now(),
      author: params.author || 'system',
      content: params.content || {},
      metadata: params.metadata || {}
    };
    
    return {
      ...superposition,
      versions: [...superposition.versions, newVersion],
      dominance: newVersion.id
    };
  }
  
  private async transformSemanticTranslation(superposition: SuperpositionState, params: any): Promise<SuperpositionState> {
    // 語意翻譯：翻譯所有語意到目標語意類型
    const translatedSemantics = superposition.semantics.map(s => ({
      ...s,
      semanticType: params.targetSemanticType || s.semanticType,
      meaning: params.translationFunction ? params.translationFunction(s.meaning) : s.meaning
    }));
    
    return {
      ...superposition,
      semantics: translatedSemantics
    };
  }
  
  private async transformRealityMapping(superposition: SuperpositionState, params: any): Promise<SuperpositionState> {
    // 現實映射：映射所有現實到目標現實
    const mappedRealities = superposition.realities.map(r => ({
      ...r,
      realityId: params.targetRealityId || r.realityId,
      abstraction: params.mappingFunction ? params.mappingFunction(r.abstraction) : r.abstraction
    }));
    
    return {
      ...superposition,
      realities: mappedRealities
    };
  }
  
  // ========================================================================
  // Version Operations
  // ========================================================================
  
  async addVersion(nodeId: string, version: NodeVersion): Promise<void> {
    if (!this.config.enableVersioning) {
      throw new Error('Versioning is disabled');
    }
    
    console.log(`[Fabric Storage] Adding version ${version.version} to node ${nodeId}`);
    
    await this.versionManager.addVersion(nodeId, version);
    
    // 清理舊版本
    await this.versionManager.cleanupOldVersions(nodeId, this.config.maxVersions);
  }
  
  async getVersion(nodeId: string, version: string): Promise<NodeVersion | undefined> {
    return await this.versionManager.getVersion(nodeId, version);
  }
  
  async getVersionHistory(nodeId: string): Promise<NodeVersion[]> {
    return await this.versionManager.getVersionHistory(nodeId);
  }
  
  async rollbackVersion(nodeId: string, version: string): Promise<void> {
    console.log(`[Fabric Storage] Rolling back node ${nodeId} to version ${version}`);
    
    await this.versionManager.rollbackVersion(nodeId, version);
  }
  
  // ========================================================================
  // Reality Operations
  // ========================================================================
  
  async addRealityMapping(nodeId: string, reality: RealityVariant): Promise<void> {
    console.log(`[Fabric Storage] Adding reality mapping ${reality.realityId} to node ${nodeId}`);
    
    await this.realityManager.addRealityMapping(nodeId, reality);
  }
  
  async getRealityMapping(nodeId: string, realityId: string): Promise<RealityVariant | undefined> {
    return await this.realityManager.getRealityMapping(nodeId, realityId);
  }
  
  async getAllRealities(nodeId: string): Promise<RealityVariant[]> {
    return await this.realityManager.getAllRealities(nodeId);
  }
  
  // ========================================================================
  // Query Operations
  // ========================================================================
  
  async querySuperpositions(query: SuperpositionQuery): Promise<SuperpositionState[]> {
    console.log(`[Fabric Storage] Querying superpositions...`);
    
    // 從儲存引擎查詢
    const results = await this.storageEngine.query(query);
    
    // 解壓縮結果
    const superpositions = await Promise.all(
      results.map(compressed => this.compressionEngine.decompress(compressed))
    );
    
    console.log(`[Fabric Storage] Found ${superpositions.length} superpositions`);
    return superpositions.filter(s => s !== undefined) as SuperpositionState[];
  }
  
  // ========================================================================
  // Statistics and Monitoring
  // ========================================================================
  
  async getStatistics(): Promise<StorageStatistics> {
    return {
      totalSuperpositions: await this.storageEngine.count(),
      totalVersions: await this.versionManager.countVersions(),
      totalRealities: await this.realityManager.countRealities(),
      averageCompressionRatio: await this.compressionEngine.getAverageCompressionRatio(),
      storageSize: await this.storageEngine.getStorageSize(),
      compressionSavings: await this.compressionEngine.getCompressionSavings()
    };
  }
  
  // ========================================================================
  // Cleanup and Maintenance
  // ========================================================================
  
  async cleanup(): Promise<void> {
    console.log('[Fabric Storage] Starting cleanup...');
    
    // 清理過期版本
    await this.versionManager.cleanupExpiredVersions(this.config.retentionDays);
    
    // 清理孤立資料
    await this.storageEngine.cleanupOrphans();
    
    // 壓縮儲存
    await this.storageEngine.compact();
    
    console.log('[Fabric Storage] Cleanup complete');
  }
  
  isInitialized(): boolean {
    return this.initialized;
  }
}

// ============================================================================
// Storage Engine
// ============================================================================

class StorageEngine {
  constructor(private config: StorageConfig) {}
  
  async initialize(): Promise<void> {
    const fs = require('fs');
    const path = require('path');
    
    // 正規化並建立儲存目錄
    const basePathResolved = path.resolve(this.config.basePath);
    
    if (!fs.existsSync(basePathResolved)) {
      fs.mkdirSync(basePathResolved, { recursive: true });
    }
    
    // 將正規化後的路徑回寫設定，後續統一使用
    this.config.basePath = basePathResolved;
  }
  
  async store(nodeId: string, compressed: CompressedSuperposition): Promise<void> {
    const fs = require('fs');
    const path = require('path');
    
    // 使用正規化後的根目錄，並確保目標路徑不會逃離根目錄
    const basePathResolved = path.resolve(this.config.basePath);
    const candidatePath = path.resolve(basePathResolved, `${nodeId}.json`);
    
    if (!(candidatePath === basePathResolved || candidatePath.startsWith(basePathResolved + path.sep))) {
      throw new Error(`Invalid nodeId for storage path: ${nodeId}`);
    }
    
    const filePath = candidatePath;
    const content = JSON.stringify(compressed, null, 2);
    
    fs.writeFileSync(filePath, content, 'utf-8');
  }
  
  async retrieve(nodeId: string): Promise<CompressedSuperposition | undefined> {
    const fs = require('fs');
    const path = require('path');
    
    // 使用與 store 相同的安全路徑解析邏輯
    const basePathResolved = path.resolve(this.config.basePath);
    const candidatePath = path.resolve(basePathResolved, `${nodeId}.json`);
    if (!(candidatePath === basePathResolved || candidatePath.startsWith(basePathResolved + path.sep))) {
      throw new Error(`Invalid nodeId for storage path: ${nodeId}`);
    }
    
    const filePath = candidatePath;
    
    
    if (!fs.existsSync(filePath)) {
      return undefined;
    }
    
    const content = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(content);
  }
  
  async query(query: SuperpositionQuery): Promise<CompressedSuperposition[]> {
    const fs = require('fs');
    const path = require('path');
    
    const results: CompressedSuperposition[] = [];
    
    // 讀取目錄中所有文件
    const files = fs.readdirSync(this.config.basePath);
    
    for (const file of files) {
      if (!file.endsWith('.json')) {
        continue;
      }
      
      const nodeId = file.replace('.json', '');
      
      // 檢查節點 ID 是否匹配
      if (query.nodeId && nodeId !== query.nodeId) {
        continue;
      }
      
      const compressed = await this.retrieve(nodeId);
      if (compressed) {
        // 檢查時間範圍
        if (query.since && compressed.timestamp < query.since) {
          continue;
        }
        if (query.until && compressed.timestamp > query.until) {
          continue;
        }
        
        results.push(compressed);
      }
    }
    
    return results;
  }
  
  async count(): Promise<number> {
    const fs = require('fs');
    const files = fs.readdirSync(this.config.basePath);
    return files.filter((f: string) => f.endsWith('.json')).length;
  }
  
  async getStorageSize(): Promise<number> {
    const fs = require('fs');
    const path = require('path');
    
    let totalSize = 0;
    const files = fs.readdirSync(this.config.basePath);
    
    for (const file of files) {
      const filePath = path.join(this.config.basePath, file);
      const stats = fs.statSync(filePath);
      totalSize += stats.size;
    }
    
    return totalSize;
  }
  
  async cleanupOrphans(): Promise<void> {
    // 清理沒有對應節點的疊加態檔案
    // 需要與 Fabric Core 協作
  }
  
  async compact(): Promise<void> {
    // 壓縮儲存空間
    console.log('[Storage Engine] Compacting storage...');
  }
}

// ============================================================================
// Superposition Compression Engine
// ============================================================================

class SuperpositionCompressionEngine {
  private compressionStats: CompressionStatistics;
  
  constructor(private config: StorageConfig) {
    this.compressionStats = {
      totalCompressed: 0,
      totalDecompressed: 0,
      averageCompressionRatio: 0.0
    };
  }
  
  async initialize(): Promise<void> {
    console.log('[Compression Engine] Initializing...');
  }
  
  async compress(superposition: SuperpositionState, nodeId: string): Promise<CompressedSuperposition> {
    console.log(`[Compression Engine] Compressing superposition for node ${nodeId}`);
    
    const startTime = Date.now();
    
    // 壓縮版本（使用增量壓縮）
    const compressedVersions = this.compressVersions(superposition.versions);
    
    // 壓縮語意
    const compressedSemantics = this.compressSemantics(superposition.semantics);
    
    // 壓縮現實
    const compressedRealities = this.compressRealities(superposition.realities);
    
    // 計算壓縮比
    const originalSize = JSON.stringify(superposition).length;
    const compressedSize = JSON.stringify({
      compressedVersions,
      compressedSemantics,
      compressedRealities
    }).length;
    const compressionRatio = compressedSize / originalSize;
    
    const compressed: CompressedSuperposition = {
      nodeId,
      compressedVersions,
      compressedSemantics,
      compressedRealities,
      compressionRatio,
      compressionMethod: 'delta-encoding',
      checksum: this.calculateChecksum(superposition),
      timestamp: Date.now()
    };
    
    // 更新統計
    this.compressionStats.totalCompressed++;
    this.compressionStats.averageCompressionRatio = 
      (this.compressionStats.averageCompressionRatio * (this.compressionStats.totalCompressed - 1) + compressionRatio) / 
      this.compressionStats.totalCompressed;
    
    console.log(`[Compression Engine] Compression complete, ratio: ${compressionRatio.toFixed(3)}`);
    return compressed;
  }
  
  private compressVersions(versions: NodeVersion[]): CompressedVersion[] {
    if (versions.length === 0) {
      return [];
    }
    
    // 第一個版本保存完整內容
    const compressed: CompressedVersion[] = [{
      id: versions[0].id,
      version: versions[0].version,
      delta: versions[0].content, // 第一個版本保存完整內容
      timestamp: versions[0].timestamp,
      size: JSON.stringify(versions[0].content).length
    }];
    
    // 後續版本只保存增量
    for (let i = 1; i < versions.length; i++) {
      const delta = this.calculateDelta(versions[i - 1].content, versions[i].content);
      
      compressed.push({
        id: versions[i].id,
        version: versions[i].version,
        delta,
        timestamp: versions[i].timestamp,
        size: JSON.stringify(delta).length
      });
    }
    
    return compressed;
  }
  
  private compressSemantics(semantics: SemanticVariant[]): CompressedSemantic[] {
    return semantics.map(s => ({
      id: s.id,
      semanticType: s.semanticType,
      confidence: s.confidence,
      compressedMeaning: this.compressData(s.meaning),
      timestamp: Date.now(),
      size: JSON.stringify(this.compressData(s.meaning)).length
    }));
  }
  
  private compressRealities(realities: RealityVariant[]): CompressedReality[] {
    return realities.map(r => ({
      id: r.id,
      realityId: r.realityId,
      compressedAbstraction: this.compressData(r.abstraction),
      timestamp: Date.now(),
      size: JSON.stringify(this.compressData(r.abstraction)).length
    }));
  }
  
  private compressData(data: any): any {
    // 簡化實作：實際可使用更複雜的壓縮算法
    if (typeof data === 'object' && data !== null) {
      const compressed: any = {};
      for (const [key, value] of Object.entries(data)) {
        if (typeof value === 'string' && value.length > 100) {
          // 長字串壓縮
          compressed[key] = {
            type: 'compressed',
            originalLength: value.length,
            data: value.substring(0, 50) + '...' + value.substring(value.length - 50)
          };
        } else {
          compressed[key] = value;
        }
      }
      return compressed;
    }
    return data;
  }
  
  private calculateDelta(prev: any, current: any): any {
    // 計算兩個對象之間的差異
    const delta: any = {};
    
    for (const [key, value] of Object.entries(current)) {
      if (prev[key] !== value) {
        delta[key] = value;
      }
    }
    
    return delta;
  }
  
  private calculateChecksum(data: any): string {
    // 簡化實作：使用內容長度作為校驗和
    return JSON.stringify(data).length.toString();
  }
  
  async decompress(compressed: CompressedSuperposition): Promise<SuperpositionState> {
    console.log(`[Compression Engine] Decompressing superposition for node ${compressed.nodeId}`);
    
    // 解壓縮版本
    const versions = this.decompressVersions(compressed.compressedVersions);
    
    // 解壓縮語意
    const semantics = this.decompressSemantics(compressed.compressedSemantics);
    
    // 解壓縮現實
    const realities = this.decompressRealities(compressed.compressedRealities);
    
    const superposition: SuperpositionState = {
      versions,
      semantics,
      realities,
      coherence: 1.0,
      dominance: versions[0]?.id || 'default',
      compressionLevel: compressed.compressionRatio
    };
    
    // 更新統計
    this.compressionStats.totalDecompressed++;
    
    console.log(`[Compression Engine] Decompression complete`);
    return superposition;
  }
  
  private decompressVersions(compressed: CompressedVersion[]): NodeVersion[] {
    if (compressed.length === 0) {
      return [];
    }
    
    const versions: NodeVersion[] = [];
    
    // 第一個版本直接還原
    versions.push({
      id: compressed[0].id,
      version: compressed[0].version,
      timestamp: compressed[0].timestamp,
      author: 'system', // 從元資料中讀取
      content: compressed[0].delta,
      metadata: {}
    });
    
    // 後續版本應用增量
    for (let i = 1; i < compressed.length; i++) {
      const prevContent = versions[i - 1].content;
      const currentContent = this.applyDelta(prevContent, compressed[i].delta);
      
      versions.push({
        id: compressed[i].id,
        version: compressed[i].version,
        timestamp: compressed[i].timestamp,
        author: 'system',
        content: currentContent,
        metadata: {}
      });
    }
    
    return versions;
  }
  
  private decompressSemantics(compressed: CompressedSemantic[]): SemanticVariant[] {
    return compressed.map(s => ({
      id: s.id,
      semanticType: s.semanticType,
      confidence: s.confidence,
      meaning: this.decompressData(s.compressedMeaning),
      context: {}
    }));
  }
  
  private decompressRealities(compressed: CompressedReality[]): RealityVariant[] {
    return compressed.map(r => ({
      id: r.id,
      realityId: r.realityId,
      abstraction: this.decompressData(r.compressedAbstraction),
      mappings: []
    }));
  }
  
  private decompressData(data: any): any {
    // 簡化實作：實際應解壓縮數據
    if (typeof data === 'object' && data !== null) {
      if (data.type === 'compressed') {
        // 返回標記為壓縮的數據
        return {
          _compressed: true,
          originalLength: data.originalLength,
          data: data.data
        };
      }
    }
    return data;
  }
  
  private applyDelta(base: any, delta: any): any {
    // 應用增量到基礎對象
    const result = JSON.parse(JSON.stringify(base));
    
    for (const [key, value] of Object.entries(delta)) {
      result[key] = value;
    }
    
    return result;
  }
  
  async getAverageCompressionRatio(): Promise<number> {
    return this.compressionStats.averageCompressionRatio;
  }
  
  async getCompressionSavings(): Promise<number> {
    const totalCompressed = this.compressionStats.totalCompressed;
    const avgRatio = this.compressionStats.averageCompressionRatio;
    
    if (totalCompressed === 0) {
      return 0;
    }
    
    // 節省 = (1 - 壓縮比) * 100%
    return (1 - avgRatio) * 100;
  }
}

// ============================================================================
// Version Manager
// ============================================================================

class VersionManager {
  private versions: Map<string, NodeVersion[]>;
  
  constructor(private config: StorageConfig) {
    this.versions = new Map();
  }
  
  async initialize(): Promise<void> {
    console.log('[Version Manager] Initializing...');
  }
  
  async addVersion(nodeId: string, version: NodeVersion): Promise<void> {
    if (!this.versions.has(nodeId)) {
      this.versions.set(nodeId, []);
    }
    
    const nodeVersions = this.versions.get(nodeId)!;
    nodeVersions.push(version);
    
    // 按時間戳排序
    nodeVersions.sort((a, b) => a.timestamp - b.timestamp);
  }
  
  async getVersion(nodeId: string, version: string): Promise<NodeVersion | undefined> {
    const nodeVersions = this.versions.get(nodeId);
    
    if (!nodeVersions) {
      return undefined;
    }
    
    return nodeVersions.find(v => v.version === version);
  }
  
  async getVersionHistory(nodeId: string): Promise<NodeVersion[]> {
    return this.versions.get(nodeId) || [];
  }
  
  async rollbackVersion(nodeId: string, version: string): Promise<void> {
    const nodeVersions = this.versions.get(nodeId);
    
    if (!nodeVersions) {
      throw new Error(`No versions found for node ${nodeId}`);
    }
    
    const targetVersion = nodeVersions.find(v => v.version === version);
    
    if (!targetVersion) {
      throw new Error(`Version ${version} not found for node ${nodeId}`);
    }
    
    // 創建新版本，內容與目標版本相同
    const newVersion: NodeVersion = {
      id: `${nodeId}-v${Date.now()}`,
      version: `${version}-rollback`,
      timestamp: Date.now(),
      author: 'rollback',
      content: targetVersion.content,
      metadata: {
        ...targetVersion.metadata,
        rollbackFrom: targetVersion.version
      }
    };
    
    await this.addVersion(nodeId, newVersion);
  }
  
  async cleanupOldVersions(nodeId: string, maxVersions: number): Promise<void> {
    const nodeVersions = this.versions.get(nodeId);
    
    if (!nodeVersions || nodeVersions.length <= maxVersions) {
      return;
    }
    
    // 保留最新的 maxVersions 個版本
    const versionsToKeep = nodeVersions.slice(-maxVersions);
    this.versions.set(nodeId, versionsToKeep);
  }
  
  async cleanupExpiredVersions(retentionDays: number): Promise<void> {
    const cutoffTime = Date.now() - (retentionDays * 24 * 60 * 60 * 1000);
    
    for (const [nodeId, nodeVersions] of this.versions) {
      const validVersions = nodeVersions.filter(v => v.timestamp > cutoffTime);
      this.versions.set(nodeId, validVersions);
    }
  }
  
  async countVersions(): Promise<number> {
    let total = 0;
    
    for (const versions of this.versions.values()) {
      total += versions.length;
    }
    
    return total;
  }
}

// ============================================================================
// Reality Manager
// ============================================================================

class RealityManager {
  private realities: Map<string, RealityVariant[]>;
  
  constructor(private config: StorageConfig) {
    this.realities = new Map();
  }
  
  async initialize(): Promise<void> {
    console.log('[Reality Manager] Initializing...');
  }
  
  async addRealityMapping(nodeId: string, reality: RealityVariant): Promise<void> {
    if (!this.realities.has(nodeId)) {
      this.realities.set(nodeId, []);
    }
    
    const nodeRealities = this.realities.get(nodeId)!;
    nodeRealities.push(reality);
  }
  
  async getRealityMapping(nodeId: string, realityId: string): Promise<RealityVariant | undefined> {
    const nodeRealities = this.realities.get(nodeId);
    
    if (!nodeRealities) {
      return undefined;
    }
    
    return nodeRealities.find(r => r.realityId === realityId);
  }
  
  async getAllRealities(nodeId: string): Promise<RealityVariant[]> {
    return this.realities.get(nodeId) || [];
  }
  
  async alignToReality(superposition: SuperpositionState, targetRealityId: string): Promise<SuperpositionState> {
    // 對齊到目標現實
    const alignedRealities = superposition.realities.map(r => {
      if (r.realityId === targetRealityId) {
        return r;
      }
      
      // 創建到目標現實的映射
      return {
        ...r,
        mappings: [
          ...r.mappings,
          {
            targetReality: targetRealityId,
            mappingRule: { type: 'identity' },
            transformation: r.abstraction
          }
        ]
      };
    });
    
    return {
      ...superposition,
      realities: alignedRealities
    };
  }
  
  async countRealities(): Promise<number> {
    let total = 0;
    
    for (const realities of this.realities.values()) {
      total += realities.length;
    }
    
    return total;
  }
}

// ============================================================================
// Type Definitions
// ============================================================================

export interface StorageStatistics {
  totalSuperpositions: number;
  totalVersions: number;
  totalRealities: number;
  averageCompressionRatio: number;
  storageSize: number;
  compressionSavings: number;
}

export interface CompressionStatistics {
  totalCompressed: number;
  totalDecompressed: number;
  averageCompressionRatio: number;
}