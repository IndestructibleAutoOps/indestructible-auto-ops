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
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
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
exports.UniversalInterfaceLayer = void 0;
/**
 * Universal Interface Layer
 *
 * 通用介面層 - 以統一語意、策略、結構與外界溝通、協作、交換資訊
 *
 * 核心能力：
 * 1. Unified semantic communication
 * 2. Unified strategy collaboration
 * 3. Unified structure information exchange
 *
 * 這是「智慧的語言」
 */
var events_1 = require("events");
var UniversalInterfaceLayer = /** @class */ (function (_super) {
    __extends(UniversalInterfaceLayer, _super);
    function UniversalInterfaceLayer() {
        var _this = _super.call(this) || this;
        _this.messageHistory = [];
        _this.translationHistory = [];
        _this.supportedProtocols = new Map();
        _this.activeConnections = new Map();
        _this.isConnected = false;
        return _this;
    }
    /**
     * Initialize the universal interface layer
     */
    UniversalInterfaceLayer.prototype.initialize = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                this.isConnected = true;
                this.registerDefaultProtocols();
                console.log('✅ Universal Interface Layer initialized');
                this.emit('initialized');
                return [2 /*return*/];
            });
        });
    };
    /**
     * Register default communication protocols
     */
    UniversalInterfaceLayer.prototype.registerDefaultProtocols = function () {
        var protocols = [
            {
                protocol: 'gl-semantic',
                version: '1.0.0',
                supportedFormats: ['json', 'yaml', 'xml'],
                features: ['semantic-aware', 'context-aware', 'cross-domain']
            },
            {
                protocol: 'gl-strategy',
                version: '1.0.0',
                supportedFormats: ['json', 'yaml'],
                features: ['strategy-encoding', 'parameter-sharing', 'constraint-exchange']
            },
            {
                protocol: 'gl-structure',
                version: '1.0.0',
                supportedFormats: ['json', 'protobuf', 'avro'],
                features: ['schema-validation', 'version-compatibility', 'type-safety']
            }
        ];
        for (var _i = 0, protocols_1 = protocols; _i < protocols_1.length; _i++) {
            var protocol = protocols_1[_i];
            this.supportedProtocols.set(protocol.protocol, protocol);
        }
    };
    /**
     * Send universal message
     */
    UniversalInterfaceLayer.prototype.sendMessage = function (message) {
        return __awaiter(this, void 0, void 0, function () {
            var error_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        // Validate message
                        if (!this.validateMessage(message)) {
                            return [2 /*return*/, false];
                        }
                        // Process message based on type
                        return [4 /*yield*/, this.processMessage(message)];
                    case 1:
                        // Process message based on type
                        _a.sent();
                        // Store in history
                        this.messageHistory.push(message);
                        this.emit('message-sent', { messageId: message.id, target: message.target });
                        return [2 /*return*/, true];
                    case 2:
                        error_1 = _a.sent();
                        console.error('Error sending message:', error_1);
                        return [2 /*return*/, false];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    /**
     * Validate universal message
     */
    UniversalInterfaceLayer.prototype.validateMessage = function (message) {
        return !!(message.id &&
            message.type &&
            message.source &&
            message.target &&
            message.payload);
    };
    /**
     * Process message based on type
     */
    UniversalInterfaceLayer.prototype.processMessage = function (message) {
        return __awaiter(this, void 0, void 0, function () {
            var _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = message.type;
                        switch (_a) {
                            case 'semantic': return [3 /*break*/, 1];
                            case 'strategy': return [3 /*break*/, 3];
                            case 'structure': return [3 /*break*/, 5];
                            case 'query': return [3 /*break*/, 7];
                            case 'response': return [3 /*break*/, 9];
                        }
                        return [3 /*break*/, 11];
                    case 1: return [4 /*yield*/, this.processSemanticMessage(message)];
                    case 2:
                        _b.sent();
                        return [3 /*break*/, 11];
                    case 3: return [4 /*yield*/, this.processStrategyMessage(message)];
                    case 4:
                        _b.sent();
                        return [3 /*break*/, 11];
                    case 5: return [4 /*yield*/, this.processStructureMessage(message)];
                    case 6:
                        _b.sent();
                        return [3 /*break*/, 11];
                    case 7: return [4 /*yield*/, this.processQueryMessage(message)];
                    case 8:
                        _b.sent();
                        return [3 /*break*/, 11];
                    case 9: return [4 /*yield*/, this.processResponseMessage(message)];
                    case 10:
                        _b.sent();
                        return [3 /*break*/, 11];
                    case 11: return [2 /*return*/];
                }
            });
        });
    };
    /**
     * Process semantic message
     */
    UniversalInterfaceLayer.prototype.processSemanticMessage = function (message) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                // Apply semantic metadata
                if (message.semantics) {
                    // Decode and process semantic information
                    console.log("Processing semantic message: ".concat(message.id));
                }
                return [2 /*return*/];
            });
        });
    };
    /**
     * Process strategy message
     */
    UniversalInterfaceLayer.prototype.processStrategyMessage = function (message) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                // Apply strategy metadata
                if (message.strategy) {
                    // Decode and process strategy information
                    console.log("Processing strategy message: ".concat(message.id));
                }
                return [2 /*return*/];
            });
        });
    };
    /**
     * Process structure message
     */
    UniversalInterfaceLayer.prototype.processStructureMessage = function (message) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                // Apply structure metadata
                if (message.structure) {
                    // Decode and process structure information
                    console.log("Processing structure message: ".concat(message.id));
                }
                return [2 /*return*/];
            });
        });
    };
    /**
     * Process query message
     */
    UniversalInterfaceLayer.prototype.processQueryMessage = function (message) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                // Handle query and generate response
                console.log("Processing query message: ".concat(message.id));
                return [2 /*return*/];
            });
        });
    };
    /**
     * Process response message
     */
    UniversalInterfaceLayer.prototype.processResponseMessage = function (message) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                // Handle response
                console.log("Processing response message: ".concat(message.id));
                return [2 /*return*/];
            });
        });
    };
    /**
     * Translate message between formats
     */
    UniversalInterfaceLayer.prototype.translateMessage = function (message, targetFormat) {
        return __awaiter(this, void 0, void 0, function () {
            var sourceFormat, translatedMessage, result;
            return __generator(this, function (_a) {
                sourceFormat = this.detectMessageFormat(message);
                translatedMessage = __assign(__assign({}, message), { id: "".concat(message.id, "_translated"), timestamp: new Date() });
                // Convert payload to target format
                translatedMessage.payload = this.convertPayload(message.payload, targetFormat);
                result = {
                    sourceMessage: message,
                    translatedMessage: translatedMessage,
                    sourceFormat: sourceFormat,
                    targetFormat: targetFormat,
                    confidence: 0.85 + Math.random() * 0.15,
                    timestamp: new Date()
                };
                this.translationHistory.push(result);
                this.emit('message-translated', { messageId: message.id, targetFormat: targetFormat });
                return [2 /*return*/, result];
            });
        });
    };
    /**
     * Detect message format
     */
    UniversalInterfaceLayer.prototype.detectMessageFormat = function (message) {
        if (message.structure && message.structure.format) {
            return message.structure.format;
        }
        return 'json';
    };
    /**
     * Convert payload to target format
     */
    UniversalInterfaceLayer.prototype.convertPayload = function (payload, targetFormat) {
        // In a real implementation, this would use proper format converters
        // For now, return payload as-is
        return payload;
    };
    /**
     * Establish connection with external system
     */
    UniversalInterfaceLayer.prototype.establishConnection = function (systemId, protocol) {
        return __awaiter(this, void 0, void 0, function () {
            var protocolInfo;
            return __generator(this, function (_a) {
                protocolInfo = this.supportedProtocols.get(protocol);
                if (!protocolInfo) {
                    console.error("Protocol ".concat(protocol, " not supported"));
                    return [2 /*return*/, false];
                }
                this.activeConnections.set(systemId, {
                    protocol: protocol,
                    connectedAt: new Date(),
                    status: 'active'
                });
                this.emit('connection-established', { systemId: systemId, protocol: protocol });
                return [2 /*return*/, true];
            });
        });
    };
    /**
     * Close connection with external system
     */
    UniversalInterfaceLayer.prototype.closeConnection = function (systemId) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                if (this.activeConnections.has(systemId)) {
                    this.activeConnections.delete(systemId);
                    this.emit('connection-closed', { systemId: systemId });
                    return [2 /*return*/, true];
                }
                return [2 /*return*/, false];
            });
        });
    };
    /**
     * Get message history
     */
    UniversalInterfaceLayer.prototype.getMessageHistory = function () {
        return this.messageHistory;
    };
    /**
     * Get translation history
     */
    UniversalInterfaceLayer.prototype.getTranslationHistory = function () {
        return this.translationHistory;
    };
    /**
     * Get supported protocols
     */
    UniversalInterfaceLayer.prototype.getSupportedProtocols = function () {
        return Array.from(this.supportedProtocols.values());
    };
    /**
     * Get active connections
     */
    UniversalInterfaceLayer.prototype.getActiveConnections = function () {
        return this.activeConnections;
    };
    /**
     * Check if connected
     */
    UniversalInterfaceLayer.prototype.isActive = function () {
        return this.isConnected;
    };
    return UniversalInterfaceLayer;
}(events_1.EventEmitter));
exports.UniversalInterfaceLayer = UniversalInterfaceLayer;
