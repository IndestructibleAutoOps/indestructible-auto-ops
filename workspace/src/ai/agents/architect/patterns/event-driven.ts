// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

export const eventDrivenPattern = {
  name: 'Event-Driven Core',
  focus: ['loose coupling', 'temporal decoupling', 'observability'],
  recommendations: [
    'Standardize on protobuf schemas for brokered events',
    'Apply idempotent consumers to handle retries',
    'Expose replay dashboards for delayed consumers'
  ]
};
