<!-- @GL-governed -->
<!-- @GL-layer: GL90-99 -->
<!-- @GL-semantic: governed-documentation -->
<!-- @GL-audit-trail: engine/governance/GL_SEMANTIC_ANCHOR.json -->

# CodeQL Workflow Fix

## Issue
The CodeQL workflow was failing due to the `nodejs/is-my-node-vulnerable@v1.6.1` action failing with:
```
Error: Did not get exactly one version record for v20.x
```

## Root Cause
The workflow used `nodejs/is-my-node-vulnerable@v1.6.1`, which reads the installed Node.js version; because Node.js was set up with a wildcard pattern (`node-version: 'lts/*'`), the action failed to resolve this LTS wildcard (for example, `v20.x`) to exactly one concrete version record in its vulnerability database.

## Fix
For the CodeQL workflow, the "Check Node.js for vulnerabilities" step using `nodejs/is-my-node-vulnerable@v1.6.1` was removed because it was:
1. Not essential for CodeQL scanning
2. Causing the entire workflow to fail
3. Blocking the javascript-typescript CodeQL analysis

Other workflows in this repository (`publish-npm-packages.yml`, `static.yml`, and `typescript-build-check.yml`) still use the same `nodejs/is-my-node-vulnerable@v1.6.1` action. To avoid similar failures and keep behavior consistent across workflows, one of the following approaches should be applied there as well:
1. Remove the "Check Node.js for vulnerabilities" step if it is not required for that workflow, **or**
2. Mark the step with `continue-on-error: true` so that failures in the vulnerability check do not fail the entire workflow, **or**
3. Configure the step to use an explicit Node.js version (for example, `20.x`) instead of a wildcard such as `lts/*` to avoid version resolution issues.

## Result
After removing this step from the CodeQL workflow, the CodeQL analysis can complete successfully for all three languages:
- actions
- javascript-typescript
- python

Similar stability can be achieved for `publish-npm-packages.yml`, `static.yml`, and `typescript-build-check.yml` once one of the consistent approaches above is applied to their `nodejs/is-my-node-vulnerable@v1.6.1` usage.
