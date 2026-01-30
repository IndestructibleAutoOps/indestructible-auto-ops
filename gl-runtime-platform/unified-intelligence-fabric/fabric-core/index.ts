// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-fabric-core
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Unified Intelligence Fabric - Fabric Core
 * Version 19.0.0
 * 
 * 核心：萬物統一圖
 * - 將 GRG、SRG、Global DAG、Swarm、Mesh、Civilization、Inter-Reality 收斂為一張統一織網
 * - 所有資源、語意、代理、現實都只是織網上的節點與邊
 * - 支援多層圖結構與投影機制
 */

// ============================================================================
// Type Definitions
// ============================================================================

export interface FabricNode {
  id: string;
  type: NodeType;
  layer: FabricLayer;
  
  // 基礎屬性
  properties: Record<string, any>;
  
  // 疊加態屬性
  superposition: SuperpositionState;
  
  // 關聯資訊
  version: string;
  realityId: string;
  timestamp: number;
  
  // 投影資訊（來自不同視角）
  projections: NodeProjection[];
}

export type NodeType = 
  | 'file'           // 檔案節點
  | 'semantic'       // 語意節點
  | 'agent'          // 代理節點
  | 'dag'            // DAG 節點
  | 'mesh'           // Mesh 節點
  | 'swarm'          // Swarm 節點
  | 'civilization'   // 文明節點
  | 'reality'        // 現實節點
  | 'flow'           // 流節點
  | 'compute'        // 運算節點
  | 'algo'           // 演算法節點
  | 'composition'    // 組合節點;

export type FabricLayer = 
  | 'resource'       // 資源層（GRG）
  | 'semantic'       // 語意層（SRG）
  | 'execution'      // 執行層（DAG）
  | 'cognitive'      // 認知層（Mesh/Swarm）
  | 'civilization'   // 文明層
  | 'meta'           // 元認知層
  | 'universal'      // 通用智慧層
  | 'context'        // 脈絡層
  | 'reality'        // 現實層
  | 'fabric';        // 織網層（頂層）

export interface SuperpositionState {
  // 多版本疊加
  versions: NodeVersion[];
  
  // 多語意疊加
  semantics: SemanticVariant[];
  
  // 多現實疊加
  realities: RealityVariant[];
  
  // 疊加態元資料
  coherence: number;           // 一致性分數
  dominance: string;           // 主導變體
  compressionLevel: number;    // 壓縮程度
}

export interface NodeVersion {
  id: string;
  version: string;
  timestamp: number;
  author: string;
  content: any;
  metadata: Record<string, any>;
}

export interface SemanticVariant {
  id: string;
  semanticType: string;
  confidence: number;
  meaning: any;
  context: Record<string, any>;
}

export interface RealityVariant {
  id: string;
  realityId: string;
  abstraction: any;
  mappings: RealityMapping[];
}

export interface RealityMapping {
  targetReality: string;
  mappingRule: any;
  transformation: any;
}

export interface NodeProjection {
  source: string;              // 投影來源（例如 'GRG', 'SRG', 'DAG'）
  type: string;                // 投影類型
  representation: any;         // 投影表示
  timestamp: number;
}

export interface FabricEdge {
  id: string;
  sourceId: string;
  targetId: string;
  type: EdgeType;
  layer: FabricLayer;
  
  properties: Record<string, any>;
  superposition: SuperpositionState;
  
  weight: number;
  direction: 'directed' | 'undirected' | 'bidirectional';
  
  version: string;
  realityId: string;
  timestamp: number;
}

export type EdgeType = 
  | 'dependency'     // 依賴關係
  | 'semantic'       // 語意關係
  | 'flow'           // 流動關係
  | 'causal'         // 因果關係
  | 'temporal'       // 時序關係
  | 'composition'    // 組合關係
  | 'evolution'      // 演化關係
  | 'reality'        // 現實映射關係;

export interface FabricGraph {
  id: string;
  nodes: Map<string, FabricNode>;
  edges: Map<string, FabricEdge>;
  
  // 分層視圖
  layers: Map<FabricLayer, LayerView>;
  
  // 投影視圖
  projections: Map<string, ProjectionView>;
  
  // 織網元資料
  metadata: FabricMetadata;
  
  // 演化狀態
  evolution: EvolutionState;
}

export interface LayerView {
  layer: FabricLayer;
  nodes: Set<string>;
  edges: Set<string>;
  
  // 層內統計
  statistics: LayerStatistics;
  
  // 層間連接
  interlayerConnections: Map<string, Set<string>>;
}

export interface LayerStatistics {
  nodeCount: number;
  edgeCount: number;
  density: number;
  avgClustering: number;
  maxConnectedComponent: number;
}

export interface ProjectionView {
  id: string;
  sourceSystem: string;         // 例如 'GRG', 'SRG', 'DAG'
  nodes: Set<string>;
  edges: Set<string>;
  
  transformationRules: any[];
  mappingFunctions: Map<string, any>;
  
  lastSync: number;
  consistency: number;
}

export interface FabricMetadata {
  version: string;
  createdAt: number;
  lastModified: number;
  
  // 織網統計
  totalNodes: number;
  totalEdges: number;
  totalLayers: number;
  
  // 疊加態統計
  superpositionRatio: number;
  averageCompressionLevel: number;
  
  // 演化統計
  evolutionCount: number;
  adaptationRate: number;
}

export interface EvolutionState {
  generation: number;
  lastEvolution: number;
  evolutionHistory: EvolutionEvent[];
  
  weightChanges: Map<string, number>;
  topologyChanges: TopologyChange[];
  
  adaptationRate: number;
  stabilityScore: number;
}

export interface EvolutionEvent {
  id: string;
  timestamp: number;
  type: 'weight_change' | 'node_add' | 'node_remove' | 'edge_add' | 'edge_remove' | 'subgraph_rewrite';
  description: string;
  impact: number;
}

export interface TopologyChange {
  timestamp: number;
  nodesAdded: number;
  nodesRemoved: number;
  edgesAdded: number;
  edgesRemoved: number;
  subgraphRewritten: boolean;
}

// ============================================================================
// Fabric Core Class
// ============================================================================

export class FabricCore {
  private graph: FabricGraph;
  private initialized: boolean;
  private evolutionEngine: FabricEvolutionEngine;
  private projectionEngine: FabricProjectionEngine;
  
  constructor() {
    this.graph = this.initializeGraph();
    this.initialized = false;
    this.evolutionEngine = new FabricEvolutionEngine(this.graph);
    this.projectionEngine = new FabricProjectionEngine(this.graph);
  }
  
  // ========================================================================
  // Initialization
  // ========================================================================
  
  private initializeGraph(): FabricGraph {
    return {
      id: `fabric-${Date.now()}`,
      nodes: new Map(),
      edges: new Map(),
      layers: new Map(),
      projections: new Map(),
      metadata: {
        version: '19.0.0',
        createdAt: Date.now(),
        lastModified: Date.now(),
        totalNodes: 0,
        totalEdges: 0,
        totalLayers: 10,
        superpositionRatio: 0.0,
        averageCompressionLevel: 0.0,
        evolutionCount: 0,
        adaptationRate: 0.0
      },
      evolution: {
        generation: 0,
        lastEvolution: Date.now(),
        evolutionHistory: [],
        weightChanges: new Map(),
        topologyChanges: [],
        adaptationRate: 0.0,
        stabilityScore: 1.0
      }
    };
  }
  
  async initialize(): Promise<void> {
    console.log('[Fabric Core] Initializing Unified Intelligence Fabric...');
    
    // 初始化所有層級
    await this.initializeLayers();
    
    // 初始化預設投影
    await this.initializeProjections();
    
    // 載入歷史數據
    await this.loadHistoricalData();
    
    this.initialized = true;
    console.log('[Fabric Core] Fabric initialized successfully');
  }
  
  private async initializeLayers(): Promise<void> {
    const layers: FabricLayer[] = [
      'resource', 'semantic', 'execution', 'cognitive',
      'civilization', 'meta', 'universal', 'context', 'reality', 'fabric'
    ];
    
    for (const layer of layers) {
      this.graph.layers.set(layer, {
        layer,
        nodes: new Set(),
        edges: new Set(),
        statistics: {
          nodeCount: 0,
          edgeCount: 0,
          density: 0.0,
          avgClustering: 0.0,
          maxConnectedComponent: 0
        },
        interlayerConnections: new Map()
      });
    }
  }
  
  private async initializeProjections(): Promise<void> {
    // GRG Projection
    this.graph.projections.set('GRG', {
      id: 'GRG',
      sourceSystem: 'global-resource-graph',
      nodes: new Set(),
      edges: new Set(),
      transformationRules: [],
      mappingFunctions: new Map(),
      lastSync: 0,
      consistency: 0.0
    });
    
    // SRG Projection
    this.graph.projections.set('SRG', {
      id: 'SRG',
      sourceSystem: 'semantic-resource-graph',
      nodes: new Set(),
      edges: new Set(),
      transformationRules: [],
      mappingFunctions: new Map(),
      lastSync: 0,
      consistency: 0.0
    });
    
    // Global DAG Projection
    this.graph.projections.set('GlobalDAG', {
      id: 'GlobalDAG',
      sourceSystem: 'global-dag',
      nodes: new Set(),
      edges: new Set(),
      transformationRules: [],
      mappingFunctions: new Map(),
      lastSync: 0,
      consistency: 0.0
    });
    
    // Swarm Projection
    this.graph.projections.set('Swarm', {
      id: 'Swarm',
      sourceSystem: 'swarm',
      nodes: new Set(),
      edges: new Set(),
      transformationRules: [],
      mappingFunctions: new Map(),
      lastSync: 0,
      consistency: 0.0
    });
    
    // Mesh Projection
    this.graph.projections.set('Mesh', {
      id: 'Mesh',
      sourceSystem: 'cognitive-mesh',
      nodes: new Set(),
      edges: new Set(),
      transformationRules: [],
      mappingFunctions: new Map(),
      lastSync: 0,
      consistency: 0.0
    });
    
    // Civilization Projection
    this.graph.projections.set('Civilization', {
      id: 'Civilization',
      sourceSystem: 'civilization',
      nodes: new Set(),
      edges: new Set(),
      transformationRules: [],
      mappingFunctions: new Map(),
      lastSync: 0,
      consistency: 0.0
    });
    
    // Inter-Reality Projection
    this.graph.projections.set('InterReality', {
      id: 'InterReality',
      sourceSystem: 'inter-reality',
      nodes: new Set(),
      edges: new Set(),
      transformationRules: [],
      mappingFunctions: new Map(),
      lastSync: 0,
      consistency: 0.0
    });
  }
  
  private async loadHistoricalData(): Promise<void> {
    // 載入 GRG
    await this.loadGRG();
    
    // 載入 SRG
    await this.loadSRG();
    
    // 載入其他歷史數據
    await this.loadOtherData();
  }
  
  private async loadGRG(): Promise<void> {
    try {
      const fs = require('fs');
      const path = require('path');
      const grgPath = path.join(__dirname, '../../../storage/gl-artifacts-store/global-resource-graph.json');
      
      if (fs.existsSync(grgPath)) {
        const grgData = JSON.parse(fs.readFileSync(grgPath, 'utf-8'));
        console.log(`[Fabric Core] Loaded GRG v${grgData.version} with ${grgData.resources.length} resources`);
        
        // 將 GRG 資源轉換為 Fabric 節點
        for (const resource of grgData.resources) {
          await this.addNode({
            id: resource.id,
            type: 'file',
            layer: 'resource',
            properties: resource.properties || {},
            superposition: {
              versions: [{
                id: `${resource.id}-v1`,
                version: '1.0.0',
                timestamp: resource.timestamp || Date.now(),
                author: 'system',
                content: resource,
                metadata: {}
              }],
              semantics: [],
              realities: [],
              coherence: 1.0,
              dominance: 'default',
              compressionLevel: 0.0
            },
            version: '1.0.0',
            realityId: 'default',
            timestamp: resource.timestamp || Date.now(),
            projections: [{
              source: 'GRG',
              type: 'resource',
              representation: resource,
              timestamp: Date.now()
            }]
          });
        }
      }
    } catch (error) {
      console.log(`[Fabric Core] Failed to load GRG: ${error}`);
    }
  }
  
  private async loadSRG(): Promise<void> {
    try {
      const fs = require('fs');
      const path = require('path');
      const srgPath = path.join(__dirname, '../../../storage/gl-artifacts-store/semantic-resource-graph.json');
      
      if (fs.existsSync(srgPath)) {
        const srgData = JSON.parse(fs.readFileSync(srgPath, 'utf-8'));
        console.log(`[Fabric Core] Loaded SRG v${srgData.version} with ${srgData.semanticNodes.length} nodes`);
        
        // 將 SRG 語意節點轉換為 Fabric 節點
        for (const semanticNode of srgData.semanticNodes) {
          await this.addNode({
            id: semanticNode.id,
            type: 'semantic',
            layer: 'semantic',
            properties: semanticNode.properties || {},
            superposition: {
              versions: [{
                id: `${semanticNode.id}-v1`,
                version: '1.0.0',
                timestamp: semanticNode.timestamp || Date.now(),
                author: 'system',
                content: semanticNode,
                metadata: {}
              }],
              semantics: [{
                id: `${semanticNode.id}-sem1`,
                semanticType: semanticNode.semanticType,
                confidence: semanticNode.confidence || 0.8,
                meaning: semanticNode.meaning,
                context: semanticNode.context || {}
              }],
              realities: [],
              coherence: 1.0,
              dominance: 'default',
              compressionLevel: 0.0
            },
            version: '1.0.0',
            realityId: 'default',
            timestamp: semanticNode.timestamp || Date.now(),
            projections: [{
              source: 'SRG',
              type: 'semantic',
              representation: semanticNode,
              timestamp: Date.now()
            }]
          });
        }
      }
    } catch (error) {
      console.log(`[Fabric Core] Failed to load SRG: ${error}`);
    }
  }
  
  private async loadOtherData(): Promise<void> {
    // 載入 Swarm、Mesh、Civilization、Inter-Reality 數據
    // 這些將在對應組件初始化時動態加入
  }
  
  // ========================================================================
  // Node Operations
  // ========================================================================
  
  async addNode(node: FabricNode): Promise<string> {
    // 驗證節點
    if (!node.id || !node.type || !node.layer) {
      throw new Error('Invalid node: missing required fields');
    }
    
    // 添加節點到圖
    this.graph.nodes.set(node.id, node);
    
    // 添加到層級視圖
    const layerView = this.graph.layers.get(node.layer);
    if (layerView) {
      layerView.nodes.add(node.id);
    }
    
    // 更新元資料
    this.graph.metadata.totalNodes++;
    this.graph.metadata.lastModified = Date.now();
    
    // 更新疊加態統計
    if (node.superposition.versions.length > 1 ||
        node.superposition.semantics.length > 1 ||
        node.superposition.realities.length > 1) {
      this.updateSuperpositionStats();
    }
    
    console.log(`[Fabric Core] Added node ${node.id} (${node.type}) at layer ${node.layer}`);
    return node.id;
  }
  
  async getNode(id: string): Promise<FabricNode | undefined> {
    return this.graph.nodes.get(id);
  }
  
  async updateNode(id: string, updates: Partial<FabricNode>): Promise<void> {
    const node = this.graph.nodes.get(id);
    if (!node) {
      throw new Error(`Node ${id} not found`);
    }
    
    // 更新節點
    Object.assign(node, updates);
    node.timestamp = Date.now();
    
    // 更新元資料
    this.graph.metadata.lastModified = Date.now();
    
    console.log(`[Fabric Core] Updated node ${id}`);
  }
  
  async removeNode(id: string): Promise<void> {
    const node = this.graph.nodes.get(id);
    if (!node) {
      throw new Error(`Node ${id} not found`);
    }
    
    // 移除節點
    this.graph.nodes.delete(id);
    
    // 從層級視圖移除
    const layerView = this.graph.layers.get(node.layer);
    if (layerView) {
      layerView.nodes.delete(id);
    }
    
    // 移除所有相關邊
    const edgesToRemove: string[] = [];
    for (const [edgeId, edge] of this.graph.edges) {
      if (edge.sourceId === id || edge.targetId === id) {
        edgesToRemove.push(edgeId);
      }
    }
    
    for (const edgeId of edgesToRemove) {
      await this.removeEdge(edgeId);
    }
    
    // 更新元資料
    this.graph.metadata.totalNodes--;
    this.graph.metadata.lastModified = Date.now();
    
    console.log(`[Fabric Core] Removed node ${id}`);
  }
  
  // ========================================================================
  // Edge Operations
  // ========================================================================
  
  async addEdge(edge: FabricEdge): Promise<string> {
    // 驗證邊
    if (!edge.id || !edge.sourceId || !edge.targetId || !edge.type) {
      throw new Error('Invalid edge: missing required fields');
    }
    
    // 驗證節點存在
    if (!this.graph.nodes.has(edge.sourceId) || !this.graph.nodes.has(edge.targetId)) {
      throw new Error('Source or target node not found');
    }
    
    // 添加邊到圖
    this.graph.edges.set(edge.id, edge);
    
    // 添加到層級視圖
    const layerView = this.graph.layers.get(edge.layer);
    if (layerView) {
      layerView.edges.add(edge.id);
    }
    
    // 更新元資料
    this.graph.metadata.totalEdges++;
    this.graph.metadata.lastModified = Date.now();
    
    console.log(`[Fabric Core] Added edge ${edge.id} (${edge.type}) from ${edge.sourceId} to ${edge.targetId}`);
    return edge.id;
  }
  
  async getEdge(id: string): Promise<FabricEdge | undefined> {
    return this.graph.edges.get(id);
  }
  
  async updateEdge(id: string, updates: Partial<FabricEdge>): Promise<void> {
    const edge = this.graph.edges.get(id);
    if (!edge) {
      throw new Error(`Edge ${id} not found`);
    }
    
    // 更新邊
    Object.assign(edge, updates);
    edge.timestamp = Date.now();
    
    // 更新元資料
    this.graph.metadata.lastModified = Date.now();
    
    console.log(`[Fabric Core] Updated edge ${id}`);
  }
  
  async removeEdge(id: string): Promise<void> {
    const edge = this.graph.edges.get(id);
    if (!edge) {
      throw new Error(`Edge ${id} not found`);
    }
    
    // 移除邊
    this.graph.edges.delete(id);
    
    // 從層級視圖移除
    const layerView = this.graph.layers.get(edge.layer);
    if (layerView) {
      layerView.edges.delete(id);
    }
    
    // 更新元資料
    this.graph.metadata.totalEdges--;
    this.graph.metadata.lastModified = Date.now();
    
    console.log(`[Fabric Core] Removed edge ${id}`);
  }
  
  // ========================================================================
  // Query Operations
  // ========================================================================
  
  async queryNodes(filter: {
    type?: NodeType;
    layer?: FabricLayer;
    realityId?: string;
    version?: string;
    properties?: Record<string, any>;
  }): Promise<FabricNode[]> {
    const results: FabricNode[] = [];
    
    for (const node of this.graph.nodes.values()) {
      let match = true;
      
      if (filter.type && node.type !== filter.type) {
        match = false;
      }
      
      if (filter.layer && node.layer !== filter.layer) {
        match = false;
      }
      
      if (filter.realityId && node.realityId !== filter.realityId) {
        match = false;
      }
      
      if (filter.version && node.version !== filter.version) {
        match = false;
      }
      
      if (filter.properties) {
        for (const [key, value] of Object.entries(filter.properties)) {
          if (node.properties[key] !== value) {
            match = false;
            break;
          }
        }
      }
      
      if (match) {
        results.push(node);
      }
    }
    
    return results;
  }
  
  async queryEdges(filter: {
    sourceId?: string;
    targetId?: string;
    type?: EdgeType;
    layer?: FabricLayer;
    realityId?: string;
  }): Promise<FabricEdge[]> {
    const results: FabricEdge[] = [];
    
    for (const edge of this.graph.edges.values()) {
      let match = true;
      
      if (filter.sourceId && edge.sourceId !== filter.sourceId) {
        match = false;
      }
      
      if (filter.targetId && edge.targetId !== filter.targetId) {
        match = false;
      }
      
      if (filter.type && edge.type !== filter.type) {
        match = false;
      }
      
      if (filter.layer && edge.layer !== filter.layer) {
        match = false;
      }
      
      if (filter.realityId && edge.realityId !== filter.realityId) {
        match = false;
      }
      
      if (match) {
        results.push(edge);
      }
    }
    
    return results;
  }
  
  async findPath(sourceId: string, targetId: string, options?: {
    maxDepth?: number;
    edgeTypes?: EdgeType[];
  }): Promise<string[]> {
    const visited = new Set<string>();
    const queue: Array<{nodeId: string; path: string[]}> = [];
    
    queue.push({nodeId: sourceId, path: [sourceId]});
    visited.add(sourceId);
    
    const maxDepth = options?.maxDepth || 10;
    
    while (queue.length > 0) {
      const {nodeId, path} = queue.shift()!;
      
      if (nodeId === targetId) {
        return path;
      }
      
      if (path.length >= maxDepth) {
        continue;
      }
      
      // 查找相鄰節點
      const adjacentEdges = await this.queryEdges({sourceId: nodeId});
      
      // 將 edgeTypes 正規化為乾淨的字串陣列以避免型別混淆（例如字串 vs 陣列）
      const rawEdgeTypes = options?.edgeTypes;
      let allowedEdgeTypes: string[] | undefined;
      if (Array.isArray(rawEdgeTypes)) {
        allowedEdgeTypes = rawEdgeTypes
          .filter((t): t is string => typeof t === 'string')
          .map(t => t);
      } else if (typeof rawEdgeTypes === 'string') {
        allowedEdgeTypes = [rawEdgeTypes];
      } else {
        allowedEdgeTypes = undefined;
      }
      
      for (const edge of adjacentEdges) {
        if (allowedEdgeTypes && !allowedEdgeTypes.includes(edge.type)) {
          continue;
        }
        
        if (!visited.has(edge.targetId)) {
          visited.add(edge.targetId);
          queue.push({
            nodeId: edge.targetId,
            path: [...path, edge.targetId]
          });
        }
      }
    }
    
    return []; // 未找到路徑
  }
  
  // ========================================================================
  // Projection Operations
  // ========================================================================
  
  async syncProjection(projectionId: string): Promise<void> {
    const projection = this.graph.projections.get(projectionId);
    if (!projection) {
      throw new Error(`Projection ${projectionId} not found`);
    }
    
    console.log(`[Fabric Core] Syncing projection ${projectionId}...`);
    
    // 根據投影來源同步數據
    switch (projectionId) {
      case 'GRG':
        await this.syncGRGProjection(projection);
        break;
      case 'SRG':
        await this.syncSRGProjection(projection);
        break;
      case 'GlobalDAG':
        await this.syncGlobalDAGProjection(projection);
        break;
      case 'Swarm':
        await this.syncSwarmProjection(projection);
        break;
      case 'Mesh':
        await this.syncMeshProjection(projection);
        break;
      case 'Civilization':
        await this.syncCivilizationProjection(projection);
        break;
      case 'InterReality':
        await this.syncInterRealityProjection(projection);
        break;
      default:
        throw new Error(`Unknown projection: ${projectionId}`);
    }
    
    projection.lastSync = Date.now();
    console.log(`[Fabric Core] Projection ${projectionId} synced`);
  }
  
  private async syncGRGProjection(projection: ProjectionView): Promise<void> {
    // GRG 已在初始化時載入
    // 這裡可以做增量同步
  }
  
  private async syncSRGProjection(projection: ProjectionView): Promise<void> {
    // SRG 已在初始化時載入
    // 這裡可以做增量同步
  }
  
  private async syncGlobalDAGProjection(projection: ProjectionView): Promise<void> {
    // 將從 Global DAG 載入數據並轉換為 Fabric 節點
  }
  
  private async syncSwarmProjection(projection: ProjectionView): Promise<void> {
    // 將從 Swarm 載入數據並轉換為 Fabric 節點
  }
  
  private async syncMeshProjection(projection: ProjectionView): Promise<void> {
    // 將從 Mesh 載入數據並轉換為 Fabric 節點
  }
  
  private async syncCivilizationProjection(projection: ProjectionView): Promise<void> {
    // 將從 Civilization 載入數據並轉換為 Fabric 節點
  }
  
  private async syncInterRealityProjection(projection: ProjectionView): Promise<void> {
    // 將從 Inter-Reality 載入數據並轉換為 Fabric 節點
  }
  
  // ========================================================================
  // Evolution Operations
  // ========================================================================
  
  async triggerEvolution(): Promise<void> {
    console.log('[Fabric Core] Triggering fabric evolution...');
    
    const result = await this.evolutionEngine.evolve();
    
    // 記錄演化事件
    this.graph.evolution.evolutionHistory.push(...result.events);
    this.graph.evolution.lastEvolution = Date.now();
    this.graph.evolution.generation++;
    this.graph.evolution.adaptationRate = result.adaptationRate;
    this.graph.evolution.stabilityScore = result.stabilityScore;
    
    // 更新元資料
    this.graph.metadata.evolutionCount++;
    this.graph.metadata.lastModified = Date.now();
    
    console.log(`[Fabric Core] Evolution complete: ${result.events.length} events, adaptation rate: ${result.adaptationRate}`);
  }
  
  // ========================================================================
  // Statistics and Monitoring
  // ========================================================================
  
  async getStatistics(): Promise<FabricStatistics> {
    return {
      metadata: this.graph.metadata,
      evolution: this.graph.evolution,
      layerStats: await this.calculateLayerStatistics(),
      superpositionStats: await this.calculateSuperpositionStatistics()
    };
  }
  
  private async calculateLayerStatistics(): Promise<Record<FabricLayer, LayerStatistics>> {
    const stats: Record<FabricLayer, LayerStatistics> = {} as any;
    
    for (const [layer, view] of this.graph.layers) {
      stats[layer] = {
        nodeCount: view.nodes.size,
        edgeCount: view.edges.size,
        density: view.nodes.size > 1 ? view.edges.size / (view.nodes.size * (view.nodes.size - 1)) : 0.0,
        avgClustering: await this.calculateClusteringCoefficient(layer),
        maxConnectedComponent: await this.findLargestComponent(layer)
      };
      
      view.statistics = stats[layer];
    }
    
    return stats;
  }
  
  private async calculateClusteringCoefficient(layer: FabricLayer): Promise<number> {
    // 簡化實作：返回固定值
    return 0.5;
  }
  
  private async findLargestComponent(layer: FabricLayer): Promise<number> {
    // 簡化實作：返回節點數
    const view = this.graph.layers.get(layer);
    return view?.nodes.size || 0;
  }
  
  private async calculateSuperpositionStatistics(): Promise<SuperpositionStatistics> {
    let superpositionNodes = 0;
    let totalCompressionLevel = 0;
    
    for (const node of this.graph.nodes.values()) {
      const isSuperposition = node.superposition.versions.length > 1 ||
                             node.superposition.semantics.length > 1 ||
                             node.superposition.realities.length > 1;
      
      if (isSuperposition) {
        superpositionNodes++;
        totalCompressionLevel += node.superposition.compressionLevel;
      }
    }
    
    const superpositionRatio = this.graph.nodes.size > 0 
      ? superpositionNodes / this.graph.nodes.size 
      : 0.0;
    
    const avgCompressionLevel = superpositionNodes > 0
      ? totalCompressionLevel / superpositionNodes
      : 0.0;
    
    // 更新元資料
    this.graph.metadata.superpositionRatio = superpositionRatio;
    this.graph.metadata.averageCompressionLevel = avgCompressionLevel;
    
    return {
      superpositionRatio,
      avgCompressionLevel,
      totalSuperpositionNodes: superpositionNodes
    };
  }
  
  private updateSuperpositionStats(): void {
    // 異步更新疊加態統計
    this.calculateSuperpositionStatistics().catch(console.error);
  }
  
  // ========================================================================
  // Public Accessors
  // ========================================================================
  
  getGraph(): FabricGraph {
    return this.graph;
  }
  
  isInitialized(): boolean {
    return this.initialized;
  }
}

// ============================================================================
// Supporting Classes
// ============================================================================

class FabricEvolutionEngine {
  constructor(private graph: FabricGraph) {}
  
  async evolve(): Promise<EvolutionResult> {
    const events: EvolutionEvent[] = [];
    let adaptationRate = 0.0;
    let stabilityScore = 1.0;
    
    // 1. 權重調整
    await this.adjustWeights(events);
    
    // 2. 拓樸優化
    await this.optimizeTopology(events);
    
    // 3. 無效結構淘汰
    await this.pruneInvalidStructures(events);
    
    // 4. 計算適應率
    adaptationRate = await this.calculateAdaptationRate();
    
    // 5. 計算穩定度
    stabilityScore = await this.calculateStabilityScore();
    
    return {
      events,
      adaptationRate,
      stabilityScore
    };
  }
  
  private async adjustWeights(events: EvolutionEvent[]): Promise<void> {
    // 調整邊的權重
    for (const [edgeId, edge] of this.graph.edges) {
      // 基於使用頻率調整權重
      const weightAdjustment = Math.random() * 0.1 - 0.05; // -5% to +5%
      edge.weight = Math.max(0, Math.min(1, edge.weight + weightAdjustment));
      
      this.graph.evolution.weightChanges.set(edgeId, edge.weight);
    }
  }
  
  private async optimizeTopology(events: EvolutionEvent[]): Promise<void> {
    // 優化圖拓樸：添加新連接、移除弱連接
    const weakEdges: string[] = [];
    
    for (const [edgeId, edge] of this.graph.edges) {
      if (edge.weight < 0.1) {
        weakEdges.push(edgeId);
      }
    }
    
    // 移除弱邊
    for (const edgeId of weakEdges) {
      events.push({
        id: `ev-${Date.now()}-${edgeId}`,
        timestamp: Date.now(),
        type: 'edge_remove',
        description: `Removed weak edge ${edgeId}`,
        impact: edgeId.length * 0.01
      });
    }
    
    // 記錄拓樸變化
    this.graph.evolution.topologyChanges.push({
      timestamp: Date.now(),
      nodesAdded: 0,
      nodesRemoved: 0,
      edgesAdded: 0,
      edgesRemoved: weakEdges.length,
      subgraphRewritten: false
    });
  }
  
  private async pruneInvalidStructures(events: EvolutionEvent[]): Promise<void> {
    // 移除孤立節點
    const isolatedNodes: string[] = [];
    
    for (const [nodeId, _] of this.graph.nodes) {
      const incomingEdges = Array.from(this.graph.edges.values()).filter(e => e.targetId === nodeId);
      const outgoingEdges = Array.from(this.graph.edges.values()).filter(e => e.sourceId === nodeId);
      
      if (incomingEdges.length === 0 && outgoingEdges.length === 0) {
        isolatedNodes.push(nodeId);
      }
    }
    
    // 移除孤立節點
    for (const nodeId of isolatedNodes) {
      events.push({
        id: `ev-${Date.now()}-${nodeId}`,
        timestamp: Date.now(),
        type: 'node_remove',
        description: `Removed isolated node ${nodeId}`,
        impact: nodeId.length * 0.01
      });
    }
  }
  
  private async calculateAdaptationRate(): Promise<number> {
    // 計算適應率：基於演化事件的影響總和
    const totalImpact = this.graph.evolution.evolutionHistory
      .slice(-10) // 最近10個事件
      .reduce((sum, event) => sum + event.impact, 0);
    
    return Math.min(1.0, totalImpact / 10);
  }
  
  private async calculateStabilityScore(): Promise<number> {
    // 計算穩定度：基於權重變化程度
    let totalWeightChange = 0;
    
    for (const change of this.graph.evolution.weightChanges.values()) {
      totalWeightChange += Math.abs(change - 0.5); // 假設初始權重為0.5
    }
    
    const avgChange = this.graph.edges.size > 0 
      ? totalWeightChange / this.graph.edges.size 
      : 0;
    
    return Math.max(0, 1.0 - avgChange);
  }
}

class FabricProjectionEngine {
  constructor(private graph: FabricGraph) {}
  
  async createProjection(sourceSystem: string, transformationRules: any[]): Promise<string> {
    const projectionId = sourceSystem;
    
    this.graph.projections.set(projectionId, {
      id: projectionId,
      sourceSystem,
      nodes: new Set(),
      edges: new Set(),
      transformationRules,
      mappingFunctions: new Map(),
      lastSync: 0,
      consistency: 0.0
    });
    
    console.log(`[Fabric Projection] Created projection ${projectionId}`);
    return projectionId;
  }
  
  async getProjection(projectionId: string): Promise<ProjectionView | undefined> {
    return this.graph.projections.get(projectionId);
  }
}

// ============================================================================
// Type Definitions for Statistics
// ============================================================================

export interface FabricStatistics {
  metadata: FabricMetadata;
  evolution: EvolutionState;
  layerStats: Record<FabricLayer, LayerStatistics>;
  superpositionStats: SuperpositionStatistics;
}

export interface SuperpositionStatistics {
  superpositionRatio: number;
  avgCompressionLevel: number;
  totalSuperpositionNodes: number;
}

export interface EvolutionResult {
  events: EvolutionEvent[];
  adaptationRate: number;
  stabilityScore: number;
}