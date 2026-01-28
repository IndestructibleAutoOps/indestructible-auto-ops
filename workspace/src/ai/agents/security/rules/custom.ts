// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

export interface CustomRule {
  id: string;
  description: string;
  severity: 'low' | 'medium' | 'high';
}

export const customRules: CustomRule[] = [
  { id: 'UIS-001', description: 'Enforce signed commits', severity: 'medium' },
  { id: 'UIS-002', description: 'Disallow plaintext secrets in configs', severity: 'high' }
];
