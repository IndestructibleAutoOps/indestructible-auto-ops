<!-- @GL-governed -->
<!-- @GL-layer: GL90-99 -->
<!-- @GL-semantic: governed-documentation -->
<!-- @GL-audit-trail: engine/governance/GL_SEMANTIC_ANCHOR.json -->

<!--
@gov-layer GL-90-META
@gov-module engine/executor/docs
@gov-semantic-anchor GL-90-META-DOC
@gov-evidence-required false
-->

# Executor Stage - Stage 7

## Overview

The Executor Stage executes artifacts on local or remote systems, supporting commands, scripts, file operations, and service management with rollback capabilities.

## Components

### LocalExecutor
Local system executor.

**Features:**
- Execute shell commands
- Run scripts
- File operations (copy, mkdir, delete)
- Service management (systemctl)
- Dry-run mode
- Timeout handling

**Usage:**
```typescript
import { LocalExecutor } from './executor/local_executor';

const executor = new LocalExecutor({
  workingDir: '/workspace',
  dryRun: false
});
const result = await executor.execute(artifact, 'production');
```

### RemoteExecutor
Remote executor with SSH and API support.

**Features:**
- SSH command execution
- API endpoint execution
- Connection pooling
- Authentication handling
- Error recovery

**Usage:**
```typescript
import { RemoteExecutor } from './executor/remote_executor';

const executor = new RemoteExecutor({
  sshConfig: { host: 'remote-server', user: 'deploy' }
});
const result = await executor.execute(artifact, 'production');
```

### Rollback
Rollback manager with pre-execution backup.

**Features:**
- Pre-execution backup
- Restore capabilities
- Rollback history
- State verification

**Usage:**
```typescript
import { RollbackManager } from './executor/rollback';

const rollback = new RollbackManager();
await rollback.createBackup(artifact);
await rollback.execute(artifact, 'production');
if (failed) {
  await rollback.restore();
}
```

## Evidence Records

All executor operations generate evidence records with:
- Command/script details
- Execution output and errors
- Exit codes
- Performance metrics

## Output

**ExecutionResult:**
- `status`: 'success' | 'error' | 'warning'
- `output`: string - Command output
- `errors`: string[] - Any errors encountered
- `duration`: number - Execution time in ms
- `evidence`: EvidenceRecord[] - Complete evidence chain
