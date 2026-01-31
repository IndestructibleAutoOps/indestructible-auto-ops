# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: javascript-module
# @GL-audit-trail: ../../engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml

/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
const fs = require('fs');

// Fix self-assessment/index.ts
let content = fs.readFileSync('meta-cognitive/self-assessment/index.ts', 'utf8');

// Fix CapabilityAssessment objects - add overallScore property
content = content.replace(/({\s*name: "([^"]+)".*?domain: "([^"]+)".*?proficiency: ([^,]+),\s*reliability: ([^,]+),\s*scalability: ([^,]+),\s*adaptability: ([^,]+),\s*strengths: \[[^\]]*\],\s*weaknesses: \[[^\]]*\],\s*improvements: \[[^\]]*\]\s*})/g, 
  '$1\n      overallScore: 0');

// Fix CulturalDepthAssessment objects - add overallDepth property
content = content.replace(/({\s*name: "([^"]+)".*?dimensions: \{[^}]+\},\s*culturalEvolutionStage: "[^"]+",\s*culturalMarkers: \[[^\]]*\]\s*})/g,
  '$1\n      overallDepth: 0');

// Fix GovernanceAssessment objects - add overallEffectiveness property
content = content.replace(/({\s*name: "([^"]+)".*?dimensions: \{[^}]+\},\s*governanceStyle: "[^"]+",\s*governanceHealth: [^}]+\s*})/g,
  '$1\n      overallEffectiveness: 0');

// Fix SelfAwarenessReport - add overallAwareness property
content = content.replace(/({\s*id: `awareness_[^`]+`,\s*timestamp: [^,]+,\s*selfKnowledge: [^,]+,\s*selfUnderstanding: [^,]+,\s*selfReflection: [^,]+,\s*selfAcceptance: [^,]+,\s*selfImprovement: [^,]+,\s*insights: \[[^\]]*\],\s*blindSpots: \[[^\]]*\]\s*})/g,
  '$1\n      overallAwareness: 0');

fs.writeFileSync('meta-cognitive/self-assessment/index.ts', content);
console.log('Fixed self-assessment/index.ts');