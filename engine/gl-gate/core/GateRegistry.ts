/**
 * @fileoverview GL-Gate Registry - Central registry for all governance gates
 * @module @machine-native-ops/gl-gate/core/GateRegistry
 * @version 1.0.0
 * @since 2026-01-26
 * @author MachineNativeOps
 * @gl-governed true
 * @gl-layer GL-40-GOVERNANCE
 * 
 * GL Unified Charter Activated
 */

import { GateDefinition, GateId, GateCategory, GateSeverity } from '../types';

/**
 * GL-Gate Registry
 * 治理閘門註冊表
 * 
 * Central registry containing all gate definitions with bilingual support.
 */
export class GateRegistry {
  private static instance: GateRegistry;
  private gates: Map<GateId, GateDefinition> = new Map();

  private constructor() {
    this.initializeGates();
  }

  /**
   * Get singleton instance
   */
  public static getInstance(): GateRegistry {
    if (!GateRegistry.instance) {
      GateRegistry.instance = new GateRegistry();
    }
    return GateRegistry.instance;
  }

  /**
   * Initialize all gate definitions
   */
  private initializeGates(): void {
    // gl-gate:01 - Performance Optimization with Batching and Caching
    this.registerGate({
      id: 'gl-gate:01',
      nameEN: 'Performance Optimization with Batching and Caching',
      nameZH: '利用批次與快取進行效能優化',
      category: 'performance',
      descriptionEN: 'Responsible for improving system performance through batch processing, caching strategies, duplicate query merging, and resource reuse to reduce latency and computational costs.',
      descriptionZH: '負責透過批次處理、快取策略、重複查詢合併與資源重用來提升系統效能，降低延遲與運算成本。',
      semanticBoundary: 'Performance optimization layer - covers caching, batching, and resource efficiency. Does not involve business logic or data content.',
      verificationStandards: [
        'Cache hit rate >= 80%',
        'Batch processing success rate >= 99%',
        'Query deduplication rate measured',
        'Resource utilization efficiency tracked',
        'Latency reduction metrics collected'
      ],
      defaultSeverity: 'high',
      enabledByDefault: true,
      version: '1.0.0'
    });

    // gl-gate:02 - Data Access Layer Abstraction
    this.registerGate({
      id: 'gl-gate:02',
      nameEN: 'Data Access Layer Abstraction',
      nameZH: '資料存取層抽象化',
      category: 'data-access',
      descriptionEN: 'Provides unified data access interfaces, isolating underlying database or storage technology differences, ensuring maintainability, replaceability, and consistent data operation flows.',
      descriptionZH: '提供統一的資料存取介面，隔離底層資料庫或儲存技術差異，確保可維護性、可替換性與一致的資料操作流程。',
      semanticBoundary: 'Data access abstraction layer - covers interface standardization and storage isolation. Does not involve specific data content or business rules.',
      verificationStandards: [
        'Interface compliance rate 100%',
        'Storage abstraction coverage verified',
        'Data operation consistency tests passed',
        'Replaceability validation completed',
        'Access pattern audit trails maintained'
      ],
      defaultSeverity: 'high',
      enabledByDefault: true,
      version: '1.0.0'
    });

    // gl-gate:06 - Observability (Logging, Metrics, Tracing)
    this.registerGate({
      id: 'gl-gate:06',
      nameEN: 'Observability (Logging, Metrics, Tracing)',
      nameZH: '可觀察性（記錄、指標、追蹤）',
      category: 'observability',
      descriptionEN: 'Establishes comprehensive observability framework covering logs, system metrics, and distributed tracing to support problem diagnosis, performance analysis, and behavior monitoring.',
      descriptionZH: '建立完整的可觀察性框架，涵蓋日誌、系統指標、分散式追蹤，以支援問題診斷、效能分析與行為監控。',
      semanticBoundary: 'Observability data layer - covers metrics, logs, traces, and telemetry. Does not involve business data content.',
      verificationStandards: [
        'Log coverage >= 95%',
        'Metric collection completeness verified',
        'Trace context propagation validated',
        'Telemetry compliance (GDPR, privacy) checked',
        'Observability data retention policies enforced'
      ],
      defaultSeverity: 'high',
      enabledByDefault: true,
      version: '1.0.0'
    });

    // gl-gate:07 - Security Layer (PII Detection, Data Sanitization)
    this.registerGate({
      id: 'gl-gate:07',
      nameEN: 'Security Layer (PII Detection, Data Sanitization)',
      nameZH: '安全層（PII 偵測、資料淨化）',
      category: 'security',
      descriptionEN: 'Responsible for sensitive information detection, data sanitization, permission control, and security policy enforcement to ensure data processing complies with privacy and security requirements.',
      descriptionZH: '負責敏感資訊偵測、資料淨化、權限控管與安全策略執行，確保資料處理符合隱私與安全要求。',
      semanticBoundary: 'Security and privacy layer - covers PII detection, sanitization, and access control. Does not involve business logic.',
      verificationStandards: [
        'PII detection accuracy >= 99%',
        'Data sanitization coverage 100%',
        'Permission model compliance verified',
        'Security policy enforcement validated',
        'Audit log integrity maintained'
      ],
      defaultSeverity: 'critical',
      enabledByDefault: true,
      version: '1.0.0'
    });

    // gl-gate:08 - Integration Layer (API Gateway, Rate Limiting)
    this.registerGate({
      id: 'gl-gate:08',
      nameEN: 'Integration Layer (API Gateway, Rate Limiting)',
      nameZH: '整合層（API 閘道、速率限制）',
      category: 'integration',
      descriptionEN: 'Provides cross-system integration capabilities including API Gateway, traffic control, rate limiting, protocol conversion, and external service collaboration.',
      descriptionZH: '提供跨系統整合能力，包括 API Gateway、流量控管、速率限制、協定轉換與外部服務協作。',
      semanticBoundary: 'Integration and API layer - covers gateway, rate limiting, and protocol handling. Does not involve internal business processing.',
      verificationStandards: [
        'API gateway availability >= 99.9%',
        'Rate limiting accuracy verified',
        'Protocol conversion compliance checked',
        'External service SLA monitoring active',
        'Integration error handling validated'
      ],
      defaultSeverity: 'high',
      enabledByDefault: true,
      version: '1.0.0'
    });

    // gl-gate:11 - Testing Layer (Data Validation, Quality Checks)
    this.registerGate({
      id: 'gl-gate:11',
      nameEN: 'Testing Layer (Data Validation, Quality Checks)',
      nameZH: '測試層（資料驗證、品質檢查）',
      category: 'testing',
      descriptionEN: 'Responsible for data validation, quality checks, automated testing, and consistency verification to ensure inputs, outputs, and processes meet expectations.',
      descriptionZH: '負責資料驗證、品質檢查、自動化測試與一致性檢查，確保輸入、輸出與流程符合預期。',
      semanticBoundary: 'Testing and validation layer - covers data validation and quality assurance. Does not involve production operations.',
      verificationStandards: [
        'Test coverage >= 80%',
        'Data validation accuracy 100%',
        'Quality check pass rate tracked',
        'Consistency verification completed',
        'Test report traceability maintained'
      ],
      defaultSeverity: 'high',
      enabledByDefault: true,
      version: '1.0.0'
    });

    // gl-gate:15 - Stress Testing Layer (Load Testing, Fault Injection)
    this.registerGate({
      id: 'gl-gate:15',
      nameEN: 'Stress Testing Layer (Load Testing, Fault Injection)',
      nameZH: '壓力測試層（負載測試、故障注入）',
      category: 'stress-testing',
      descriptionEN: 'Validates system stability and recovery capabilities under extreme conditions through load testing, stress testing, and fault injection.',
      descriptionZH: '透過負載測試、壓力測試、故障注入等方式驗證系統在極端情況下的穩定性與恢復能力。',
      semanticBoundary: 'Stress and resilience testing layer - covers load testing and chaos engineering. Does not involve normal operations.',
      verificationStandards: [
        'Load test scenarios executed',
        'Stress test thresholds validated',
        'Fault injection recovery verified',
        'System resilience metrics collected',
        'Performance degradation limits checked'
      ],
      defaultSeverity: 'medium',
      enabledByDefault: true,
      version: '1.0.0'
    });

    // gl-gate:19 - Governance Summary (Compliance Reporting)
    this.registerGate({
      id: 'gl-gate:19',
      nameEN: 'Governance Summary (Compliance Reporting)',
      nameZH: '治理摘要（合規報告）',
      category: 'governance',
      descriptionEN: 'Aggregates governance layer execution status, compliance reports, audit records, and governance event summaries to provide decision-making and review basis.',
      descriptionZH: '彙整治理層級的執行情況、合規性報告、稽核紀錄與治理事件摘要，提供決策與審查依據。',
      semanticBoundary: 'Governance reporting layer - covers compliance aggregation and audit summaries. Does not involve operational execution.',
      verificationStandards: [
        'Compliance report completeness verified',
        'Audit record integrity maintained',
        'Governance event stream captured',
        'Decision support data available',
        'Review trail traceability ensured'
      ],
      defaultSeverity: 'high',
      enabledByDefault: true,
      dependencies: ['gl-gate:06', 'gl-gate:07', 'gl-gate:11'],
      version: '1.0.0'
    });

    // gl-gate:20 - Final Seal Layer (Irreversible Governance Baselines)
    this.registerGate({
      id: 'gl-gate:20',
      nameEN: 'Final Seal Layer (Irreversible Governance Baselines)',
      nameZH: '最終封印層（不可逆治理基線）',
      category: 'sealing',
      descriptionEN: 'Responsible for final sealing of governance baselines, making them irreversible and immutable, ensuring governance state integrity and permanence.',
      descriptionZH: '負責將治理基線進行最終封存，使其不可逆、不可修改，確保治理狀態的完整性與永久性。',
      semanticBoundary: 'Sealing and immutability layer - covers final baseline sealing and evidence chain. Does not involve ongoing governance operations.',
      verificationStandards: [
        'Seal integrity cryptographically verified',
        'Immutability guarantees validated',
        'Evidence chain completeness checked',
        'Baseline permanence ensured',
        'Seal timestamp accuracy verified'
      ],
      defaultSeverity: 'critical',
      enabledByDefault: true,
      dependencies: ['gl-gate:19'],
      version: '1.0.0'
    });
  }

  /**
   * Register a gate definition
   */
  public registerGate(definition: GateDefinition): void {
    this.gates.set(definition.id, definition);
  }

  /**
   * Get gate definition by ID
   */
  public getGate(id: GateId): GateDefinition | undefined {
    return this.gates.get(id);
  }

  /**
   * Get all gate definitions
   */
  public getAllGates(): GateDefinition[] {
    return Array.from(this.gates.values());
  }

  /**
   * Get gates by category
   */
  public getGatesByCategory(category: GateCategory): GateDefinition[] {
    return this.getAllGates().filter(gate => gate.category === category);
  }

  /**
   * Get gates by severity
   */
  public getGatesBySeverity(severity: GateSeverity): GateDefinition[] {
    return this.getAllGates().filter(gate => gate.defaultSeverity === severity);
  }

  /**
   * Get enabled gates
   */
  public getEnabledGates(): GateDefinition[] {
    return this.getAllGates().filter(gate => gate.enabledByDefault);
  }

  /**
   * Get gate dependencies (topologically sorted)
   */
  public getGateDependencies(id: GateId): GateId[] {
    const gate = this.getGate(id);
    if (!gate || !gate.dependencies) {
      return [];
    }
    
    const allDeps: GateId[] = [];
    const visited = new Set<GateId>();
    
    const collectDeps = (gateId: GateId) => {
      if (visited.has(gateId)) return;
      visited.add(gateId);
      
      const g = this.getGate(gateId);
      if (g?.dependencies) {
        for (const dep of g.dependencies) {
          collectDeps(dep);
          if (!allDeps.includes(dep)) {
            allDeps.push(dep);
          }
        }
      }
    };
    
    collectDeps(id);
    return allDeps;
  }

  /**
   * Validate gate execution order
   */
  public validateExecutionOrder(gateIds: GateId[]): { valid: boolean; errors: string[] } {
    const errors: string[] = [];
    const executed = new Set<GateId>();
    
    for (const gateId of gateIds) {
      const gate = this.getGate(gateId);
      if (!gate) {
        errors.push(`Unknown gate: ${gateId}`);
        continue;
      }
      
      if (gate.dependencies) {
        for (const dep of gate.dependencies) {
          if (!executed.has(dep) && !gateIds.slice(0, gateIds.indexOf(gateId)).includes(dep)) {
            errors.push(`Gate ${gateId} depends on ${dep} which is not scheduled before it`);
          }
        }
      }
      
      executed.add(gateId);
    }
    
    return { valid: errors.length === 0, errors };
  }

  /**
   * Get gate count
   */
  public getGateCount(): number {
    return this.gates.size;
  }

  /**
   * Export registry as JSON
   */
  public toJSON(): Record<string, GateDefinition> {
    const result: Record<string, GateDefinition> = {};
    for (const [id, def] of this.gates) {
      result[id] = def;
    }
    return result;
  }
}

// Export singleton instance
export const gateRegistry = GateRegistry.getInstance();

// GL Unified Charter Activated