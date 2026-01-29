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
exports.CrossRealityConsistencyEngine = void 0;
/**
 * Cross-Reality Consistency Engine
 *
 * 跨現實一致性引擎 - 確保推理、語意、策略、文明規則、演化軌跡在不同框架下保持一致
 *
 * 核心能力：
 * 1. 推理一致性檢查
 * 2. 語意一致性檢查
 * 3. 策略一致性檢查
 * 4. 文明規則一致性檢查
 * 5. 演化軌跡一致性檢查
 *
 * 即使在不同框架下，也能保持穩定
 */
var events_1 = require("events");
var CrossRealityConsistencyEngine = /** @class */ (function (_super) {
    __extends(CrossRealityConsistencyEngine, _super);
    function CrossRealityConsistencyEngine() {
        var _this = _super.call(this) || this;
        _this.consistencyChecks = new Map();
        _this.consistencySnapshots = [];
        _this.enforcementHistory = [];
        _this.thresholds = new Map();
        _this.isConnected = false;
        // Set default thresholds
        _this.thresholds.set('reasoning', 0.85);
        _this.thresholds.set('semantic', 0.90);
        _this.thresholds.set('strategy', 0.85);
        _this.thresholds.set('civilization', 0.90);
        _this.thresholds.set('evolution', 0.80);
        return _this;
    }
    /**
     * Initialize the cross-reality consistency engine
     */
    CrossRealityConsistencyEngine.prototype.initialize = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                this.isConnected = true;
                console.log('✅ Cross-Reality Consistency Engine initialized');
                this.emit('initialized');
                return [2 /*return*/];
            });
        });
    };
    /**
     * Check reasoning consistency across realities
     */
    CrossRealityConsistencyEngine.prototype.checkReasoningConsistency = function (realityIds, reasoningData) {
        return __awaiter(this, void 0, void 0, function () {
            var threshold, consistency, check;
            return __generator(this, function (_a) {
                threshold = this.thresholds.get('reasoning') || 0.85;
                consistency = this.calculateReasoningConsistency(realityIds, reasoningData);
                check = {
                    realityId: realityIds.join('+'),
                    type: 'reasoning',
                    consistency: consistency,
                    threshold: threshold,
                    status: consistency >= threshold ? 'consistent' : (consistency >= threshold * 0.8 ? 'warning' : 'inconsistent'),
                    violations: this.detectReasoningViolations(realityIds, reasoningData, consistency),
                    recommendations: this.generateReasoningRecommendations(consistency),
                    timestamp: new Date()
                };
                this.storeConsistencyCheck(check);
                this.emit('reasoning-consistency-checked', { consistency: consistency, status: check.status });
                return [2 /*return*/, check];
            });
        });
    };
    /**
     * Check semantic consistency across realities
     */
    CrossRealityConsistencyEngine.prototype.checkSemanticConsistency = function (realityIds, semanticData) {
        return __awaiter(this, void 0, void 0, function () {
            var threshold, consistency, check;
            return __generator(this, function (_a) {
                threshold = this.thresholds.get('semantic') || 0.90;
                consistency = this.calculateSemanticConsistency(realityIds, semanticData);
                check = {
                    realityId: realityIds.join('+'),
                    type: 'semantic',
                    consistency: consistency,
                    threshold: threshold,
                    status: consistency >= threshold ? 'consistent' : (consistency >= threshold * 0.8 ? 'warning' : 'inconsistent'),
                    violations: this.detectSemanticViolations(realityIds, semanticData, consistency),
                    recommendations: this.generateSemanticRecommendations(consistency),
                    timestamp: new Date()
                };
                this.storeConsistencyCheck(check);
                this.emit('semantic-consistency-checked', { consistency: consistency, status: check.status });
                return [2 /*return*/, check];
            });
        });
    };
    /**
     * Check strategy consistency across realities
     */
    CrossRealityConsistencyEngine.prototype.checkStrategyConsistency = function (realityIds, strategyData) {
        return __awaiter(this, void 0, void 0, function () {
            var threshold, consistency, check;
            return __generator(this, function (_a) {
                threshold = this.thresholds.get('strategy') || 0.85;
                consistency = this.calculateStrategyConsistency(realityIds, strategyData);
                check = {
                    realityId: realityIds.join('+'),
                    type: 'strategy',
                    consistency: consistency,
                    threshold: threshold,
                    status: consistency >= threshold ? 'consistent' : (consistency >= threshold * 0.8 ? 'warning' : 'inconsistent'),
                    violations: this.detectStrategyViolations(realityIds, strategyData, consistency),
                    recommendations: this.generateStrategyRecommendations(consistency),
                    timestamp: new Date()
                };
                this.storeConsistencyCheck(check);
                this.emit('strategy-consistency-checked', { consistency: consistency, status: check.status });
                return [2 /*return*/, check];
            });
        });
    };
    /**
     * Check civilization rules consistency across realities
     */
    CrossRealityConsistencyEngine.prototype.checkCivilizationConsistency = function (realityIds, civilizationData) {
        return __awaiter(this, void 0, void 0, function () {
            var threshold, consistency, check;
            return __generator(this, function (_a) {
                threshold = this.thresholds.get('civilization') || 0.90;
                consistency = this.calculateCivilizationConsistency(realityIds, civilizationData);
                check = {
                    realityId: realityIds.join('+'),
                    type: 'civilization',
                    consistency: consistency,
                    threshold: threshold,
                    status: consistency >= threshold ? 'consistent' : (consistency >= threshold * 0.8 ? 'warning' : 'inconsistent'),
                    violations: this.detectCivilizationViolations(realityIds, civilizationData, consistency),
                    recommendations: this.generateCivilizationRecommendations(consistency),
                    timestamp: new Date()
                };
                this.storeConsistencyCheck(check);
                this.emit('civilization-consistency-checked', { consistency: consistency, status: check.status });
                return [2 /*return*/, check];
            });
        });
    };
    /**
     * Check evolution trajectory consistency across realities
     */
    CrossRealityConsistencyEngine.prototype.checkEvolutionConsistency = function (realityIds, evolutionData) {
        return __awaiter(this, void 0, void 0, function () {
            var threshold, consistency, check;
            return __generator(this, function (_a) {
                threshold = this.thresholds.get('evolution') || 0.80;
                consistency = this.calculateEvolutionConsistency(realityIds, evolutionData);
                check = {
                    realityId: realityIds.join('+'),
                    type: 'evolution',
                    consistency: consistency,
                    threshold: threshold,
                    status: consistency >= threshold ? 'consistent' : (consistency >= threshold * 0.8 ? 'warning' : 'inconsistent'),
                    violations: this.detectEvolutionViolations(realityIds, evolutionData, consistency),
                    recommendations: this.generateEvolutionRecommendations(consistency),
                    timestamp: new Date()
                };
                this.storeConsistencyCheck(check);
                this.emit('evolution-consistency-checked', { consistency: consistency, status: check.status });
                return [2 /*return*/, check];
            });
        });
    };
    /**
     * Calculate reasoning consistency
     */
    CrossRealityConsistencyEngine.prototype.calculateReasoningConsistency = function (realityIds, data) {
        // Simulate consistency calculation
        return 0.7 + Math.random() * 0.3;
    };
    /**
     * Calculate semantic consistency
     */
    CrossRealityConsistencyEngine.prototype.calculateSemanticConsistency = function (realityIds, data) {
        // Simulate consistency calculation
        return 0.75 + Math.random() * 0.25;
    };
    /**
     * Calculate strategy consistency
     */
    CrossRealityConsistencyEngine.prototype.calculateStrategyConsistency = function (realityIds, data) {
        // Simulate consistency calculation
        return 0.65 + Math.random() * 0.35;
    };
    /**
     * Calculate civilization consistency
     */
    CrossRealityConsistencyEngine.prototype.calculateCivilizationConsistency = function (realityIds, data) {
        // Simulate consistency calculation
        return 0.8 + Math.random() * 0.2;
    };
    /**
     * Calculate evolution consistency
     */
    CrossRealityConsistencyEngine.prototype.calculateEvolutionConsistency = function (realityIds, data) {
        // Simulate consistency calculation
        return 0.6 + Math.random() * 0.4;
    };
    /**
     * Detect reasoning violations
     */
    CrossRealityConsistencyEngine.prototype.detectReasoningViolations = function (realityIds, data, consistency) {
        var violations = [];
        if (consistency < 0.7) {
            violations.push({
                id: "reasoning_violation_".concat(Date.now()),
                description: 'Low reasoning consistency across realities',
                severity: consistency < 0.5 ? 'critical' : 'high',
                context: { realityIds: realityIds, consistency: consistency },
                suggestedResolution: 'Align reasoning frameworks across realities'
            });
        }
        return violations;
    };
    /**
     * Detect semantic violations
     */
    CrossRealityConsistencyEngine.prototype.detectSemanticViolations = function (realityIds, data, consistency) {
        var violations = [];
        if (consistency < 0.75) {
            violations.push({
                id: "semantic_violation_".concat(Date.now()),
                description: 'Semantic inconsistency detected',
                severity: consistency < 0.6 ? 'high' : 'medium',
                context: { realityIds: realityIds, consistency: consistency },
                suggestedResolution: 'Unify semantic models across realities'
            });
        }
        return violations;
    };
    /**
     * Detect strategy violations
     */
    CrossRealityConsistencyEngine.prototype.detectStrategyViolations = function (realityIds, data, consistency) {
        var violations = [];
        if (consistency < 0.6) {
            violations.push({
                id: "strategy_violation_".concat(Date.now()),
                description: 'Strategy alignment issues detected',
                severity: consistency < 0.4 ? 'critical' : 'high',
                context: { realityIds: realityIds, consistency: consistency },
                suggestedResolution: 'Realign strategies across realities'
            });
        }
        return violations;
    };
    /**
     * Detect civilization violations
     */
    CrossRealityConsistencyEngine.prototype.detectCivilizationViolations = function (realityIds, data, consistency) {
        var violations = [];
        if (consistency < 0.8) {
            violations.push({
                id: "civilization_violation_".concat(Date.now()),
                description: 'Civilization rules inconsistency',
                severity: consistency < 0.6 ? 'high' : 'medium',
                context: { realityIds: realityIds, consistency: consistency },
                suggestedResolution: 'Synchronize civilization rules'
            });
        }
        return violations;
    };
    /**
     * Detect evolution violations
     */
    CrossRealityConsistencyEngine.prototype.detectEvolutionViolations = function (realityIds, data, consistency) {
        var violations = [];
        if (consistency < 0.5) {
            violations.push({
                id: "evolution_violation_".concat(Date.now()),
                description: 'Evolution trajectory divergence',
                severity: consistency < 0.3 ? 'critical' : 'high',
                context: { realityIds: realityIds, consistency: consistency },
                suggestedResolution: 'Converge evolution trajectories'
            });
        }
        return violations;
    };
    /**
     * Generate reasoning recommendations
     */
    CrossRealityConsistencyEngine.prototype.generateReasoningRecommendations = function (consistency) {
        var recommendations = [];
        if (consistency < 0.7) {
            recommendations.push('Align reasoning frameworks across realities');
            recommendations.push('Establish shared reasoning primitives');
        }
        else if (consistency < 0.85) {
            recommendations.push('Monitor reasoning consistency closely');
        }
        return recommendations;
    };
    /**
     * Generate semantic recommendations
     */
    CrossRealityConsistencyEngine.prototype.generateSemanticRecommendations = function (consistency) {
        var recommendations = [];
        if (consistency < 0.75) {
            recommendations.push('Unify semantic models across realities');
            recommendations.push('Create cross-reality semantic dictionary');
        }
        else if (consistency < 0.9) {
            recommendations.push('Maintain semantic alignment');
        }
        return recommendations;
    };
    /**
     * Generate strategy recommendations
     */
    CrossRealityConsistencyEngine.prototype.generateStrategyRecommendations = function (consistency) {
        var recommendations = [];
        if (consistency < 0.6) {
            recommendations.push('Realign strategies across realities');
            recommendations.push('Establish shared strategic goals');
        }
        else if (consistency < 0.85) {
            recommendations.push('Coordinate strategic adaptations');
        }
        return recommendations;
    };
    /**
     * Generate civilization recommendations
     */
    CrossRealityConsistencyEngine.prototype.generateCivilizationRecommendations = function (consistency) {
        var recommendations = [];
        if (consistency < 0.8) {
            recommendations.push('Synchronize civilization rules');
            recommendations.push('Harmonize cultural norms');
        }
        else if (consistency < 0.9) {
            recommendations.push('Maintain civilization alignment');
        }
        return recommendations;
    };
    /**
     * Generate evolution recommendations
     */
    CrossRealityConsistencyEngine.prototype.generateEvolutionRecommendations = function (consistency) {
        var recommendations = [];
        if (consistency < 0.5) {
            recommendations.push('Converge evolution trajectories');
            recommendations.push('Establish shared evolution goals');
        }
        else if (consistency < 0.8) {
            recommendations.push('Monitor evolution alignment');
        }
        return recommendations;
    };
    /**
     * Store consistency check
     */
    CrossRealityConsistencyEngine.prototype.storeConsistencyCheck = function (check) {
        if (!this.consistencyChecks.has(check.type)) {
            this.consistencyChecks.set(check.type, []);
        }
        this.consistencyChecks.get(check.type).push(check);
    };
    /**
     * Create consistency snapshot
     */
    CrossRealityConsistencyEngine.prototype.createSnapshot = function (realityIds) {
        return __awaiter(this, void 0, void 0, function () {
            var consistencyScores, totalViolations, recommendations, checkTypes, _i, checkTypes_1, type, checks, latestCheck, overallConsistency, snapshot;
            return __generator(this, function (_a) {
                consistencyScores = new Map();
                totalViolations = 0;
                recommendations = [];
                checkTypes = [
                    'reasoning', 'semantic', 'strategy', 'civilization', 'evolution'
                ];
                for (_i = 0, checkTypes_1 = checkTypes; _i < checkTypes_1.length; _i++) {
                    type = checkTypes_1[_i];
                    checks = this.consistencyChecks.get(type) || [];
                    if (checks.length > 0) {
                        latestCheck = checks[checks.length - 1];
                        consistencyScores.set(type, latestCheck.consistency);
                        totalViolations += latestCheck.violations.length;
                        recommendations.push.apply(recommendations, latestCheck.recommendations);
                    }
                    else {
                        consistencyScores.set(type, 0.5); // Default score
                    }
                }
                overallConsistency = Array.from(consistencyScores.values()).reduce(function (sum, score) { return sum + score; }, 0) / consistencyScores.size;
                snapshot = {
                    id: "snapshot_".concat(Date.now()),
                    timestamp: new Date(),
                    realities: realityIds,
                    overallConsistency: overallConsistency,
                    consistencyScores: consistencyScores,
                    totalViolations: totalViolations,
                    recommendations: recommendations
                };
                this.consistencySnapshots.push(snapshot);
                this.emit('snapshot-created', { overallConsistency: overallConsistency, totalViolations: totalViolations });
                return [2 /*return*/, snapshot];
            });
        });
    };
    /**
     * Get consistency checks for a type
     */
    CrossRealityConsistencyEngine.prototype.getConsistencyChecks = function (type) {
        return this.consistencyChecks.get(type) || [];
    };
    /**
     * Get all snapshots
     */
    CrossRealityConsistencyEngine.prototype.getSnapshots = function () {
        return this.consistencySnapshots;
    };
    /**
     * Check if connected
     */
    CrossRealityConsistencyEngine.prototype.isActive = function () {
        return this.isConnected;
    };
    return CrossRealityConsistencyEngine;
}(events_1.EventEmitter));
exports.CrossRealityConsistencyEngine = CrossRealityConsistencyEngine;
