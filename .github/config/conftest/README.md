<!-- @GL-governed -->
<!-- @GL-layer: GL90-99 -->
<!-- @GL-semantic: governed-documentation -->
<!-- @GL-audit-trail: engine/governance/GL_SEMANTIC_ANCHOR.json -->

# Conftest Configuration

This directory contains the Conftest framework configuration.

## Structure

```
.config/
└── conftest/
    └── policies -> ../../.meta/policies/  # Symlink to centralized policies
```

## Usage

Conftest policies are centralized in `.meta/policies/`. This directory only contains framework configuration.

## Running Policy Checks

```bash
conftest test <file> -p .meta/policies/
```

## See Also

- [Conftest Documentation]([EXTERNAL_URL_REMOVED])
- [Policies Directory](../../.meta/policies/)
