# Phase 3: 命名规范统一 (Naming Convention Standardization: gl-* → gov-*)

## Objectives
- Systematically replace all `gl-*` prefixes with `gov-*` across the entire codebase
- Ensure all references are updated in files, directories, and documentation
- Maintain backward compatibility where needed
- Validate all changes before committing

## Tasks

### [ ] 3.1 Discovery and Inventory
- [ ] Scan all files for `gl-` prefix occurrences
- [ ] List all files and directories with `gl-` naming
- [ ] Create comprehensive inventory of changes needed
- [ ] Categorize by file type (code, config, docs, tests)

### [ ] 3.2 Batch Renaming Operations
- [ ] Rename all `gl-` prefixed directories to `gov-`
- [ ] Rename all `gl-` prefixed files to `gov-`
- [ ] Update all file content references (imports, paths, links)
- [ ] Update documentation references

### [ ] 3.3 Code Reference Updates
- [ ] Update Python import statements
- [ ] Update YAML configuration references
- [ ] Update shell script references
- [ ] Update Markdown documentation links

### [ ] 3.4 Validation and Testing
- [ ] Run syntax validation on all Python files
- [ ] Validate YAML configuration files
- [ ] Test import resolution
- [ ] Check for broken links in documentation

### [ ] 3.5 Documentation and Evidence
- [ ] Generate change log
- [ ] Create migration report
- [ ] Document any exceptions or special cases
- [ ] Validate backward compatibility needs

### [ ] 3.6 Commit and Push
- [ ] Stage all changes
- [ ] Create comprehensive commit message
- [ ] Push to feature branch
- [ ] Create pull request