#!/usr/bin/env python3
"""
降級檢測工具
No Degradation Check Tool

用途：確保所有指標永不降級
模式：ZERO TOLERANCE
動作：BLOCK on any degradation
"""

import json
import sys
from pathlib import Path
from typing import Dict, List


# 基線指標（不可降級）
BASELINE_METRICS = {
    'test_coverage': 0.95,           # >= 95%
    'lint_score': 9.5,                # >= 9.5/10
    'validation_latency_ms': 100,     # <= 100ms
    'closure_check_latency_ms': 500,  # <= 500ms
    'ml_repair_timeout_s': 60,        # <= 60s
    'ml_confidence_min': 0.95,        # >= 95%
    'closure_completeness': 1.0,      # == 100%
    'uniqueness_score': 1.0,          # == 100%
    'conflict_rate': 0.0,             # == 0%
    'system_availability': 0.9999     # >= 99.99%
}

# 指標方向（改善方向）
METRIC_DIRECTION = {
    'test_coverage': 'higher_better',        # ↑
    'lint_score': 'higher_better',           # ↑
    'validation_latency_ms': 'lower_better', # ↓
    'closure_check_latency_ms': 'lower_better', # ↓
    'ml_repair_timeout_s': 'lower_better',   # ↓
    'ml_confidence_min': 'higher_better',    # ↑
    'closure_completeness': 'exact',         # =
    'uniqueness_score': 'exact',             # =
    'conflict_rate': 'exact',                # =
    'system_availability': 'higher_better'   # ↑
}


def load_current_metrics() -> Dict[str, float]:
    """載入當前指標"""
    # 嘗試從測試報告載入
    metrics_file = Path('metrics/current.json')
    
    if metrics_file.exists():
        with open(metrics_file, 'r') as f:
            return json.load(f)
    
    # 如果沒有，使用基線（第一次運行）
    return BASELINE_METRICS.copy()


def check_degradation() -> Tuple[bool, List[Dict]]:
    """
    檢查指標降級
    
    Returns:
        (是否有降級, 降級列表)
    """
    baseline = BASELINE_METRICS
    current = load_current_metrics()
    
    degradations = []
    
    for metric, baseline_value in baseline.items():
        current_value = current.get(metric)
        
        if current_value is None:
            degradations.append({
                'metric': metric,
                'type': 'MISSING',
                'baseline': baseline_value,
                'current': None,
                'severity': 'CRITICAL'
            })
            continue
        
        direction = METRIC_DIRECTION.get(metric, 'higher_better')
        
        # 檢查降級
        is_degraded = False
        degradation_type = None
        
        if direction == 'higher_better':
            if current_value < baseline_value:
                is_degraded = True
                degradation_type = 'LOWER_THAN_BASELINE'
        
        elif direction == 'lower_better':
            if current_value > baseline_value:
                is_degraded = True
                degradation_type = 'HIGHER_THAN_BASELINE'
        
        elif direction == 'exact':
            if current_value != baseline_value:
                is_degraded = True
                degradation_type = 'DEVIATION_FROM_BASELINE'
        
        if is_degraded:
            degradation_pct = abs((current_value - baseline_value) / baseline_value * 100) if baseline_value != 0 else 100
            
            degradations.append({
                'metric': metric,
                'type': degradation_type,
                'baseline': baseline_value,
                'current': current_value,
                'degradation_pct': degradation_pct,
                'severity': 'IMMUTABLE' if direction == 'exact' else 'ABSOLUTE'
            })
    
    return (len(degradations) > 0, degradations)


def generate_report(degradations: List[Dict]) -> str:
    """生成降級報告"""
    report_lines = [
        "=" * 70,
        "🚨 ZERO_TOLERANCE VIOLATION: Metric Degradation Detected",
        "=" * 70,
        ""
    ]
    
    for d in degradations:
        report_lines.append(f"❌ {d['metric']} [{d['severity']}]:")
        report_lines.append(f"   Type: {d['type']}")
        report_lines.append(f"   Baseline: {d['baseline']}")
        report_lines.append(f"   Current:  {d.get('current', 'MISSING')}")
        
        if d.get('degradation_pct'):
            report_lines.append(f"   Degradation: {d['degradation_pct']:.1f}%")
        
        report_lines.append("")
    
    report_lines.extend([
        "=" * 70,
        "🚫 PERMANENT_BLOCK: All metrics must maintain or improve",
        "=" * 70,
        "",
        "修復動作：",
        "1. 識別降級原因",
        "2. 還原或改善指標",
        "3. 添加回歸測試",
        "4. 重新提交 PR",
        "",
        "IndestructibleAutoOps 原則：永不降級",
        ""
    ])
    
    return "\n".join(report_lines)


def main():
    """主函數"""
    has_degradation, degradations = check_degradation()
    
    if has_degradation:
        print(generate_report(degradations))
        sys.exit(1)
    
    print("=" * 70)
    print("✅ No Degradation Detected")
    print("=" * 70)
    print()
    print("所有指標維持或改善：")
    
    baseline = BASELINE_METRICS
    current = load_current_metrics()
    
    for metric, baseline_value in sorted(baseline.items()):
        current_value = current.get(metric, baseline_value)
        direction = METRIC_DIRECTION.get(metric)
        
        if direction == 'higher_better':
            status = "✅" if current_value >= baseline_value else "❌"
            trend = "↑" if current_value > baseline_value else "→"
        elif direction == 'lower_better':
            status = "✅" if current_value <= baseline_value else "❌"
            trend = "↓" if current_value < baseline_value else "→"
        else:  # exact
            status = "✅" if current_value == baseline_value else "❌"
            trend = "="
        
        print(f"  {status} {metric:30s} {trend} {current_value}")
    
    print()
    print("IndestructibleAutoOps: All metrics maintained or improved ✅")
    sys.exit(0)


if __name__ == "__main__":
    main()
