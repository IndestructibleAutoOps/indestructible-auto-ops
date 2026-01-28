// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

export const deployPipeline = {
  name: 'Deploy',
  strategies: ['blue-green', 'canary'],
  approvalsRequired: true,
};
