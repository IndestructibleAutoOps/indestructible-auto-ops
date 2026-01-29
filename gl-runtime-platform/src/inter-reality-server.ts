// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-inter-reality-integration
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Inter-Reality Integration Architecture API Server
 * 
 * REST API 伺服器 - 提供 Version 18 跨現實整合架構的所有功能
 * 
 * Port: 3010
 */

const express = require('express');
const cors = require('cors');
const { GLInterRealityArchitecture } = require('../inter-reality');

const app = express();
const PORT = 3010;

// Initialize inter-reality architecture
const interReality = new GLInterRealityArchitecture();

// Middleware
app.use(cors());
app.use(express.json());

/**
 * Health Check Endpoint
 */
app.get('/health', (req, res) => {
  const status = interReality.getStatus();
  res.json({
    status: 'healthy',
    version: '18.0.0',
    interReality: status.overall ? 'active' : 'inactive',
    components: {
      realityModelAbstraction: status.realityModelAbstraction ? 'active' : 'inactive',
      multiRealityMapping: status.multiRealityMapping ? 'active' : 'inactive',
      adaptiveReasoning: status.adaptiveReasoning ? 'active' : 'inactive',
      crossRealityConsistency: status.crossRealityConsistency ? 'active' : 'inactive',
      invariantKnowledge: status.invariantKnowledge ? 'active' : 'inactive',
      interRealityGovernance: status.interRealityGovernance ? 'active' : 'inactive'
    }
  });
});

/**
 * Get Inter-Reality Status
 */
app.get('/api/v18/inter-reality/status', (req, res) => {
  const status = interReality.getStatus();
  const statistics = interReality.getStatistics();
  
  res.json({
    success: true,
    status,
    statistics,
    timestamp: new Date().toISOString()
  });
});

/**
 * Demonstrate All Capabilities
 */
app.get('/api/v18/inter-reality/demonstrate', async (req, res) => {
  try {
    const demonstrations: any[] = [];

    // 1. Reality Model Abstraction
    const realityAbstraction = interReality.getRealityModelAbstraction();
    demonstrations.push({
      capability: 'Reality Model Abstraction',
      description: '現實模型抽象 - 將不同環境抽象成統一語意、規則、結構、推理框架',
      result: {
        realityModels: realityAbstraction.getRealityModels().length,
        unifiedRealities: realityAbstraction.getUnifiedRealities().size,
        abstractionHistory: realityAbstraction.getAbstractionHistory().length
      }
    });

    // 2. Multi-Reality Mapping
    const multiRealityMapping = interReality.getMultiRealityMapping();
    demonstrations.push({
      capability: 'Multi-Reality Mapping',
      description: '多現實映射 - 跨世界規則映射、跨系統語意映射、跨文明結構映射',
      result: {
        realityMappings: multiRealityMapping.getRealityMappings().length,
        mappingHistory: multiRealityMapping.getMappingHistory().length,
        transferHistory: multiRealityMapping.getTransferHistory().length
      }
    });

    // 3. Adaptive Reasoning
    const adaptiveReasoning = interReality.getAdaptiveReasoning();
    demonstrations.push({
      capability: 'Reality-Adaptive Reasoning',
      description: '現實適應推理 - 推理方式調整、策略選擇調整、Mesh 結構調整、Swarm 分工調整',
      result: {
        realityContexts: adaptiveReasoning.getRealityContexts().length,
        adaptationHistory: adaptiveReasoning.getAdaptationHistory().length
      }
    });

    // 4. Cross-Reality Consistency
    const crossRealityConsistency = interReality.getCrossRealityConsistency();
    demonstrations.push({
      capability: 'Cross-Reality Consistency',
      description: '跨現實一致性 - 推理、語意、策略、文明規則、演化軌跡一致性檢查',
      result: {
        snapshots: crossRealityConsistency.getSnapshots().length,
        totalConsistencyChecks: Object.keys(crossRealityConsistency.getConsistencyChecks('')).length
      }
    });

    // 5. Invariant Knowledge
    const invariantKnowledge = interReality.getInvariantKnowledge();
    demonstrations.push({
      capability: 'Reality-Invariant Knowledge',
      description: '現實不變知識 - 跨環境規律、跨語言語意、跨文化結構、跨系統策略提取',
      result: {
        invariantKnowledge: invariantKnowledge.getAllInvariantKnowledge().length,
        extractionHistory: invariantKnowledge.getExtractionHistory().length,
        applicationHistory: invariantKnowledge.getApplicationHistory().length
      }
    });

    // 6. Inter-Reality Governance
    const interRealityGovernance = interReality.getInterRealityGovernance();
    demonstrations.push({
      capability: 'Inter-Reality Governance',
      description: '跨現實治理 - 跨框架依賴、跨世界規則、跨文明協作、跨 Mesh 整合管理',
      result: {
        governanceScopes: interRealityGovernance.getGovernanceScopes().length,
        governanceHistory: interRealityGovernance.getGovernanceHistory().length,
        snapshots: interRealityGovernance.getGovernanceSnapshots().length
      }
    });

    res.json({
      success: true,
      version: '18.0.0',
      philosophy: '智慧的跨框架穩定性階段 - 在不同現實框架之間保持一致性、穩定性、適應性',
      demonstrations,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: String(error),
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * Reality Model Abstraction Endpoints
 */
app.get('/api/v18/reality-abstraction/models', (req, res) => {
  const models = interReality.getRealityModelAbstraction().getRealityModels();
  res.json({ success: true, models });
});

app.post('/api/v18/reality-abstraction/register', (req, res) => {
  const { model } = req.body;
  interReality.getRealityModelAbstraction().registerRealityModel(model);
  res.json({ success: true, message: 'Reality model registered' });
});

app.post('/api/v18/reality-abstraction/abstract', async (req, res) => {
  const { realityId } = req.body;
  const result = await interReality.getRealityModelAbstraction().abstractReality(realityId);
  res.json({ success: result.success, result });
});

app.post('/api/v18/reality-abstraction/switch', async (req, res) => {
  const { fromRealityId, toRealityId } = req.body;
  const result = await interReality.getRealityModelAbstraction().switchReality(fromRealityId, toRealityId);
  res.json({ success: result, message: result ? 'Reality switched' : 'Switch failed' });
});

/**
 * Multi-Reality Mapping Endpoints
 */
app.get('/api/v18/multi-reality/mappings', (req, res) => {
  const mappings = interReality.getMultiRealityMapping().getRealityMappings();
  res.json({ success: true, mappings });
});

app.post('/api/v18/multi-reality/map', async (req, res) => {
  const { sourceReality, targetReality, type } = req.body;
  const result = await interReality.getMultiRealityMapping().createMapping(sourceReality, targetReality, type);
  res.json({ success: result.success, result });
});

app.post('/api/v18/multi-reality/transfer', async (req, res) => {
  const { sourceReality, targetReality, element } = req.body;
  const result = await interReality.getMultiRealityMapping().transferElement(sourceReality, targetReality, element);
  res.json({ success: result.success, result });
});

app.post('/api/v18/multi-reality/bidirectional', async (req, res) => {
  const { mappingId } = req.body;
  const result = await interReality.getMultiRealityMapping().makeBidirectional(mappingId);
  res.json({ success: result, message: result ? 'Mapping made bidirectional' : 'Failed' });
});

/**
 * Adaptive Reasoning Endpoints
 */
app.get('/api/v18/adaptive-reasoning/contexts', (req, res) => {
  const contexts = interReality.getAdaptiveReasoning().getRealityContexts();
  res.json({ success: true, contexts });
});

app.post('/api/v18/adaptive-reasoning/register', (req, res) => {
  const { context } = req.body;
  interReality.getAdaptiveReasoning().registerRealityContext(context);
  res.json({ success: true, message: 'Reality context registered' });
});

app.post('/api/v18/adaptive-reasoning/adapt', async (req, res) => {
  const { realityId } = req.body;
  const result = await interReality.getAdaptiveReasoning().adaptToReality(realityId);
  res.json({ success: result.success, result });
});

/**
 * Cross-Reality Consistency Endpoints
 */
app.get('/api/v18/cross-reality-consistency/checks', (req, res) => {
  const checks = interReality.getCrossRealityConsistency().getConsistencyChecks('reasoning');
  res.json({ success: true, checks });
});

app.post('/api/v18/cross-reality-consistency/check', async (req, res) => {
  const { realityIds, type, data } = req.body;
  let result;
  
  switch (type) {
    case 'reasoning':
      result = await interReality.getCrossRealityConsistency().checkReasoningConsistency(realityIds, data);
      break;
    case 'semantic':
      result = await interReality.getCrossRealityConsistency().checkSemanticConsistency(realityIds, data);
      break;
    case 'strategy':
      result = await interReality.getCrossRealityConsistency().checkStrategyConsistency(realityIds, data);
      break;
    case 'civilization':
      result = await interReality.getCrossRealityConsistency().checkCivilizationConsistency(realityIds, data);
      break;
    case 'evolution':
      result = await interReality.getCrossRealityConsistency().checkEvolutionConsistency(realityIds, data);
      break;
    default:
      res.status(400).json({ success: false, error: 'Invalid consistency type' });
      return;
  }
  
  res.json({ success: true, result });
});

app.post('/api/v18/cross-reality-consistency/snapshot', async (req, res) => {
  const { realityIds } = req.body;
  const snapshot = await interReality.getCrossRealityConsistency().createSnapshot(realityIds);
  res.json({ success: true, snapshot });
});

/**
 * Invariant Knowledge Endpoints
 */
app.get('/api/v18/invariant-knowledge/all', (req, res) => {
  const knowledge = interReality.getInvariantKnowledge().getAllInvariantKnowledge();
  res.json({ success: true, knowledge });
});

app.post('/api/v18/invariant-knowledge/extract', async (req, res) => {
  const { realityIds, type } = req.body;
  const result = await interReality.getInvariantKnowledge().extractInvariantKnowledge(realityIds, type);
  res.json({ success: true, result });
});

app.post('/api/v18/invariant-knowledge/apply', async (req, res) => {
  const { knowledgeId, targetReality } = req.body;
  const result = await interReality.getInvariantKnowledge().applyInvariantKnowledge(knowledgeId, targetReality);
  res.json({ success: true, result });
});

/**
 * Inter-Reality Governance Endpoints
 */
app.get('/api/v18/inter-reality-governance/scopes', (req, res) => {
  const scopes = interReality.getInterRealityGovernance().getGovernanceScopes();
  res.json({ success: true, scopes });
});

app.post('/api/v18/inter-reality-governance/register', (req, res) => {
  const { scope } = req.body;
  interReality.getInterRealityGovernance().registerGovernanceScope(scope);
  res.json({ success: true, message: 'Governance scope registered' });
});

app.post('/api/v18/inter-reality-governance/enforce', async (req, res) => {
  const { ruleId, affectedRealities, context } = req.body;
  const result = await interReality.getInterRealityGovernance().enforceRule(ruleId, affectedRealities, context);
  res.json({ success: true, result });
});

app.get('/api/v18/inter-reality-governance/topology', async (req, res) => {
  const topology = interReality.getInterRealityGovernance().getGovernanceTopology();
  res.json({ success: true, topology });
});

app.get('/api/v18/inter-reality-governance/collaboration', async (req, res) => {
  const matrix = interReality.getInterRealityGovernance().getCollaborationMatrix();
  res.json({ success: true, matrix });
});

app.post('/api/v18/inter-reality-governance/snapshot', async (req, res) => {
  const snapshot = await interReality.getInterRealityGovernance().createSnapshot();
  res.json({ success: true, snapshot });
});

/**
 * Start Server
 */
async function startServer() {
  try {
    // Initialize inter-reality architecture
    await interReality.initialize();
    
    // Start server
    app.listen(PORT, () => {
      console.log(`🌌 GL Inter-Reality Integration Architecture API Server`);
      console.log(`   Version: 18.0.0`);
      console.log(`   Port: ${PORT}`);
      console.log(`   Philosophy: 智慧的跨框架穩定性階段`);
      console.log(`   Status: Active`);
      console.log('');
      console.log(`   Endpoints:`);
      console.log(`   - GET  /health`);
      console.log(`   - GET  /api/v18/inter-reality/status`);
      console.log(`   - GET  /api/v18/inter-reality/demonstrate`);
      console.log(`   - GET  /api/v18/reality-abstraction/*`);
      console.log(`   - GET  /api/v18/multi-reality/*`);
      console.log(`   - GET  /api/v18/adaptive-reasoning/*`);
      console.log(`   - GET  /api/v18/cross-reality-consistency/*`);
      console.log(`   - GET  /api/v18/invariant-knowledge/*`);
      console.log(`   - GET  /api/v18/inter-reality-governance/*`);
    });
  } catch (error) {
    console.error('Error starting server:', error);
    process.exit(1);
  }
}

// Start the server
startServer();