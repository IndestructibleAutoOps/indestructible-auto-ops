#!/usr/bin/env python3
"""
NG 閉環狀態鎖定引擎
State Locking Engine - Layer 0 (Non-bypassable)

SHA3-512 不可變狀態鎖定：
- 每個迴圈的初始狀態被密碼學鎖定
- 鎖定後不可修改、不可覆蓋
- 後續迴圈必須參照此基準
- 支援狀態鏈（每輪鎖定指向上一輪）
"""

from __future__ import annotations

import hashlib
import json
import copy
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha3_512(data: bytes) -> str:
    return hashlib.sha3_512(data).hexdigest()


def _canonical_json(obj: Any) -> bytes:
    """Deterministic JSON serialization for hashing."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


@dataclass
class CycleParameters:
    """迴圈可測量參數"""
    name: str
    value: float
    tolerance: float
    unit: str = ""


@dataclass
class StateLock:
    """不可變狀態鎖定"""
    cycle_id: str
    sequence: int
    timestamp: str
    state_hash: str
    parent_hash: Optional[str]  # 上一輪的 hash（形成鏈）
    parameters: List[Dict[str, Any]]
    assumptions: List[str]
    external_constraints: Dict[str, Any]
    locked: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class StateLockChain:
    """
    狀態鎖定鏈

    每個迴圈的初始狀態形成不可變鏈：
      Lock_0 -> Lock_1 -> Lock_2 -> ...
    每個鎖定包含指向上一個的 parent_hash。
    """

    def __init__(self, storage_path: Optional[Path] = None):
        self._chain: List[StateLock] = []
        self._storage_path = storage_path

    @property
    def length(self) -> int:
        return len(self._chain)

    @property
    def latest(self) -> Optional[StateLock]:
        return self._chain[-1] if self._chain else None

    def lock_initial_state(
        self,
        cycle_id: str,
        parameters: List[CycleParameters],
        assumptions: List[str],
        external_constraints: Dict[str, Any],
    ) -> StateLock:
        """
        鎖定一個新迴圈的初始狀態。

        Returns:
            不可變的 StateLock
        Raises:
            ValueError: 如果 cycle_id 已存在
        """
        if any(lock.cycle_id == cycle_id for lock in self._chain):
            raise ValueError(f"Cycle '{cycle_id}' already locked")

        parent_hash = self._chain[-1].state_hash if self._chain else None
        sequence = len(self._chain)
        timestamp = _utc_now()

        param_dicts = [asdict(p) for p in parameters]

        hashable_payload = {
            "cycle_id": cycle_id,
            "sequence": sequence,
            "timestamp": timestamp,
            "parent_hash": parent_hash,
            "parameters": param_dicts,
            "assumptions": sorted(assumptions),
            "external_constraints": external_constraints,
        }

        state_hash = _sha3_512(_canonical_json(hashable_payload))

        lock = StateLock(
            cycle_id=cycle_id,
            sequence=sequence,
            timestamp=timestamp,
            state_hash=state_hash,
            parent_hash=parent_hash,
            parameters=param_dicts,
            assumptions=sorted(assumptions),
            external_constraints=external_constraints,
            locked=True,
        )

        self._chain.append(lock)
        self._persist()
        return lock

    def verify_chain_integrity(self) -> Dict[str, Any]:
        """
        驗證整條鏈的完整性。

        Returns:
            {"valid": bool, "errors": [...], "length": int}
        """
        errors: List[str] = []

        for i, lock in enumerate(self._chain):
            # 1. 驗證序列號
            if lock.sequence != i:
                errors.append(f"Lock {i}: sequence mismatch (expected {i}, got {lock.sequence})")

            # 2. 驗證 parent_hash
            if i == 0:
                if lock.parent_hash is not None:
                    errors.append("Lock 0: parent_hash should be None")
            else:
                expected_parent = self._chain[i - 1].state_hash
                if lock.parent_hash != expected_parent:
                    errors.append(f"Lock {i}: parent_hash mismatch")

            # 3. 重新計算 hash 驗證未被篡改
            hashable_payload = {
                "cycle_id": lock.cycle_id,
                "sequence": lock.sequence,
                "timestamp": lock.timestamp,
                "parent_hash": lock.parent_hash,
                "parameters": lock.parameters,
                "assumptions": lock.assumptions,
                "external_constraints": lock.external_constraints,
            }
            recomputed = _sha3_512(_canonical_json(hashable_payload))
            if recomputed != lock.state_hash:
                errors.append(f"Lock {i}: hash tampered (recomputed != stored)")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "length": len(self._chain),
        }

    def get_parameter_drift(self, param_name: str) -> List[Dict[str, Any]]:
        """
        追蹤特定參數在各迴圈間的漂移。

        Returns:
            [{"cycle_id": ..., "value": ..., "tolerance": ..., "within_tolerance": bool}, ...]
        """
        drift: List[Dict[str, Any]] = []
        baseline_value: Optional[float] = None

        for lock in self._chain:
            for p in lock.parameters:
                if p["name"] == param_name:
                    value = p["value"]
                    tolerance = p["tolerance"]

                    if baseline_value is None:
                        baseline_value = value

                    within = abs(value - baseline_value) <= tolerance

                    drift.append({
                        "cycle_id": lock.cycle_id,
                        "value": value,
                        "tolerance": tolerance,
                        "baseline": baseline_value,
                        "deviation": value - baseline_value,
                        "within_tolerance": within,
                    })
                    break

        return drift

    def export_chain(self) -> List[Dict[str, Any]]:
        """導出完整鏈（用於審計）"""
        return [lock.to_dict() for lock in self._chain]

    def _persist(self) -> None:
        if self._storage_path is not None:
            self._storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._storage_path, "w", encoding="utf-8") as f:
                json.dump(self.export_chain(), f, indent=2, ensure_ascii=False)
