# Integration Run

This folder packages a runnable pipeline using the real IndestructibleAutoOps engine and assets.

Contents:
- `project/`: A sample workspace copied from `examples/dirty_project`, used as the target project.
- `run.sh`: Drives the full flow (plan → repair+verify+seal → verify read-only) with the production configs.

Usage:
```bash
cd iaops/integration-run
./run.sh
```

The script writes evidence, plans, and seals inside `project/.indestructibleautoops`.
