// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL?: string;
  // Add more env variables as needed
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
