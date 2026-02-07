/**
 * @GL-governed
 * @GL-layer: aep-engine-app
 * @GL-semantic: hooks-use-color-scheme
 * @GL-audit-trail: ../governance/GL_SEMANTIC_ANCHOR.json
 * 
 * GL Unified Charter Activated
 */

import { useThemeContext } from "@/lib/theme-provider";

export function useColorScheme() {
  return useThemeContext().colorScheme;
}
