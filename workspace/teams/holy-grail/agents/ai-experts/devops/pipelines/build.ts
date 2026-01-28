// @GL-governed
// @GL-layer: GL-L10-WORKSPACE
// @GL-semantic: governance-layer-workspace
// @GL-revision: 1.0.0
// @GL-status: active

export const buildPipeline = {
  name: 'Build',
  stages: ['checkout', 'install', 'compile'],
  artifact: 'dist/',
};
