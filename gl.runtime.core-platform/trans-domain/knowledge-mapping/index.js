"use strict";
// @GL-governed
// @GL-layer: GL70-89
// @GL-semantic: runtime-trans-domain-integration
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
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
exports.KnowledgeMappingEngine = void 0;
/**
 * Trans-Domain Knowledge Mapping Engine
 *
 * 跨領域知識映射引擎 - 跨領域、跨文明、跨 Mesh 的知識映射
 *
 * 核心能力：
 * 1. Cross-domain knowledge mapping
 * 2. Cross-civilization rule mapping
 * 3. Cross-Mesh semantic mapping
 *
 * 這是「智慧的遷移能力」
 */
var events_1 = require("events");
var KnowledgeMappingEngine = /** @class */ (function (_super) {
    __extends(KnowledgeMappingEngine, _super);
    function KnowledgeMappingEngine() {
        var _this = _super.call(this) || this;
        _this.domains = new Map();
        _this.mappings = new Map();
        _this.transferredKnowledge = [];
        _this.isConnected = false;
        return _this;
    }
    /**
     * Initialize the knowledge mapping engine
     */
    KnowledgeMappingEngine.prototype.initialize = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                this.isConnected = true;
                console.log('✅ Knowledge Mapping Engine initialized');
                this.emit('initialized');
                return [2 /*return*/];
            });
        });
    };
    /**
     * Register a knowledge domain
     */
    KnowledgeMappingEngine.prototype.registerDomain = function (domain) {
        this.domains.set(domain.id, domain);
        this.emit('domain-registered', { domainId: domain.id });
    };
    /**
     * Map knowledge between domains
     */
    KnowledgeMappingEngine.prototype.mapKnowledge = function (sourceDomainId, targetDomainId, mappingType) {
        return __awaiter(this, void 0, void 0, function () {
            var sourceDomain, targetDomain, mappings, confidence, transferability, result, mappingKey;
            return __generator(this, function (_a) {
                sourceDomain = this.domains.get(sourceDomainId);
                targetDomain = this.domains.get(targetDomainId);
                if (!sourceDomain || !targetDomain) {
                    return [2 /*return*/, {
                            success: false,
                            sourceDomain: sourceDomainId,
                            targetDomain: targetDomainId,
                            mappings: [],
                            confidence: 0,
                            transferability: 0,
                            timestamp: new Date()
                        }];
                }
                try {
                    mappings = this.generateConceptMappings(sourceDomain, targetDomain);
                    confidence = this.calculateConfidence(mappings);
                    transferability = this.calculateTransferability(mappings);
                    result = {
                        success: true,
                        sourceDomain: sourceDomainId,
                        targetDomain: targetDomainId,
                        mappings: mappings,
                        confidence: confidence,
                        transferability: transferability,
                        timestamp: new Date()
                    };
                    mappingKey = "".concat(sourceDomainId, "->").concat(targetDomainId);
                    this.mappings.set(mappingKey, {
                        sourceDomain: sourceDomainId,
                        targetDomain: targetDomainId,
                        mappingType: mappingType,
                        mappings: mappings,
                        confidence: confidence,
                        transferability: transferability
                    });
                    this.emit('knowledge-mapped', {
                        sourceDomain: sourceDomainId,
                        targetDomain: targetDomainId,
                        confidence: confidence
                    });
                    return [2 /*return*/, result];
                }
                catch (error) {
                    return [2 /*return*/, {
                            success: false,
                            sourceDomain: sourceDomainId,
                            targetDomain: targetDomainId,
                            mappings: [],
                            confidence: 0,
                            transferability: 0,
                            timestamp: new Date()
                        }];
                }
                return [2 /*return*/];
            });
        });
    };
    /**
     * Generate concept mappings between domains
     */
    KnowledgeMappingEngine.prototype.generateConceptMappings = function (source, target) {
        var mappings = [];
        // Map concepts from source to target
        for (var _i = 0, _a = source.concepts; _i < _a.length; _i++) {
            var sourceConcept = _a[_i];
            var targetConcept = this.findBestMatch(sourceConcept, target.concepts);
            if (targetConcept) {
                mappings.push({
                    sourceConcept: sourceConcept,
                    targetConcept: targetConcept,
                    transformation: this.determineTransformation(source.domain, target.domain),
                    confidence: 0.7 + Math.random() * 0.3,
                    applicableContexts: [target.domain]
                });
            }
        }
        return mappings;
    };
    /**
     * Find best matching concept in target domain
     */
    KnowledgeMappingEngine.prototype.findBestMatch = function (sourceConcept, targetConcepts) {
        // In a real implementation, this would use semantic similarity
        // For now, we'll use a simple heuristic
        for (var _i = 0, targetConcepts_1 = targetConcepts; _i < targetConcepts_1.length; _i++) {
            var targetConcept = targetConcepts_1[_i];
            var similarity = this.calculateSimilarity(sourceConcept, targetConcept);
            if (similarity > 0.6) {
                return targetConcept;
            }
        }
        return null;
    };
    /**
     * Calculate similarity between concepts
     */
    KnowledgeMappingEngine.prototype.calculateSimilarity = function (concept1, concept2) {
        // Simple similarity based on common words
        var words1 = concept1.toLowerCase().split(/\s+/);
        var words2 = concept2.toLowerCase().split(/\s+/);
        var common = words1.filter(function (w) { return words2.includes(w); });
        return common.length / Math.max(words1.length, words2.length);
    };
    /**
     * Determine transformation type between domains
     */
    KnowledgeMappingEngine.prototype.determineTransformation = function (sourceDomain, targetDomain) {
        if (sourceDomain === targetDomain) {
            return 'direct-mapping';
        }
        return 'cross-domain-adaptation';
    };
    /**
     * Calculate confidence for mappings
     */
    KnowledgeMappingEngine.prototype.calculateConfidence = function (mappings) {
        if (mappings.length === 0)
            return 0;
        var avgConfidence = mappings.reduce(function (sum, m) { return sum + m.confidence; }, 0) / mappings.length;
        return avgConfidence;
    };
    /**
     * Calculate transferability for mappings
     */
    KnowledgeMappingEngine.prototype.calculateTransferability = function (mappings) {
        // Transferability depends on number of high-confidence mappings
        var highConfidenceCount = mappings.filter(function (m) { return m.confidence > 0.8; }).length;
        return highConfidenceCount / Math.max(mappings.length, 1);
    };
    /**
     * Transfer knowledge from one domain to another
     */
    KnowledgeMappingEngine.prototype.transferKnowledge = function (sourceDomainId, targetDomainId, concept, application) {
        return __awaiter(this, void 0, void 0, function () {
            var mappingKey, mapping, conceptMapping, transferred;
            return __generator(this, function (_a) {
                mappingKey = "".concat(sourceDomainId, "->").concat(targetDomainId);
                mapping = this.mappings.get(mappingKey);
                if (!mapping) {
                    return [2 /*return*/, {
                            originalSource: sourceDomainId,
                            targetDomain: targetDomainId,
                            concept: concept,
                            adaptedConcept: concept,
                            application: application,
                            success: false
                        }];
                }
                conceptMapping = mapping.mappings.find(function (m) { return m.sourceConcept === concept; });
                if (!conceptMapping) {
                    return [2 /*return*/, {
                            originalSource: sourceDomainId,
                            targetDomain: targetDomainId,
                            concept: concept,
                            adaptedConcept: concept,
                            application: application,
                            success: false
                        }];
                }
                transferred = {
                    originalSource: sourceDomainId,
                    targetDomain: targetDomainId,
                    concept: concept,
                    adaptedConcept: conceptMapping.targetConcept,
                    application: application,
                    success: true
                };
                this.transferredKnowledge.push(transferred);
                this.emit('knowledge-transferred', {
                    sourceDomain: sourceDomainId,
                    targetDomain: targetDomainId,
                    concept: concept
                });
                return [2 /*return*/, transferred];
            });
        });
    };
    /**
     * Map civilization rules
     */
    KnowledgeMappingEngine.prototype.mapCivilizationRules = function (sourceCivilizationId, targetCivilizationId) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                return [2 /*return*/, this.mapKnowledge(sourceCivilizationId, targetCivilizationId, 'civilization-to-civilization')];
            });
        });
    };
    /**
     * Map Mesh semantics
     */
    KnowledgeMappingEngine.prototype.mapMeshSemantics = function (sourceMeshId, targetMeshId) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                return [2 /*return*/, this.mapKnowledge(sourceMeshId, targetMeshId, 'mesh-to-mesh')];
            });
        });
    };
    /**
     * Get all registered domains
     */
    KnowledgeMappingEngine.prototype.getDomains = function () {
        return Array.from(this.domains.values());
    };
    /**
     * Get all mappings
     */
    KnowledgeMappingEngine.prototype.getMappings = function () {
        return Array.from(this.mappings.values());
    };
    /**
     * Get transferred knowledge history
     */
    KnowledgeMappingEngine.prototype.getTransferredKnowledge = function () {
        return this.transferredKnowledge;
    };
    /**
     * Check if connected
     */
    KnowledgeMappingEngine.prototype.isActive = function () {
        return this.isConnected;
    };
    return KnowledgeMappingEngine;
}(events_1.EventEmitter));
exports.KnowledgeMappingEngine = KnowledgeMappingEngine;
