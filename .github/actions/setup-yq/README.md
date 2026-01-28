# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# yq - portable yaml processor

A reusable GitHub Action for installing yq, a lightweight and portable command-line YAML processor.

## About

This action installs [yq](https://github.com/mikefarah/yq) which is used throughout the MachineNativeOps repository for:
- Reading version numbers from YAML configuration files
- Validating YAML file syntax
- Parsing and manipulating YAML data in scripts and workflows

## Usage

```yaml
- name: Setup yq
  uses: ./.github/actions/setup-yq
  
- name: Read version from YAML
  run: |
    VERSION=$(yq eval '.version' machinenativeops.yaml)
    echo "Project version: $VERSION"
```

## Example Workflow

```yaml
name: Example Workflow
on: [push]

jobs:
  example:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Setup yq
        uses: ./.github/actions/setup-yq
        
      - name: Process YAML files
        run: |
          yq eval '.version' machinenativeops.yaml
          yq eval '.status.deploymentStatus' config.yaml
```

## Version

This action uses `mikefarah/yq@v4.50.1`.

## References

- [yq GitHub Repository](https://github.com/mikefarah/yq)
- [yq Documentation](https://mikefarah.gitbook.io/yq/)
- [VERSION_MANAGEMENT.md](../../../workspace/docs/VERSION_MANAGEMENT.md) - How yq is used for version management in this repository
