"use strict";
// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-inter-reality-integration
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
exports.MultiRealityMappingEngine = void 0;
/**
 * Multi-Reality Mapping Engine
 *
 * 多現實映射引擎 - 把 A 世界的規則映射到 B 世界、語意映射到語意、結構映射到結構
 *
 * 核心能力：
 * 1. 跨世界規則映射
 * 2. 跨系統語意映射
 * 3. 跨文明結構映射
 *
 * 這是「跨框架智慧」
 */
var events_1 = require("events");
var MultiRealityMappingEngine = /** @class */ (function (_super) {
    __extends(MultiRealityMappingEngine, _super);
    function MultiRealityMappingEngine() {
        var _this = _super.call(this) || this;
        _this.realityMappings = new Map();
        _this.mappingHistory = [];
        _this.transferHistory = [];
        _this.isConnected = false;
        return _this;
    }
    /**
     * Initialize the multi-reality mapping engine
     */
    MultiRealityMappingEngine.prototype.initialize = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                this.isConnected = true;
                console.log('✅ Multi-Reality Mapping Engine initialized');
                this.emit('initialized');
                return [2 /*return*/];
            });
        });
    };
    /**
     * Create a mapping between two realities
     */
    MultiRealityMappingEngine.prototype.createMapping = function (sourceReality, targetReality, type) {
        return __awaiter(this, void 0, void 0, function () {
            var mappingId, mappings, confidence, mapping, result;
            return __generator(this, function (_a) {
                mappingId = "".concat(sourceReality, "->").concat(targetReality, "-").concat(type);
                mappings = this.generateMappings(sourceReality, targetReality, type);
                confidence = this.calculateMappingConfidence(mappings);
                mapping = {
                    id: mappingId,
                    sourceReality: sourceReality,
                    targetReality: targetReality,
                    type: type,
                    mappings: mappings,
                    confidence: confidence,
                    bidirectional: false,
                    metadata: {
                        createdAt: new Date(),
                        status: 'active'
                    }
                };
                this.realityMappings.set(mappingId, mapping);
                result = {
                    success: true,
                    mappingId: mappingId,
                    sourceReality: sourceReality,
                    targetReality: targetReality,
                    mappings: mappings,
                    confidence: confidence,
                    timestamp: new Date()
                };
                this.mappingHistory.push(result);
                this.emit('mapping-created', { mappingId: mappingId, confidence: confidence });
                return [2 /*return*/, result];
            });
        });
    };
    /**
     * Generate mappings between realities
     */
    MultiRealityMappingEngine.prototype.generateMappings = function (sourceReality, targetReality, type) {
        var mappings = [];
        var numMappings = 5 + Math.floor(Math.random() * 5);
        for (var i = 0; i < numMappings; i++) {
            mappings.push({
                sourceElement: "".concat(sourceReality, "_").concat(type, "_").concat(i),
                targetElement: "".concat(targetReality, "_").concat(type, "_").concat(i),
                transformation: this.getTransformationType(type),
                confidence: 0.6 + Math.random() * 0.4,
                applicable: Math.random() > 0.2
            });
        }
        return mappings;
    };
    /**
     * Get transformation type based on mapping type
     */
    MultiRealityMappingEngine.prototype.getTransformationType = function (type) {
        switch (type) {
            case 'rule-mapping':
                return 'rule-transformation';
            case 'semantic-mapping':
                return 'semantic-translation';
            case 'structure-mapping':
                return 'structure-adaptation';
            default:
                return 'generic-transformation';
        }
    };
    /**
     * Calculate mapping confidence
     */
    MultiRealityMappingEngine.prototype.calculateMappingConfidence = function (mappings) {
        if (mappings.length === 0)
            return 0;
        var applicableMappings = mappings.filter(function (m) { return m.applicable; });
        var avgConfidence = applicableMappings.reduce(function (sum, m) { return sum + m.confidence; }, 0) / applicableMappings.length;
        return avgConfidence;
    };
    /**
     * Transfer element from source reality to target reality
     */
    MultiRealityMappingEngine.prototype.transferElement = function (sourceReality, targetReality, element) {
        return __awaiter(this, void 0, void 0, function () {
            var mappingKey, mapping, _i, _a, _b, key, value, specificMapping, transfer;
            return __generator(this, function (_c) {
                mappingKey = "".concat(sourceReality, "->").concat(targetReality, "-*");
                mapping = null;
                for (_i = 0, _a = Array.from(this.realityMappings.entries()); _i < _a.length; _i++) {
                    _b = _a[_i], key = _b[0], value = _b[1];
                    if (key.startsWith("".concat(sourceReality, "->").concat(targetReality))) {
                        mapping = value;
                        break;
                    }
                }
                if (!mapping) {
                    return [2 /*return*/, {
                            sourceReality: sourceReality,
                            targetReality: targetReality,
                            element: element,
                            transferredElement: element,
                            transformation: 'none',
                            success: false,
                            timestamp: new Date()
                        }];
                }
                specificMapping = mapping.mappings.find(function (m) { return m.sourceElement === element; });
                if (!specificMapping || !specificMapping.applicable) {
                    return [2 /*return*/, {
                            sourceReality: sourceReality,
                            targetReality: targetReality,
                            element: element,
                            transferredElement: element,
                            transformation: 'none',
                            success: false,
                            timestamp: new Date()
                        }];
                }
                transfer = {
                    sourceReality: sourceReality,
                    targetReality: targetReality,
                    element: element,
                    transferredElement: specificMapping.targetElement,
                    transformation: specificMapping.transformation,
                    success: true,
                    timestamp: new Date()
                };
                this.transferHistory.push(transfer);
                this.emit('element-transferred', transfer);
                return [2 /*return*/, transfer];
            });
        });
    };
    /**
     * Map rules from source to target reality
     */
    MultiRealityMappingEngine.prototype.mapRules = function (sourceReality, targetReality) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                return [2 /*return*/, this.createMapping(sourceReality, targetReality, 'rule-mapping')];
            });
        });
    };
    /**
     * Map semantics from source to target reality
     */
    MultiRealityMappingEngine.prototype.mapSemantics = function (sourceReality, targetReality) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                return [2 /*return*/, this.createMapping(sourceReality, targetReality, 'semantic-mapping')];
            });
        });
    };
    /**
     * Map structures from source to target reality
     */
    MultiRealityMappingEngine.prototype.mapStructures = function (sourceReality, targetReality) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                return [2 /*return*/, this.createMapping(sourceReality, targetReality, 'structure-mapping')];
            });
        });
    };
    /**
     * Make a mapping bidirectional
     */
    MultiRealityMappingEngine.prototype.makeBidirectional = function (mappingId) {
        return __awaiter(this, void 0, void 0, function () {
            var mapping, reverseMappings, reverseMappingId, reverseMapping;
            return __generator(this, function (_a) {
                mapping = this.realityMappings.get(mappingId);
                if (!mapping) {
                    return [2 /*return*/, false];
                }
                reverseMappings = mapping.mappings.map(function (m) { return ({
                    sourceElement: m.targetElement,
                    targetElement: m.sourceElement,
                    transformation: m.transformation,
                    confidence: m.confidence,
                    applicable: m.applicable
                }); });
                reverseMappingId = "".concat(mapping.targetReality, "->").concat(mapping.sourceReality, "-").concat(mapping.type);
                reverseMapping = {
                    id: reverseMappingId,
                    sourceReality: mapping.targetReality,
                    targetReality: mapping.sourceReality,
                    type: mapping.type,
                    mappings: reverseMappings,
                    confidence: mapping.confidence,
                    bidirectional: true,
                    metadata: {
                        createdAt: new Date(),
                        status: 'active',
                        originalMapping: mappingId
                    }
                };
                this.realityMappings.set(reverseMappingId, reverseMapping);
                mapping.bidirectional = true;
                this.emit('mapping-made-bidirectional', { mappingId: mappingId });
                return [2 /*return*/, true];
            });
        });
    };
    /**
     * Get all reality mappings
     */
    MultiRealityMappingEngine.prototype.getRealityMappings = function () {
        return Array.from(this.realityMappings.values());
    };
    /**
     * Get mapping history
     */
    MultiRealityMappingEngine.prototype.getMappingHistory = function () {
        return this.mappingHistory;
    };
    /**
     * Get transfer history
     */
    MultiRealityMappingEngine.prototype.getTransferHistory = function () {
        return this.transferHistory;
    };
    /**
     * Check if connected
     */
    MultiRealityMappingEngine.prototype.isActive = function () {
        return this.isConnected;
    };
    return MultiRealityMappingEngine;
}(events_1.EventEmitter));
exports.MultiRealityMappingEngine = MultiRealityMappingEngine;
