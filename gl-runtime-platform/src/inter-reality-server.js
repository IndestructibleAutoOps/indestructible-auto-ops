// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-inter-reality-integration
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
var _this = this;
/**
 * GL Inter-Reality Integration Architecture API Server
 *
 * REST API 伺服器 - 提供 Version 18 跨現實整合架構的所有功能
 *
 * Port: 3010
 */
var express = require('express');
var cors = require('cors');
var GLInterRealityArchitecture = require('../inter-reality').GLInterRealityArchitecture;
var app = express();
var PORT = 3010;
// Initialize inter-reality architecture
var interReality = new GLInterRealityArchitecture();
// Middleware
app.use(cors());
app.use(express.json());
/**
 * Health Check Endpoint
 */
app.get('/health', function (req, res) {
    var status = interReality.getStatus();
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
app.get('/api/v18/inter-reality/status', function (req, res) {
    var status = interReality.getStatus();
    var statistics = interReality.getStatistics();
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
app.get('/api/v18/inter-reality/demonstrate', function (req, res) { return __awaiter(_this, void 0, void 0, function () {
    var demonstrations, realityAbstraction, multiRealityMapping, adaptiveReasoning, crossRealityConsistency, invariantKnowledge, interRealityGovernance;
    return __generator(this, function (_a) {
        try {
            demonstrations = [];
            realityAbstraction = interReality.getRealityModelAbstraction();
            demonstrations.push({
                capability: 'Reality Model Abstraction',
                description: '現實模型抽象 - 將不同環境抽象成統一語意、規則、結構、推理框架',
                result: {
                    realityModels: realityAbstraction.getRealityModels().length,
                    unifiedRealities: realityAbstraction.getUnifiedRealities().size,
                    abstractionHistory: realityAbstraction.getAbstractionHistory().length
                }
            });
            multiRealityMapping = interReality.getMultiRealityMapping();
            demonstrations.push({
                capability: 'Multi-Reality Mapping',
                description: '多現實映射 - 跨世界規則映射、跨系統語意映射、跨文明結構映射',
                result: {
                    realityMappings: multiRealityMapping.getRealityMappings().length,
                    mappingHistory: multiRealityMapping.getMappingHistory().length,
                    transferHistory: multiRealityMapping.getTransferHistory().length
                }
            });
            adaptiveReasoning = interReality.getAdaptiveReasoning();
            demonstrations.push({
                capability: 'Reality-Adaptive Reasoning',
                description: '現實適應推理 - 推理方式調整、策略選擇調整、Mesh 結構調整、Swarm 分工調整',
                result: {
                    realityContexts: adaptiveReasoning.getRealityContexts().length,
                    adaptationHistory: adaptiveReasoning.getAdaptationHistory().length
                }
            });
            crossRealityConsistency = interReality.getCrossRealityConsistency();
            demonstrations.push({
                capability: 'Cross-Reality Consistency',
                description: '跨現實一致性 - 推理、語意、策略、文明規則、演化軌跡一致性檢查',
                result: {
                    snapshots: crossRealityConsistency.getSnapshots().length,
                    totalConsistencyChecks: Object.keys(crossRealityConsistency.getConsistencyChecks('')).length
                }
            });
            invariantKnowledge = interReality.getInvariantKnowledge();
            demonstrations.push({
                capability: 'Reality-Invariant Knowledge',
                description: '現實不變知識 - 跨環境規律、跨語言語意、跨文化結構、跨系統策略提取',
                result: {
                    invariantKnowledge: invariantKnowledge.getAllInvariantKnowledge().length,
                    extractionHistory: invariantKnowledge.getExtractionHistory().length,
                    applicationHistory: invariantKnowledge.getApplicationHistory().length
                }
            });
            interRealityGovernance = interReality.getInterRealityGovernance();
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
 * Reality Model Abstraction Endpoints
 */
app.get('/api/v18/reality-abstraction/models', function (req, res) {
    var models = interReality.getRealityModelAbstraction().getRealityModels();
    res.json({ success: true, models: models });
});
app.post('/api/v18/reality-abstraction/register', function (req, res) {
    var model = req.body.model;
    interReality.getRealityModelAbstraction().registerRealityModel(model);
    res.json({ success: true, message: 'Reality model registered' });
});
app.post('/api/v18/reality-abstraction/abstract', function (req, res) { return __awaiter(_this, void 0, void 0, function () {
    var realityId, result;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                realityId = req.body.realityId;
                return [4 /*yield*/, interReality.getRealityModelAbstraction().abstractReality(realityId)];
            case 1:
                result = _a.sent();
                res.json({ success: result.success, result: result });
                return [2 /*return*/];
        }
    });
}); });
app.post('/api/v18/reality-abstraction/switch', function (req, res) { return __awaiter(_this, void 0, void 0, function () {
    var _a, fromRealityId, toRealityId, result;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = req.body, fromRealityId = _a.fromRealityId, toRealityId = _a.toRealityId;
                return [4 /*yield*/, interReality.getRealityModelAbstraction().switchReality(fromRealityId, toRealityId)];
            case 1:
                result = _b.sent();
                res.json({ success: result, message: result ? 'Reality switched' : 'Switch failed' });
                return [2 /*return*/];
        }
    });
}); });
/**
 * Multi-Reality Mapping Endpoints
 */
app.get('/api/v18/multi-reality/mappings', function (req, res) {
    var mappings = interReality.getMultiRealityMapping().getRealityMappings();
    res.json({ success: true, mappings: mappings });
});
app.post('/api/v18/multi-reality/map', function (req, res) { return __awaiter(_this, void 0, void 0, function () {
    var _a, sourceReality, targetReality, type, result;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = req.body, sourceReality = _a.sourceReality, targetReality = _a.targetReality, type = _a.type;
                return [4 /*yield*/, interReality.getMultiRealityMapping().createMapping(sourceReality, targetReality, type)];
            case 1:
                result = _b.sent();
                res.json({ success: result.success, result: result });
                return [2 /*return*/];
        }
    });
}); });
app.post('/api/v18/multi-reality/transfer', function (req, res) { return __awaiter(_this, void 0, void 0, function () {
    var _a, sourceReality, targetReality, element, result;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = req.body, sourceReality = _a.sourceReality, targetReality = _a.targetReality, element = _a.element;
                return [4 /*yield*/, interReality.getMultiRealityMapping().transferElement(sourceReality, targetReality, element)];
            case 1:
                result = _b.sent();
                res.json({ success: result.success, result: result });
                return [2 /*return*/];
        }
    });
}); });
app.post('/api/v18/multi-reality/bidirectional', function (req, res) { return __awaiter(_this, void 0, void 0, function () {
    var mappingId, result;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                mappingId = req.body.mappingId;
                return [4 /*yield*/, interReality.getMultiRealityMapping().makeBidirectional(mappingId)];
            case 1:
                result = _a.sent();
                res.json({ success: result, message: result ? 'Mapping made bidirectional' : 'Failed' });
                return [2 /*return*/];
        }
    });
}); });
/**
 * Adaptive Reasoning Endpoints
 */
app.get('/api/v18/adaptive-reasoning/contexts', function (req, res) {
    var contexts = interReality.getAdaptiveReasoning().getRealityContexts();
    res.json({ success: true, contexts: contexts });
});
app.post('/api/v18/adaptive-reasoning/register', function (req, res) {
    var context = req.body.context;
    interReality.getAdaptiveReasoning().registerRealityContext(context);
    res.json({ success: true, message: 'Reality context registered' });
});
app.post('/api/v18/adaptive-reasoning/adapt', function (req, res) { return __awaiter(_this, void 0, void 0, function () {
    var realityId, result;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                realityId = req.body.realityId;
                return [4 /*yield*/, interReality.getAdaptiveReasoning().adaptToReality(realityId)];
            case 1:
                result = _a.sent();
                res.json({ success: result.success, result: result });
                return [2 /*return*/];
        }
    });
}); });
/**
 * Cross-Reality Consistency Endpoints
 */
app.get('/api/v18/cross-reality-consistency/checks', function (req, res) {
    var checks = interReality.getCrossRealityConsistency().getConsistencyChecks('reasoning');
    res.json({ success: true, checks: checks });
});
app.post('/api/v18/cross-reality-consistency/check', function (req, res) { return __awaiter(_this, void 0, void 0, function () {
    var _a, realityIds, type, data, result, _b;
    return __generator(this, function (_c) {
        switch (_c.label) {
            case 0:
                _a = req.body, realityIds = _a.realityIds, type = _a.type, data = _a.data;
                _b = type;
                switch (_b) {
                    case 'reasoning': return [3 /*break*/, 1];
                    case 'semantic': return [3 /*break*/, 3];
                    case 'strategy': return [3 /*break*/, 5];
                    case 'civilization': return [3 /*break*/, 7];
                    case 'evolution': return [3 /*break*/, 9];
                }
                return [3 /*break*/, 11];
            case 1: return [4 /*yield*/, interReality.getCrossRealityConsistency().checkReasoningConsistency(realityIds, data)];
            case 2:
                result = _c.sent();
                return [3 /*break*/, 12];
            case 3: return [4 /*yield*/, interReality.getCrossRealityConsistency().checkSemanticConsistency(realityIds, data)];
            case 4:
                result = _c.sent();
                return [3 /*break*/, 12];
            case 5: return [4 /*yield*/, interReality.getCrossRealityConsistency().checkStrategyConsistency(realityIds, data)];
            case 6:
                result = _c.sent();
                return [3 /*break*/, 12];
            case 7: return [4 /*yield*/, interReality.getCrossRealityConsistency().checkCivilizationConsistency(realityIds, data)];
            case 8:
                result = _c.sent();
                return [3 /*break*/, 12];
            case 9: return [4 /*yield*/, interReality.getCrossRealityConsistency().checkEvolutionConsistency(realityIds, data)];
            case 10:
                result = _c.sent();
                return [3 /*break*/, 12];
            case 11:
                res.status(400).json({ success: false, error: 'Invalid consistency type' });
                return [2 /*return*/];
            case 12:
                res.json({ success: true, result: result });
                return [2 /*return*/];
        }
    });
}); });
app.post('/api/v18/cross-reality-consistency/snapshot', function (req, res) { return __awaiter(_this, void 0, void 0, function () {
    var realityIds, snapshot;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                realityIds = req.body.realityIds;
                return [4 /*yield*/, interReality.getCrossRealityConsistency().createSnapshot(realityIds)];
            case 1:
                snapshot = _a.sent();
                res.json({ success: true, snapshot: snapshot });
                return [2 /*return*/];
        }
    });
}); });
/**
 * Invariant Knowledge Endpoints
 */
app.get('/api/v18/invariant-knowledge/all', function (req, res) {
    var knowledge = interReality.getInvariantKnowledge().getAllInvariantKnowledge();
    res.json({ success: true, knowledge: knowledge });
});
app.post('/api/v18/invariant-knowledge/extract', function (req, res) { return __awaiter(_this, void 0, void 0, function () {
    var _a, realityIds, type, result;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = req.body, realityIds = _a.realityIds, type = _a.type;
                return [4 /*yield*/, interReality.getInvariantKnowledge().extractInvariantKnowledge(realityIds, type)];
            case 1:
                result = _b.sent();
                res.json({ success: true, result: result });
                return [2 /*return*/];
        }
    });
}); });
app.post('/api/v18/invariant-knowledge/apply', function (req, res) { return __awaiter(_this, void 0, void 0, function () {
    var _a, knowledgeId, targetReality, result;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = req.body, knowledgeId = _a.knowledgeId, targetReality = _a.targetReality;
                return [4 /*yield*/, interReality.getInvariantKnowledge().applyInvariantKnowledge(knowledgeId, targetReality)];
            case 1:
                result = _b.sent();
                res.json({ success: true, result: result });
                return [2 /*return*/];
        }
    });
}); });
/**
 * Inter-Reality Governance Endpoints
 */
app.get('/api/v18/inter-reality-governance/scopes', function (req, res) {
    var scopes = interReality.getInterRealityGovernance().getGovernanceScopes();
    res.json({ success: true, scopes: scopes });
});
app.post('/api/v18/inter-reality-governance/register', function (req, res) {
    var scope = req.body.scope;
    interReality.getInterRealityGovernance().registerGovernanceScope(scope);
    res.json({ success: true, message: 'Governance scope registered' });
});
app.post('/api/v18/inter-reality-governance/enforce', function (req, res) { return __awaiter(_this, void 0, void 0, function () {
    var _a, ruleId, affectedRealities, context, result;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = req.body, ruleId = _a.ruleId, affectedRealities = _a.affectedRealities, context = _a.context;
                return [4 /*yield*/, interReality.getInterRealityGovernance().enforceRule(ruleId, affectedRealities, context)];
            case 1:
                result = _b.sent();
                res.json({ success: true, result: result });
                return [2 /*return*/];
        }
    });
}); });
app.get('/api/v18/inter-reality-governance/topology', function (req, res) { return __awaiter(_this, void 0, void 0, function () {
    var topology;
    return __generator(this, function (_a) {
        topology = interReality.getInterRealityGovernance().getGovernanceTopology();
        res.json({ success: true, topology: topology });
        return [2 /*return*/];
    });
}); });
app.get('/api/v18/inter-reality-governance/collaboration', function (req, res) { return __awaiter(_this, void 0, void 0, function () {
    var matrix;
    return __generator(this, function (_a) {
        matrix = interReality.getInterRealityGovernance().getCollaborationMatrix();
        res.json({ success: true, matrix: matrix });
        return [2 /*return*/];
    });
}); });
app.post('/api/v18/inter-reality-governance/snapshot', function (req, res) { return __awaiter(_this, void 0, void 0, function () {
    var snapshot;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0: return [4 /*yield*/, interReality.getInterRealityGovernance().createSnapshot()];
            case 1:
                snapshot = _a.sent();
                res.json({ success: true, snapshot: snapshot });
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
                    // Initialize inter-reality architecture
                    return [4 /*yield*/, interReality.initialize()];
                case 1:
                    // Initialize inter-reality architecture
                    _a.sent();
                    // Start server
                    app.listen(PORT, function () {
                        console.log("\uD83C\uDF0C GL Inter-Reality Integration Architecture API Server");
                        console.log("   Version: 18.0.0");
                        console.log("   Port: ".concat(PORT));
                        console.log("   Philosophy: \u667A\u6167\u7684\u8DE8\u6846\u67B6\u7A69\u5B9A\u6027\u968E\u6BB5");
                        console.log("   Status: Active");
                        console.log('');
                        console.log("   Endpoints:");
                        console.log("   - GET  /health");
                        console.log("   - GET  /api/v18/inter-reality/status");
                        console.log("   - GET  /api/v18/inter-reality/demonstrate");
                        console.log("   - GET  /api/v18/reality-abstraction/*");
                        console.log("   - GET  /api/v18/multi-reality/*");
                        console.log("   - GET  /api/v18/adaptive-reasoning/*");
                        console.log("   - GET  /api/v18/cross-reality-consistency/*");
                        console.log("   - GET  /api/v18/invariant-knowledge/*");
                        console.log("   - GET  /api/v18/inter-reality-governance/*");
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
