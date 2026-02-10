# ECOSYSTEM-MERGE-MAP

## Purpose
Define the merge and retirement strategy between:
- repository root (source of truth)
- nested repository: machine-native-ops/ (legacy snapshot)

This map is an inventory and mapping plan. It does not execute moves.

## Decision Anchor
- Source of truth: repository root (/workspace)
- Nested repo: machine-native-ops/ is legacy and must be merged then retired
- Rationale: root already contains the full platform tree; nested repo is a
  separate Git worktree that causes governance and traceability conflicts.

## Inventory Summary
### Root (selected top-level)
- ecosystem/
- gov-runtime-engine-platform/
- gov-runtime-execution-platform/
- gov-governance-compliance/
- gov-governance-architecture-platform/
- gov-infrastructure-foundation-platform/
- gov-meta-specifications/
- gov-enterprise-architecture/
- docs/
- governance/
- scripts/
- tests/
- platforms/

### Nested repo: machine-native-ops/ (top-level)
- ecosystem/
- gl.runtime.engine-platform/
- ARCHITECTURE-COMPLETE.md
- GL-NAMING-ONTOLOGY-COMPLETE.md
- P0-IMPLEMENTATION-SUMMARY.md
- Makefile
- pytest.ini
- test_dual_path_system.py
- .yamllint.yml
- .coverage

## Mapping Table (machine-native-ops -> root)
| machine-native-ops path | Root target | Action | Notes |
|---|---|---|---|
| ecosystem/ | ecosystem/ | Merge | Compare tree; keep root as primary. |
| gl.runtime.engine-platform/ | gov-runtime-engine-platform/ | Merge/Rename | Normalize name; diff with root runtime engine. |
| ARCHITECTURE-COMPLETE.md | docs/architecture/ARCHITECTURE-COMPLETE.md | Move/Merge | If already exists, merge content. |
| GL-NAMING-ONTOLOGY-COMPLETE.md | docs/verification/GL-NAMING-ONTOLOGY-COMPLETE.md | Move/Merge | If already exists, merge or dedupe. |
| P0-IMPLEMENTATION-SUMMARY.md | docs/reports/P0-IMPLEMENTATION-SUMMARY.md | Move | Prefer reports/ bucket. |
| Makefile | /workspace/Makefile | Evaluate | Keep if used by root build. |
| pytest.ini | /workspace/pytest.ini | Evaluate | Keep if tests run from root. |
| test_dual_path_system.py | tests/ or scripts/ | Evaluate | Move under tests/ if active. |
| .yamllint.yml | /workspace/.yamllint.yml | Evaluate | Keep if linting is used. |
| .coverage | (ignore) | Drop | Generated artifact; do not merge. |

## Root-Only (no merge needed)
These exist in root and should remain authoritative:
- gov-runtime-execution-platform/
- gov-governance-compliance/
- gov-governance-architecture-platform/
- gov-infrastructure-foundation-platform/
- gov-meta-specifications/
- gov-enterprise-architecture/
- docs/ (already layered)

## Required Diffs Before Merge
1. ecosystem/ vs machine-native-ops/ecosystem/
2. gov-runtime-engine-platform/ vs machine-native-ops/gl.runtime.engine-platform/
3. docs/architecture/ARCHITECTURE-COMPLETE.md presence check
4. docs/verification/GL-NAMING-ONTOLOGY-COMPLETE.md presence check
5. tests/ coverage of test_dual_path_system.py usage

## Execution Phases (recommended)
Phase A - Inventory and Diffs
- Generate file-level diff report for the two ecosystems.
- Verify any root files that already exist in docs/.

Phase B - Merge (root remains primary)
- Merge ecosystem/ content into root.
- Rename gl.runtime.engine-platform -> gov-runtime-engine-platform and merge.
- Move docs into docs/ buckets if not already present.

Phase C - Retire nested repo
- Remove machine-native-ops/ directory or archive to archives/legacy/.
- Add governance rule to prevent nested git repos.

## Risks and Guardrails
- Risk: duplicate platform trees cause conflicting runtime behavior.
- Guardrail: root always wins; nested repo is treated as legacy.
- Risk: naming mismatch (gl.runtime.* vs gov-runtime-*).
- Guardrail: enforce kebab-case for platform dirs.

## Success Criteria
- No nested Git repo remains in root.
- Single ecosystem/ and single gov-runtime-engine-platform/ source.
- All legacy docs moved under docs/.
- No references to machine-native-ops/ remain in code or docs.
