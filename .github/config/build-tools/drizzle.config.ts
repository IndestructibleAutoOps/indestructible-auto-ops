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
