# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: archive-tools
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
// @GL-governed
// @GL-layer: GL-L5-CONFIG
// @GL-semantic: governance-layer-configuration
// @GL-revision: 1.0.0
// @GL-status: active

import { defineConfig } from "drizzle-kit";

if (!process.env.DATABASE_URL) {
  throw new Error("DATABASE_URL, ensure the database is provisioned");
}

export default defineConfig({
  out: "./migrations",
  schema: "./shared/schema.ts",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL,
  },
});
