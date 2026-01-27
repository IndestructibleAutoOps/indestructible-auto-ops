// MachineNativeOps Module Data
// This file contains the module dependency data for visualization

const moduleData = {
    modules: [
        {
            id: "01-core",
            name: "Core Infrastructure",
            autonomyLevel: "L1-L2",
            status: "active",
            semanticHealth: 100,
            namespace: "mno-core",
            description: "Foundation layer providing core infrastructure services",
            dependencies: [],
            components: ["config-manager", "service-registry", "event-bus", "logging-framework"]
        },
        {
            id: "02-intelligence",
            name: "Intelligence Layer",
            autonomyLevel: "L2-L3",
            status: "active",
            semanticHealth: 100,
            namespace: "mno-intelligence",
            description: "AI/ML capabilities and intelligent decision making",
            dependencies: ["01-core"],
            components: ["ml-pipeline", "model-registry", "inference-engine", "training-orchestrator", "feature-store"]
        },
        {
            id: "03-governance",
            name: "Governance Framework",
            autonomyLevel: "L3-L4",
            status: "active",
            semanticHealth: 100,
            namespace: "mno-governance",
            description: "Policy enforcement and governance automation",
            dependencies: ["01-core", "02-intelligence"],
            components: ["policy-engine", "compliance-checker", "audit-logger", "access-controller", "rule-evaluator", "governance-dashboard"]
        },
        {
            id: "04-autonomous",
            name: "Autonomous Operations",
            autonomyLevel: "L4-L5",
            status: "in-development",
            semanticHealth: 85,
            namespace: "mno-autonomous",
            description: "Self-managing and self-healing capabilities",
            dependencies: ["01-core", "02-intelligence", "03-governance"],
            components: ["auto-scaler", "self-healer", "anomaly-detector", "decision-engine", "workflow-orchestrator", "resource-optimizer"]
        },
        {
            id: "05-observability",
            name: "Observability Platform",
            autonomyLevel: "L4-L5",
            status: "active",
            semanticHealth: 100,
            namespace: "mno-observability",
            description: "Monitoring, logging, and tracing infrastructure",
            dependencies: ["01-core", "02-intelligence", "03-governance"],
            components: ["metrics-collector", "log-aggregator", "trace-analyzer", "alert-manager", "dashboard-service", "slo-monitor", "incident-tracker"]
        },
        {
            id: "06-security",
            name: "Security & Compliance",
            autonomyLevel: "Global Layer",
            status: "active",
            semanticHealth: 100,
            namespace: "mno-security",
            description: "Cross-cutting security with VETO authority",
            dependencies: ["01-core", "03-governance", "05-observability"],
            components: ["identity-manager", "secret-vault", "threat-detector", "compliance-scanner", "audit-trail", "encryption-service", "access-gateway", "vulnerability-scanner"]
        }
    ],
    
    // Graph structure for D3
    graph: {
        "01-core": [],
        "02-intelligence": ["01-core"],
        "03-governance": ["01-core", "02-intelligence"],
        "04-autonomous": ["01-core", "02-intelligence", "03-governance"],
        "05-observability": ["01-core", "02-intelligence", "03-governance"],
        "06-security": ["01-core", "03-governance", "05-observability"]
    },
    
    // Depth levels for hierarchical layout
    depths: {
        "01-core": 0,
        "02-intelligence": 1,
        "03-governance": 2,
        "04-autonomous": 3,
        "05-observability": 3,
        "06-security": 4
    },
    
    // Statistics
    statistics: {
        totalModules: 6,
        totalDependencies: 12,
        maxDepth: 4,
        cycles: 0,
        activeModules: 5,
        inDevelopment: 1,
        averageSemanticHealth: 97.5
    }
};

// Helper function to get module by ID
function getModuleById(id) {
    return moduleData.modules.find(m => m.id === id);
}

// Helper function to get dependents (modules that depend on this module)
function getDependents(moduleId) {
    return moduleData.modules
        .filter(m => m.dependencies.includes(moduleId))
        .map(m => m.id);
}

// Helper function to get all links for D3
function getLinks() {
    const links = [];
    for (const [target, sources] of Object.entries(moduleData.graph)) {
        for (const source of sources) {
            links.push({ source, target });
        }
    }
    return links;
}

// Helper function to get nodes for D3
function getNodes() {
    return moduleData.modules.map(m => ({
        id: m.id,
        name: m.name,
        autonomyLevel: m.autonomyLevel,
        status: m.status,
        semanticHealth: m.semanticHealth,
        namespace: m.namespace,
        description: m.description,
        dependencies: m.dependencies,
        dependents: getDependents(m.id),
        components: m.components,
        depth: moduleData.depths[m.id]
    }));
}

// Export for use in visualization
window.moduleData = moduleData;
window.getModuleById = getModuleById;
window.getDependents = getDependents;
window.getLinks = getLinks;
window.getNodes = getNodes;