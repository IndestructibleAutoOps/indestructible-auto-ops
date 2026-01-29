"use strict";
// @GL-governed
// @GL-layer: GL70-89
// @GL-semantic: runtime-trans-domain-integration
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../engine/governance/GL_SEMANTIC_ANCHOR.json
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * GL Trans-Domain Integration Architecture API Server
 *
 * REST API 伺服器 - 提供 Version 17 跨域整合架構的所有功能
 *
 * Port: 3009
 */
var express = require('express');
var cors = require('cors');
var trans_domain_1 = require("../trans-domain");
var app = express();
var PORT = 3009;
// Initialize trans-domain architecture
var transDomain = new trans_domain_1.GLTransDomainArchitecture();
// Middleware
app.use(cors());
app.use(express.json());
/**
 * Health Check Endpoint
 */
app.get('/health', function (req, res) {
    var status = transDomain.getStatus();
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
app.get('/api/v17/trans-domain/status', function (req, res) {
    var status = transDomain.getStatus();
    var statistics = transDomain.getStatistics();
    res.json({
        success: true,
        status: status,
        statistics: statistics,
        timestamp: new Date().toISOString()
    });
});
/**
 * Demonstrate All Capabilities
 */
app.get('/api/v17/trans-domain/demonstrate', function (req, res) { return __awaiter(void 0, void 0, void 0, function () {
    var demonstrations, crossSystem, multiModel, knowledgeMapping, governance, universalInterface, stability;
    return __generator(this, function (_a) {
        try {
            demonstrations = [];
            crossSystem = transDomain.getCrossSystemIntegration();
            demonstrations.push({
                capability: 'Cross-System Integration',
                description: '智慧的外延擴張 - 與外部平台、模型、工具、知識庫整合',
                result: {
                    externalSystems: crossSystem.getExternalSystems().length,
                    integrationHistory: crossSystem.getIntegrationHistory().length
                }
            });
            multiModel = transDomain.getMultiModelAlignment();
            demonstrations.push({
                capability: 'Multi-Model Alignment',
                description: '智慧的兼容性 - 對齊不同推理框架、語意模型、策略結構、知識表示',
                result: {
                    registeredModels: multiModel.getRegisteredModels().length,
                    alignmentHistory: multiModel.getAlignmentHistory().length
                }
            });
            knowledgeMapping = transDomain.getKnowledgeMapping();
            demonstrations.push({
                capability: 'Knowledge Mapping',
                description: '智慧的遷移能力 - 跨領域、跨文明、跨 Mesh 的知識映射',
                result: {
                    domains: knowledgeMapping.getDomains().length,
                    mappings: knowledgeMapping.getMappings().length
                }
            });
            governance = transDomain.getInterSystemGovernance();
            demonstrations.push({
                capability: 'Inter-System Governance',
                description: '智慧的協調能力 - 管理多平台、多文明、多模型、多叢集',
                result: {
                    scopes: governance.getScopes().length,
                    governanceHistory: governance.getGovernanceHistory().length
                }
            });
            universalInterface = transDomain.getUniversalInterface();
            demonstrations.push({
                capability: 'Universal Interface',
                description: '智慧的語言 - 以統一語意、策略、結構與外界溝通',
                result: {
                    protocols: universalInterface.getSupportedProtocols().length,
                    activeConnections: universalInterface.getActiveConnections().size,
                    messageHistory: universalInterface.getMessageHistory().length
                }
            });
            stability = transDomain.getStabilityEngine();
            demonstrations.push({
                capability: 'Trans-Domain Stability',
                description: '智慧的穩定性 - 保持跨域推理的一致性、穩定性、安全性、可解釋性',
                result: {
                    checkHistory: stability.getCheckHistory().length,
                    violations: stability.getViolations().filter(function (v) { return !v.resolved; }).length,
                    snapshots: stability.getSnapshots().length
                }
            });
            res.json({
                success: true,
                version: '17.0.0',
                philosophy: '智慧的外延擴張階段 - 整合外部系統、知識、模型、文明的能力',
                demonstrations: demonstrations,
                timestamp: new Date().toISOString()
            });
        }
        catch (error) {
            res.status(500).json({
                success: false,
                error: String(error),
                timestamp: new Date().toISOString()
            });
        }
        return [2 /*return*/];
    });
}); });
/**
 * Cross-System Integration Endpoints
 */
app.get('/api/v17/cross-system/systems', function (req, res) {
    var systems = transDomain.getCrossSystemIntegration().getExternalSystems();
    res.json({ success: true, systems: systems });
});
app.post('/api/v17/cross-system/register', function (req, res) {
    var system = req.body.system;
    transDomain.getCrossSystemIntegration().registerExternalSystem(system);
    res.json({ success: true, message: 'System registered' });
});
app.post('/api/v17/cross-system/connect/:systemId', function (req, res) { return __awaiter(void 0, void 0, void 0, function () {
    var systemId, result;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                systemId = req.params.systemId;
                return [4 /*yield*/, transDomain.getCrossSystemIntegration().connectToSystem(systemId)];
            case 1:
                result = _a.sent();
                res.json({ success: result.success, result: result });
                return [2 /*return*/];
        }
    });
}); });
/**
 * Multi-Model Alignment Endpoints
 */
app.get('/api/v17/multi-model/models', function (req, res) {
    var models = transDomain.getMultiModelAlignment().getRegisteredModels();
    res.json({ success: true, models: models });
});
app.post('/api/v17/multi-model/register', function (req, res) {
    var model = req.body.model;
    transDomain.getMultiModelAlignment().registerModel(model);
    res.json({ success: true, message: 'Model registered' });
});
app.post('/api/v17/multi-model/align', function (req, res) { return __awaiter(void 0, void 0, void 0, function () {
    var _a, sourceModelId, targetModelId, result;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = req.body, sourceModelId = _a.sourceModelId, targetModelId = _a.targetModelId;
                return [4 /*yield*/, transDomain.getMultiModelAlignment().alignModels(sourceModelId, targetModelId)];
            case 1:
                result = _b.sent();
                res.json({ success: result.success, result: result });
                return [2 /*return*/];
        }
    });
}); });
/**
 * Knowledge Mapping Endpoints
 */
app.get('/api/v17/knowledge/domains', function (req, res) {
    var domains = transDomain.getKnowledgeMapping().getDomains();
    res.json({ success: true, domains: domains });
});
app.post('/api/v17/knowledge/register', function (req, res) {
    var domain = req.body.domain;
    transDomain.getKnowledgeMapping().registerDomain(domain);
    res.json({ success: true, message: 'Domain registered' });
});
app.post('/api/v17/knowledge/map', function (req, res) { return __awaiter(void 0, void 0, void 0, function () {
    var _a, sourceDomainId, targetDomainId, mappingType, result;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = req.body, sourceDomainId = _a.sourceDomainId, targetDomainId = _a.targetDomainId, mappingType = _a.mappingType;
                return [4 /*yield*/, transDomain.getKnowledgeMapping().mapKnowledge(sourceDomainId, targetDomainId, mappingType)];
            case 1:
                result = _b.sent();
                res.json({ success: result.success, result: result });
                return [2 /*return*/];
        }
    });
}); });
/**
 * Inter-System Governance Endpoints
 */
app.get('/api/v17/governance/scopes', function (req, res) {
    var scopes = transDomain.getInterSystemGovernance().getScopes();
    res.json({ success: true, scopes: scopes });
});
app.post('/api/v17/governance/register', function (req, res) {
    var scope = req.body.scope;
    transDomain.getInterSystemGovernance().registerScope(scope);
    res.json({ success: true, message: 'Scope registered' });
});
app.get('/api/v17/governance/dependencies', function (req, res) { return __awaiter(void 0, void 0, void 0, function () {
    var platformIds, ids, graph;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                platformIds = req.query.platformIds;
                ids = typeof platformIds === 'string' ? platformIds.split(',') : [];
                return [4 /*yield*/, transDomain.getInterSystemGovernance().managePlatformDependencies(ids)];
            case 1:
                graph = _a.sent();
                res.json({ success: true, graph: graph });
                return [2 /*return*/];
        }
    });
}); });
app.get('/api/v17/governance/collaboration', function (req, res) { return __awaiter(void 0, void 0, void 0, function () {
    var modelIds, ids, matrix;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                modelIds = req.query.modelIds;
                ids = typeof modelIds === 'string' ? modelIds.split(',') : [];
                return [4 /*yield*/, transDomain.getInterSystemGovernance().manageModelCollaboration(ids)];
            case 1:
                matrix = _a.sent();
                res.json({ success: true, matrix: matrix });
                return [2 /*return*/];
        }
    });
}); });
/**
 * Universal Interface Endpoints
 */
app.get('/api/v17/interface/protocols', function (req, res) {
    var protocols = transDomain.getUniversalInterface().getSupportedProtocols();
    res.json({ success: true, protocols: protocols });
});
app.get('/api/v17/interface/connections', function (req, res) {
    var connections = Object.fromEntries(transDomain.getUniversalInterface().getActiveConnections());
    res.json({ success: true, connections: connections });
});
app.get('/api/v17/interface/messages', function (req, res) {
    var messages = transDomain.getUniversalInterface().getMessageHistory();
    res.json({ success: true, messages: messages });
});
app.post('/api/v17/interface/connect', function (req, res) { return __awaiter(void 0, void 0, void 0, function () {
    var _a, systemId, protocol, result;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = req.body, systemId = _a.systemId, protocol = _a.protocol;
                return [4 /*yield*/, transDomain.getUniversalInterface().establishConnection(systemId, protocol)];
            case 1:
                result = _b.sent();
                res.json({ success: result, message: result ? 'Connection established' : 'Connection failed' });
                return [2 /*return*/];
        }
    });
}); });
/**
 * Stability Engine Endpoints
 */
app.get('/api/v17/stability/metrics', function (req, res) {
    var metrics = Object.fromEntries(transDomain.getStabilityEngine().getAllMetrics());
    res.json({ success: true, metrics: metrics });
});
app.get('/api/v17/stability/checks', function (req, res) {
    var checks = transDomain.getStabilityEngine().getCheckHistory();
    res.json({ success: true, checks: checks });
});
app.get('/api/v17/stability/violations', function (req, res) {
    var violations = transDomain.getStabilityEngine().getViolations();
    res.json({ success: true, violations: violations });
});
app.get('/api/v17/stability/snapshots', function (req, res) {
    var snapshots = transDomain.getStabilityEngine().getSnapshots();
    res.json({ success: true, snapshots: snapshots });
});
app.post('/api/v17/stability/check-consistency', function (req, res) { return __awaiter(void 0, void 0, void 0, function () {
    var _a, sourceDomain, targetDomain, reasoning, result;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = req.body, sourceDomain = _a.sourceDomain, targetDomain = _a.targetDomain, reasoning = _a.reasoning;
                return [4 /*yield*/, transDomain.getStabilityEngine().checkReasoningConsistency(sourceDomain, targetDomain, reasoning)];
            case 1:
                result = _b.sent();
                res.json({ success: true, result: result });
                return [2 /*return*/];
        }
    });
}); });
app.post('/api/v17/stability/check-stability', function (req, res) { return __awaiter(void 0, void 0, void 0, function () {
    var _a, civilization1, civilization2, collaboration, result;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = req.body, civilization1 = _a.civilization1, civilization2 = _a.civilization2, collaboration = _a.collaboration;
                return [4 /*yield*/, transDomain.getStabilityEngine().checkCollaborationStability(civilization1, civilization2, collaboration)];
            case 1:
                result = _b.sent();
                res.json({ success: true, result: result });
                return [2 /*return*/];
        }
    });
}); });
app.post('/api/v17/stability/check-safety', function (req, res) { return __awaiter(void 0, void 0, void 0, function () {
    var _a, system1, system2, integration, result;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = req.body, system1 = _a.system1, system2 = _a.system2, integration = _a.integration;
                return [4 /*yield*/, transDomain.getStabilityEngine().checkIntegrationSafety(system1, system2, integration)];
            case 1:
                result = _b.sent();
                res.json({ success: true, result: result });
                return [2 /*return*/];
        }
    });
}); });
app.post('/api/v17/stability/check-explainability', function (req, res) { return __awaiter(void 0, void 0, void 0, function () {
    var _a, model1, model2, alignment, result;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = req.body, model1 = _a.model1, model2 = _a.model2, alignment = _a.alignment;
                return [4 /*yield*/, transDomain.getStabilityEngine().checkAlignmentExplainability(model1, model2, alignment)];
            case 1:
                result = _b.sent();
                res.json({ success: true, result: result });
                return [2 /*return*/];
        }
    });
}); });
/**
 * Start Server
 */
function startServer() {
    return __awaiter(this, void 0, void 0, function () {
        var error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    // Initialize trans-domain architecture
                    return [4 /*yield*/, transDomain.initialize()];
                case 1:
                    // Initialize trans-domain architecture
                    _a.sent();
                    // Start server
                    app.listen(PORT, function () {
                        console.log("\uD83C\uDF0C GL Trans-Domain Integration Architecture API Server");
                        console.log("   Version: 17.0.0");
                        console.log("   Port: ".concat(PORT));
                        console.log("   Philosophy: \u667A\u6167\u7684\u5916\u5EF6\u64F4\u5F35\u968E\u6BB5");
                        console.log("   Status: Active");
                        console.log('');
                        console.log("   Endpoints:");
                        console.log("   - GET  /health");
                        console.log("   - GET  /api/v17/trans-domain/status");
                        console.log("   - GET  /api/v17/trans-domain/demonstrate");
                        console.log("   - GET  /api/v17/cross-system/*");
                        console.log("   - GET  /api/v17/multi-model/*");
                        console.log("   - GET  /api/v17/knowledge/*");
                        console.log("   - GET  /api/v17/governance/*");
                        console.log("   - GET  /api/v17/interface/*");
                        console.log("   - GET  /api/v17/stability/*");
                    });
                    return [3 /*break*/, 3];
                case 2:
                    error_1 = _a.sent();
                    console.error('Error starting server:', error_1);
                    process.exit(1);
                    return [3 /*break*/, 3];
                case 3: return [2 /*return*/];
            }
        });
    });
}
// Start the server
startServer();
