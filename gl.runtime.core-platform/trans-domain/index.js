"use strict";
// @GL-governed
// @GL-layer: GL70-89
// @GL-semantic: runtime-trans-domain-integration
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../engine/governance/GL_SEMANTIC_ANCHOR.json
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
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
exports.TransDomainStabilityEngine = exports.UniversalInterfaceLayer = exports.InterSystemGovernanceEngine = exports.KnowledgeMappingEngine = exports.MultiModelAlignmentEngine = exports.CrossSystemIntegrationEngine = exports.GLTransDomainArchitecture = void 0;
/**
 * GL Trans-Domain Integration Architecture (Version 17.0.0)
 *
 * 跨域整合架構 - 智慧的外延擴張階段
 *
 * 核心定位：
 * - 整合所有「外部系統、外部知識、外部模型、外部文明」的能力
 * - 跨域推理、跨域協作、跨域治理的能力
 * - 保持跨域推理的一致性、穩定性、可解釋性
 *
 * 六大核心能力：
 * 1. Cross-System Integration - 智慧的互通性
 * 2. Multi-Model Alignment - 智慧的兼容性
 * 3. Trans-Domain Knowledge Mapping - 智慧的遷移能力
 * 4. Inter-System Governance - 智慧的協調能力
 * 5. Universal Interface Layer - 智慧的語言
 * 6. Trans-Domain Stability Engine - 智慧的穩定性
 *
 * 這不是「超越智慧」，而是「智慧的外延擴張」
 */
var events_1 = require("events");
var cross_system_integration_1 = require("./cross-system-integration");
var multi_model_alignment_1 = require("./multi-model-alignment");
var knowledge_mapping_1 = require("./knowledge-mapping");
var inter_system_governance_1 = require("./inter-system-governance");
var universal_interface_1 = require("./universal-interface");
var stability_engine_1 = require("./stability-engine");
var GLTransDomainArchitecture = /** @class */ (function (_super) {
    __extends(GLTransDomainArchitecture, _super);
    function GLTransDomainArchitecture() {
        var _this = _super.call(this) || this;
        // Initialize all six engines
        _this.crossSystemIntegration = new cross_system_integration_1.CrossSystemIntegrationEngine();
        _this.multiModelAlignment = new multi_model_alignment_1.MultiModelAlignmentEngine();
        _this.knowledgeMapping = new knowledge_mapping_1.KnowledgeMappingEngine();
        _this.interSystemGovernance = new inter_system_governance_1.InterSystemGovernanceEngine();
        _this.universalInterface = new universal_interface_1.UniversalInterfaceLayer();
        _this.stabilityEngine = new stability_engine_1.TransDomainStabilityEngine();
        _this.isInitialized = false;
        // Forward events from all engines
        _this.setupEventForwarding();
        return _this;
    }
    /**
     * Setup event forwarding from all engines
     */
    GLTransDomainArchitecture.prototype.setupEventForwarding = function () {
        var _this = this;
        var engines = [
            this.crossSystemIntegration,
            this.multiModelAlignment,
            this.knowledgeMapping,
            this.interSystemGovernance,
            this.universalInterface,
            this.stabilityEngine
        ];
        for (var _i = 0, engines_1 = engines; _i < engines_1.length; _i++) {
            var engine = engines_1[_i];
            engine.on('initialized', function () { return _this.emit('component-initialized'); });
            engine.on('*', function (event, data) { return _this.emit(event, data); });
        }
    };
    /**
     * Initialize the trans-domain architecture
     */
    GLTransDomainArchitecture.prototype.initialize = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        console.log('🌌 Initializing GL Trans-Domain Integration Architecture (v17.0.0)...');
                        // Initialize all engines
                        return [4 /*yield*/, Promise.all([
                                this.crossSystemIntegration.initialize(),
                                this.multiModelAlignment.initialize(),
                                this.knowledgeMapping.initialize(),
                                this.interSystemGovernance.initialize(),
                                this.universalInterface.initialize(),
                                this.stabilityEngine.initialize()
                            ])];
                    case 1:
                        // Initialize all engines
                        _a.sent();
                        this.isInitialized = true;
                        console.log('✅ GL Trans-Domain Integration Architecture initialized');
                        this.emit('initialized');
                        return [2 /*return*/];
                }
            });
        });
    };
    /**
     * Get system status
     */
    GLTransDomainArchitecture.prototype.getStatus = function () {
        return {
            crossSystemIntegration: this.crossSystemIntegration.isActive(),
            multiModelAlignment: this.multiModelAlignment.isActive(),
            knowledgeMapping: this.knowledgeMapping.isActive(),
            interSystemGovernance: this.interSystemGovernance.isActive(),
            universalInterface: this.universalInterface.isActive(),
            stabilityEngine: this.stabilityEngine.isActive(),
            overall: this.isInitialized
        };
    };
    /**
     * Get comprehensive statistics
     */
    GLTransDomainArchitecture.prototype.getStatistics = function () {
        var externalSystems = this.crossSystemIntegration.getExternalSystems().length;
        var registeredModels = this.multiModelAlignment.getRegisteredModels().length;
        var knowledgeDomains = this.knowledgeMapping.getDomains().length;
        var governanceScopes = this.interSystemGovernance.getScopes().length;
        var activeConnections = this.universalInterface.getActiveConnections().size;
        var stabilityChecks = this.stabilityEngine.getCheckHistory().length;
        var consistencyViolations = this.stabilityEngine.getViolations().filter(function (v) { return !v.resolved; }).length;
        // Calculate overall coherence
        var overallCoherence = this.calculateOverallCoherence(externalSystems, registeredModels, knowledgeDomains, governanceScopes, activeConnections, stabilityChecks, consistencyViolations);
        return {
            externalSystems: externalSystems,
            registeredModels: registeredModels,
            knowledgeDomains: knowledgeDomains,
            governanceScopes: governanceScopes,
            activeConnections: activeConnections,
            stabilityChecks: stabilityChecks,
            consistencyViolations: consistencyViolations,
            overallCoherence: overallCoherence
        };
    };
    /**
     * Calculate overall coherence score
     */
    GLTransDomainArchitecture.prototype.calculateOverallCoherence = function (externalSystems, registeredModels, knowledgeDomains, governanceScopes, activeConnections, stabilityChecks, consistencyViolations) {
        // Base score
        var score = 0.5;
        // Bonus for integration
        score += Math.min(externalSystems / 10, 0.1);
        score += Math.min(registeredModels / 10, 0.1);
        score += Math.min(knowledgeDomains / 10, 0.1);
        score += Math.min(governanceScopes / 10, 0.1);
        score += Math.min(activeConnections / 10, 0.1);
        // Bonus for stability monitoring
        if (stabilityChecks > 0) {
            score += 0.05;
        }
        // Penalty for violations
        var violationPenalty = Math.min(consistencyViolations / 10, 0.1);
        score -= violationPenalty;
        // Clamp to [0, 1]
        return Math.max(0, Math.min(1, score));
    };
    /**
     * Get access to individual engines
     */
    GLTransDomainArchitecture.prototype.getCrossSystemIntegration = function () {
        return this.crossSystemIntegration;
    };
    GLTransDomainArchitecture.prototype.getMultiModelAlignment = function () {
        return this.multiModelAlignment;
    };
    GLTransDomainArchitecture.prototype.getKnowledgeMapping = function () {
        return this.knowledgeMapping;
    };
    GLTransDomainArchitecture.prototype.getInterSystemGovernance = function () {
        return this.interSystemGovernance;
    };
    GLTransDomainArchitecture.prototype.getUniversalInterface = function () {
        return this.universalInterface;
    };
    GLTransDomainArchitecture.prototype.getStabilityEngine = function () {
        return this.stabilityEngine;
    };
    /**
     * Check if initialized
     */
    GLTransDomainArchitecture.prototype.isActive = function () {
        return this.isInitialized;
    };
    return GLTransDomainArchitecture;
}(events_1.EventEmitter));
exports.GLTransDomainArchitecture = GLTransDomainArchitecture;
// Export all components
var cross_system_integration_2 = require("./cross-system-integration");
Object.defineProperty(exports, "CrossSystemIntegrationEngine", { enumerable: true, get: function () { return cross_system_integration_2.CrossSystemIntegrationEngine; } });
var multi_model_alignment_2 = require("./multi-model-alignment");
Object.defineProperty(exports, "MultiModelAlignmentEngine", { enumerable: true, get: function () { return multi_model_alignment_2.MultiModelAlignmentEngine; } });
var knowledge_mapping_2 = require("./knowledge-mapping");
Object.defineProperty(exports, "KnowledgeMappingEngine", { enumerable: true, get: function () { return knowledge_mapping_2.KnowledgeMappingEngine; } });
var inter_system_governance_2 = require("./inter-system-governance");
Object.defineProperty(exports, "InterSystemGovernanceEngine", { enumerable: true, get: function () { return inter_system_governance_2.InterSystemGovernanceEngine; } });
var universal_interface_2 = require("./universal-interface");
Object.defineProperty(exports, "UniversalInterfaceLayer", { enumerable: true, get: function () { return universal_interface_2.UniversalInterfaceLayer; } });
var stability_engine_2 = require("./stability-engine");
Object.defineProperty(exports, "TransDomainStabilityEngine", { enumerable: true, get: function () { return stability_engine_2.TransDomainStabilityEngine; } });
