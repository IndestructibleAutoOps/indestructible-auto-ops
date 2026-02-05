# 文檔重組計劃

## 目標
將根目錄中的 39 個 MD 文檔按照功能和用途重新組織到適當的位置。

## 文檔分類

### 1. 核心文檔 - 保留在根目錄 (7 個)
- README.md
- CONTRIBUTING.md
- DEVELOPMENT_STRATEGY.md
- DEPLOYMENT_GUIDE.md
- CODE_OF_CONDUCT.md
- CHANGELOG.md
- ARCHITECTURE_COMPLETE.md

### 2. 項目狀態文檔 - 保留在根目錄 (4 個)
- CURRENT_STRUCTURE_SUMMARY.md
- DIRECTORY_STRUCTURE_VERIFICATION.md
- ECOSYSTEM_MIGRATION_GUIDE.md
- ECOSYSTEM_PLATFORM_RESTRUCTURE_PLAN.md
- GL_NAMING_ONTOLOGY_COMPLETE.md

### 3. 報告文檔 - 移至 docs/reports/ (5 個)
- comprehensive_cross_comparison_report.md
- final_comprehensive_report.md
- final_execution_report.md
- gl_markers_report.md
- validation_report.md

### 4. 分析文檔 - 移至 docs/analysis/ (3 個)
- elasticsearch_search_system_analysis.md
- naming_governance_analysis_report.md
- structure_gap_analysis.md

### 5. 計劃文檔 - 移至 docs/plans/ (8 個)
- execution_plan.md
- external_dependency_removal_strategy.md
- gl-platform-restructure-plan.md
- migration_strategy.md
- naming_governance_analysis_task.md
- naming_governance_structure_definition.md
- professional_naming_restructure_proposal.md
- radical_dependency_elimination_plan.md
- scripts_cleanup_plan.md
- structure_migration_plan.md
- terminology_replacement_strategy.md
- governance_files_migration_plan.md

### 6. 階段報告 - 移至 docs/phases/ (4 個)
- phase1_semantic_models.md
- phase2_comprehensive_alignment_report.md
- phase3_gl_root_reconstruction.md
- phase4_gl_markers_compliance_summary.md

### 7. 專案特定文檔 - 移至 docs/projects/ (3 個)
- PROJECT_STRUCTURE_REBUILD_COMPLETE.md
- radical_dependency_elimination_complete.md
- structure_rebuild_verification_report.md

### 8. 分析工具報告 - 移至 docs/verification/ (4 個)
- GL_NAMING_ONTOLOGY_GAP_ANALYSIS.md
- LOCAL_KNOWLEDGE_BASE.md
- MAIN_BRANCH_FILE_PATH_VERIFICATION.md
- platform_directory_structure_best_practices.md

### 9. 遺留文檔 - 移至 docs/archive/ (2 個)
- naming_governance_analysis_task.md
- naming_governance_structure_definition.md
- todo.md

## 執行命令

```bash
# 創建目標目錄
mkdir -p docs/reports docs/analysis docs/plans docs/phases docs/projects docs/verification docs/archive

# 移動報告文檔
mv comprehensive_cross_comparison_report.md docs/reports/
mv final_comprehensive_report.md docs/reports/
mv final_execution_report.md docs/reports/
mv gl_markers_report.md docs/reports/
mv validation_report.md docs/reports/

# 移動分析文檔
mv elasticsearch_search_system_analysis.md docs/analysis/
mv naming_governance_analysis_report.md docs/analysis/
mv structure_gap_analysis.md docs/analysis/

# 移動計劃文檔
mv execution_plan.md docs/plans/
mv external_dependency_removal_strategy.md docs/plans/
mv gl-platform-restructure-plan.md docs/plans/
mv migration_strategy.md docs/plans/
mv professional_naming_restructure_proposal.md docs/plans/
mv radical_dependency_elimination_plan.md docs/plans/
mv scripts_cleanup_plan.md docs/plans/
mv structure_migration_plan.md docs/plans/
mv terminology_replacement_strategy.md docs/plans/
mv governance_files_migration_plan.md docs/plans/
mv naming_governance_analysis_task.md docs/plans/
mv naming_governance_structure_definition.md docs/plans/

# 移動階段報告
mv phase1_semantic_models.md docs/phases/
mv phase2_comprehensive_alignment_report.md docs/phases/
mv phase3_gl_root_reconstruction.md docs/phases/
mv phase4_gl_markers_compliance_summary.md docs/phases/

# 移動專案特定文檔
mv PROJECT_STRUCTURE_REBUILD_COMPLETE.md docs/projects/
mv radical_dependency_elimination_complete.md docs/projects/
mv structure_rebuild_verification_report.md docs/projects/

# 移動驗證文檔
mv GL_NAMING_ONTOLOGY_GAP_ANALYSIS.md docs/verification/
mv LOCAL_KNOWLEDGE_BASE.md docs/verification/
mv MAIN_BRANCH_FILE_PATH_VERIFICATION.md docs/verification/
mv platform_directory_structure_best_practices.md docs/verification/

# 移動遺留文檔
mv todo.md docs/archive/
```

## 驗證檢查
- [ ] 核心文檔在根目錄
- [ ] 所有其他文檔已移至 docs/ 下的適當子目錄
- [ ] 文檔分類清晰且有意義
- [ ] 根目錄清爽，只保留核心文檔
