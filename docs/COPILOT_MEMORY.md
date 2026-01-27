<!-- GL Layer: GL90-99 Meta-Specification Layer -->
<!-- Purpose: Provide repository Copilot Memory content and setup guidance -->
# GitHub Copilot Memory Guide

Use this guide to configure the repository Copilot Memory at:
`https://github.com/MachineNativeOps/machine-native-ops/settings/copilot/memory`.

## ✅ Copilot Memory Content (Paste into Settings)

```
Repository: MachineNativeOps/machine-native-ops
Purpose: AI-native governance platform with strict GL (Governance Layers) boundaries.

Key rules:
- Never modify files in controlplane/ (read-only).
- Respect GL layer boundaries (GL00-99); do not restructure governance artifacts or DAG topology.
- Prefer minimal, surgical changes; fix only task-related issues.
- Use Python 3.11+, TypeScript 5.x, Node.js 18+.
- Avoid eval(); use ast.literal_eval/json.loads when needed.

Build/Test/Lint:
- npm run lint / npm run build / npm run test
- make test
- python scripts/gl/validate-semantics.py
- python scripts/gl/quantum-validate.py
- npm run check:gl-compliance

Documentation:
- Copilot instructions live in .github/copilot-instructions.md.
- Project memory lives in workspace/PROJECT_MEMORY.md.
```

## 🧭 When to Update Memory

- Add new critical rules (security, governance, or workflow).
- Update build/test commands if they change.
- Add new restricted paths or processes.

## 📌 Related References

- [Copilot Instructions](../.github/copilot-instructions.md)
- [Project Memory](../workspace/PROJECT_MEMORY.md)
- [Developer Guidelines](DEVELOPER_GUIDELINES.md)
