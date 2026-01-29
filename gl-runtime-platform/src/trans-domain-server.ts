// @GL-governed
// @GL-layer: GL70-89
// @GL-semantic: runtime-trans-domain-integration
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Trans-Domain Integration Architecture API Server
 * 
 * REST API 伺服器 - 提供 Version 17 跨域整合架構的所有功能
 * 
 * Port: 3009
 */

const express = require('express');
const cors = require('cors');
import { GLTransDomainArchitecture } from '../trans-domain';

const app = express();
const PORT = 3009;

// Initialize trans-domain architecture
const transDomain = new GLTransDomainArchitecture();

// Middleware
app.use(cors());
app.use(express.json());

/**
 * Health Check Endpoint
 */
app.get('/health', (req, res) => {
  const status = transDomain.getStatus();
  res.json({
    status: 'healthy',
    version: '17.0.0',
    transDomain: status.overall ? 'active' : 'inactive',
    components: {
      crossSystemIntegration: status.crossSystemIntegration ? 'active' : 'inactive',
      multiModelAlignment: status.multiModelAlignment ? 'active' : 'inactive',
      knowledgeMapping: status.knowledgeMapping ? 'active' : 'inactive',
      interSystemGovernance: status.interSystemGovernance ? 'active' : 'inactive',
      universalInterface: status.universalInterface ? 'active' : 'inactive',
      stabilityEngine: status.stabilityEngine ? 'active' : 'inactive'
    }
  });
});

/**
 * Get Trans-Domain Status
 */
app.get('/api/v17/trans-domain/status', (req, res) => {
  const status = transDomain.getStatus();
  const statistics = transDomain.getStatistics();
  
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
app.get('/api/v17/trans-domain/demonstrate', async (req, res) => {
  try {
    const demonstrations: any[] = [];

    // 1. Cross-System Integration
    const crossSystem = transDomain.getCrossSystemIntegration();
    demonstrations.push({
      capability: 'Cross-System Integration',
      description: '智慧的外延擴張 - 與外部平台、模型、工具、知識庫整合',
      result: {
        externalSystems: crossSystem.getExternalSystems().length,
        integrationHistory: crossSystem.getIntegrationHistory().length
      }
    });

    // 2. Multi-Model Alignment
    const multiModel = transDomain.getMultiModelAlignment();
    demonstrations.push({
      capability: 'Multi-Model Alignment',
      description: '智慧的兼容性 - 對齊不同推理框架、語意模型、策略結構、知識表示',
      result: {
        registeredModels: multiModel.getRegisteredModels().length,
        alignmentHistory: multiModel.getAlignmentHistory().length
      }
    });

    // 3. Knowledge Mapping
    const knowledgeMapping = transDomain.getKnowledgeMapping();
    demonstrations.push({
      capability: 'Knowledge Mapping',
      description: '智慧的遷移能力 - 跨領域、跨文明、跨 Mesh 的知識映射',
      result: {
        domains: knowledgeMapping.getDomains().length,
        mappings: knowledgeMapping.getMappings().length
      }
    });

    // 4. Inter-System Governance
    const governance = transDomain.getInterSystemGovernance();
    demonstrations.push({
      capability: 'Inter-System Governance',
      description: '智慧的協調能力 - 管理多平台、多文明、多模型、多叢集',
      result: {
        scopes: governance.getScopes().length,
        governanceHistory: governance.getGovernanceHistory().length
      }
    });

    // 5. Universal Interface
    const universalInterface = transDomain.getUniversalInterface();
    demonstrations.push({
      capability: 'Universal Interface',
      description: '智慧的語言 - 以統一語意、策略、結構與外界溝通',
      result: {
        protocols: universalInterface.getSupportedProtocols().length,
        activeConnections: universalInterface.getActiveConnections().size,
        messageHistory: universalInterface.getMessageHistory().length
      }
    });

    // 6. Stability Engine
    const stability = transDomain.getStabilityEngine();
    demonstrations.push({
      capability: 'Trans-Domain Stability',
      description: '智慧的穩定性 - 保持跨域推理的一致性、穩定性、安全性、可解釋性',
      result: {
        checkHistory: stability.getCheckHistory().length,
        violations: stability.getViolations().filter(v => !v.resolved).length,
        snapshots: stability.getSnapshots().length
      }
    });

    res.json({
      success: true,
      version: '17.0.0',
      philosophy: '智慧的外延擴張階段 - 整合外部系統、知識、模型、文明的能力',
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
 * Cross-System Integration Endpoints
 */
app.get('/api/v17/cross-system/systems', (req, res) => {
  const systems = transDomain.getCrossSystemIntegration().getExternalSystems();
  res.json({ success: true, systems });
});

app.post('/api/v17/cross-system/register', (req, res) => {
  const { system } = req.body;
  transDomain.getCrossSystemIntegration().registerExternalSystem(system);
  res.json({ success: true, message: 'System registered' });
});

app.post('/api/v17/cross-system/connect/:systemId', async (req, res) => {
  const { systemId } = req.params;
  const result = await transDomain.getCrossSystemIntegration().connectToSystem(systemId);
  res.json({ success: result.success, result });
});

/**
 * Multi-Model Alignment Endpoints
 */
app.get('/api/v17/multi-model/models', (req, res) => {
  const models = transDomain.getMultiModelAlignment().getRegisteredModels();
  res.json({ success: true, models });
});

app.post('/api/v17/multi-model/register', (req, res) => {
  const { model } = req.body;
  transDomain.getMultiModelAlignment().registerModel(model);
  res.json({ success: true, message: 'Model registered' });
});

app.post('/api/v17/multi-model/align', async (req, res) => {
  const { sourceModelId, targetModelId } = req.body;
  const result = await transDomain.getMultiModelAlignment().alignModels(sourceModelId, targetModelId);
  res.json({ success: result.success, result });
});

/**
 * Knowledge Mapping Endpoints
 */
app.get('/api/v17/knowledge/domains', (req, res) => {
  const domains = transDomain.getKnowledgeMapping().getDomains();
  res.json({ success: true, domains });
});

app.post('/api/v17/knowledge/register', (req, res) => {
  const { domain } = req.body;
  transDomain.getKnowledgeMapping().registerDomain(domain);
  res.json({ success: true, message: 'Domain registered' });
});

app.post('/api/v17/knowledge/map', async (req, res) => {
  const { sourceDomainId, targetDomainId, mappingType } = req.body;
  const result = await transDomain.getKnowledgeMapping().mapKnowledge(
    sourceDomainId,
    targetDomainId,
    mappingType
  );
  res.json({ success: result.success, result });
});

/**
 * Inter-System Governance Endpoints
 */
app.get('/api/v17/governance/scopes', (req, res) => {
  const scopes = transDomain.getInterSystemGovernance().getScopes();
  res.json({ success: true, scopes });
});

app.post('/api/v17/governance/register', (req, res) => {
  const { scope } = req.body;
  transDomain.getInterSystemGovernance().registerScope(scope);
  res.json({ success: true, message: 'Scope registered' });
});

app.get('/api/v17/governance/dependencies', async (req, res) => {
  const { platformIds } = req.query;
  const ids = typeof platformIds === 'string' ? platformIds.split(',') : [];
  const graph = await transDomain.getInterSystemGovernance().managePlatformDependencies(ids);
  res.json({ success: true, graph });
});

app.get('/api/v17/governance/collaboration', async (req, res) => {
  const { modelIds } = req.query;
  const ids = typeof modelIds === 'string' ? modelIds.split(',') : [];
  const matrix = await transDomain.getInterSystemGovernance().manageModelCollaboration(ids);
  res.json({ success: true, matrix });
});

/**
 * Universal Interface Endpoints
 */
app.get('/api/v17/interface/protocols', (req, res) => {
  const protocols = transDomain.getUniversalInterface().getSupportedProtocols();
  res.json({ success: true, protocols });
});

app.get('/api/v17/interface/connections', (req, res) => {
  const connections = Object.fromEntries(
    transDomain.getUniversalInterface().getActiveConnections()
  );
  res.json({ success: true, connections });
});

app.get('/api/v17/interface/messages', (req, res) => {
  const messages = transDomain.getUniversalInterface().getMessageHistory();
  res.json({ success: true, messages });
});

app.post('/api/v17/interface/connect', async (req, res) => {
  const { systemId, protocol } = req.body;
  const result = await transDomain.getUniversalInterface().establishConnection(systemId, protocol);
  res.json({ success: result, message: result ? 'Connection established' : 'Connection failed' });
});

/**
 * Stability Engine Endpoints
 */
app.get('/api/v17/stability/metrics', (req, res) => {
  const metrics = Object.fromEntries(
    transDomain.getStabilityEngine().getAllMetrics()
  );
  res.json({ success: true, metrics });
});

app.get('/api/v17/stability/checks', (req, res) => {
  const checks = transDomain.getStabilityEngine().getCheckHistory();
  res.json({ success: true, checks });
});

app.get('/api/v17/stability/violations', (req, res) => {
  const violations = transDomain.getStabilityEngine().getViolations();
  res.json({ success: true, violations });
});

app.get('/api/v17/stability/snapshots', (req, res) => {
  const snapshots = transDomain.getStabilityEngine().getSnapshots();
  res.json({ success: true, snapshots });
});

app.post('/api/v17/stability/check-consistency', async (req, res) => {
  const { sourceDomain, targetDomain, reasoning } = req.body;
  const result = await transDomain.getStabilityEngine().checkReasoningConsistency(
    sourceDomain,
    targetDomain,
    reasoning
  );
  res.json({ success: true, result });
});

app.post('/api/v17/stability/check-stability', async (req, res) => {
  const { civilization1, civilization2, collaboration } = req.body;
  const result = await transDomain.getStabilityEngine().checkCollaborationStability(
    civilization1,
    civilization2,
    collaboration
  );
  res.json({ success: true, result });
});

app.post('/api/v17/stability/check-safety', async (req, res) => {
  const { system1, system2, integration } = req.body;
  const result = await transDomain.getStabilityEngine().checkIntegrationSafety(
    system1,
    system2,
    integration
  );
  res.json({ success: true, result });
});

app.post('/api/v17/stability/check-explainability', async (req, res) => {
  const { model1, model2, alignment } = req.body;
  const result = await transDomain.getStabilityEngine().checkAlignmentExplainability(
    model1,
    model2,
    alignment
  );
  res.json({ success: true, result });
});

/**
 * Start Server
 */
async function startServer() {
  try {
    // Initialize trans-domain architecture
    await transDomain.initialize();
    
    // Start server
    app.listen(PORT, () => {
      console.log(`🌌 GL Trans-Domain Integration Architecture API Server`);
      console.log(`   Version: 17.0.0`);
      console.log(`   Port: ${PORT}`);
      console.log(`   Philosophy: 智慧的外延擴張階段`);
      console.log(`   Status: Active`);
      console.log('');
      console.log(`   Endpoints:`);
      console.log(`   - GET  /health`);
      console.log(`   - GET  /api/v17/trans-domain/status`);
      console.log(`   - GET  /api/v17/trans-domain/demonstrate`);
      console.log(`   - GET  /api/v17/cross-system/*`);
      console.log(`   - GET  /api/v17/multi-model/*`);
      console.log(`   - GET  /api/v17/knowledge/*`);
      console.log(`   - GET  /api/v17/governance/*`);
      console.log(`   - GET  /api/v17/interface/*`);
      console.log(`   - GET  /api/v17/stability/*`);
    });
  } catch (error) {
    console.error('Error starting server:', error);
    process.exit(1);
  }
}

// Start the server
startServer();