# ECOSYSTEM Merge Decisions (Phase B)

**Date:** 2026-02-05  
**Scope:** Decisions and actions taken during merge execution

## Actions Completed
1. **Merged legacy reasoning pipeline code**
   - Added `ecosystem/reasoning/dual_path/base_retrieval.py`
   - Added `ecosystem/reasoning/dual_path/pipeline.py`

2. **Merged legacy reasoning utilities**
   - Added `ecosystem/reasoning/utils/simple_yaml.py`
   - Added `ecosystem/reasoning/utils/__init__.py`

3. **Preserved legacy test script as a runnable tool**
   - Added `scripts/test_dual_path_system.py`
   - Adjusted sys.path to load `ecosystem/` from repo root

## Exclusions (Not Merged)
- **Legacy logs / generated data**
  - `machine-native-ops/ecosystem/logs/**`
  - `machine-native-ops/ecosystem/reasoning/logs/**`
  - `machine-native-ops/ecosystem/reasoning/data/**`
- **Legacy `.coverage` / audit trail DB**
  - Treated as generated artifact; not merged

## Root-Preferred Files (Kept Root Versions)
- `Makefile`
- `pytest.ini`
- `.yamllint.yml`

## Pending
- Evaluate **M-modified** files for selective merge vs root-wins.
- Update references to `machine-native-ops/` prior to retiring nested repo.
- Plan Phase C: archive or remove `machine-native-ops/`.
