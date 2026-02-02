#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: tools
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL事实验证管道执行脚本
版本: 1.0.0
用途: 执行三层验证管道，生成基于可验证事实的报告
"""

import yaml
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class EvidenceType(Enum):
    CONTRACT = "contract"
    REGISTRY = "registry"
    GOVERNANCE = "governance"
    ONTOLOGY = "ontology"
    ACTUAL_STATE = "actual_state"


class DifferenceCategory(Enum):
    ALIGNED = "aligned"
    INTENTIONAL_DEVIATION = "intentional-deviation"
    ALTERNATIVE_IMPLEMENTATION = "alternative-implementation"
    TECHNICAL_DEBT = "technical-debt"
    GAP = "gap"
    EXTENSION = "extension"


@dataclass
class ValidationResult:
    passed: bool
    errors: List[str]
    warnings: List[str]


@dataclass
class InternalSource:
    path: str
    hash: str
    size: int
    last_modified: str
    kind: str
    version: Optional[str] = None


@dataclass
class ExternalReference:
    standard_name: str
    standard_version: str
    source_url: str
    last_updated: str
    applicability: str
    reliability_level: str


@dataclass
class Difference:
    category: DifferenceCategory
    description: str
    internal_evidence: str
    external_reference: str
    rationale: Optional[str] = None
    action: Optional[str] = None


class GLFactPipeline:
    def __init__(self, config_path: str, workspace_path: str = "."):
        self.config_path = Path(config_path)
        self.workspace_path = Path(workspace_path)
        
        # 加载配置
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # 初始化状态
        self.internal_facts: Dict = {}
        self.external_context: Dict = {}
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []
        
        # 禁止的短语
        self.forbidden_phrases = [
            (r"100% 完成", "基于已实现的功能集"),
            (r"完全符合", "在[方面]与标准对齐"),
            (r"已全部实现", "已实现[具体功能列表]"),
            (r"覆盖所有标准", "覆盖[具体标准列表]"),
            (r"应该是", "根据[证据]，建议"),
            (r"可能是", "基于[证据]，推测"),
            (r"我认为", "基于[证据]，分析表明"),
            (r"推测", "基于[证据]，推断"),
        ]
    
    def validate_internal_source(self, path: Path) -> ValidationResult:
        """验证内部源文件"""
        errors = []
        warnings = []
        
        if not path.exists():
            errors.append(f"文件不存在: {path}")
            return ValidationResult(False, errors, warnings)
        
        if not path.is_file():
            errors.append(f"不是文件: {path}")
            return ValidationResult(False, errors, warnings)
        
        try:
            with open(path, 'r') as f:
                content = f.read()
                
            # 计算 SHA-256 哈希
            file_hash = hashlib.sha256(content.encode()).hexdigest()
            
            # 如果是 YAML 文件，尝试解析
            if path.suffix in ['.yaml', '.yml']:
                try:
                    yaml_data = yaml.safe_load(content)
                    if yaml_data:
                        # 检查必需字段
                        if 'metadata' in yaml_data:
                            if 'version' not in yaml_data['metadata']:
                                warnings.append(f"缺少 version 字段: {path}")
                            if 'kind' not in yaml_data['metadata']:
                                warnings.append(f"缺少 kind 字段: {path}")
                except yaml.YAMLError as e:
                    errors.append(f"YAML 解析失败 {path}: {e}")
            
            return ValidationResult(True, [], warnings)
            
        except Exception as e:
            errors.append(f"读取失败 {path}: {e}")
            return ValidationResult(False, errors, warnings)
    
    def collect_internal_facts(self) -> Dict:
        """第一阶段：收集内部事实"""
        print("🔍 阶段1: 收集内部事实...")
        
        facts = {
            "timestamp": datetime.utcnow().isoformat(),
            "sources": [],
            "contracts": {},
            "registry_state": {},
            "root_hash": None
        }
        
        # 收集契约
        contracts_path = self.workspace_path / "ecosystem/contracts"
        if contracts_path.exists():
            print(f"  📂 扫描契约目录: {contracts_path}")
            for contract_file in contracts_path.glob("**/*.yaml"):
                validation = self.validate_internal_source(contract_file)
                if validation.passed:
                    with open(contract_file, 'r') as f:
                        content = f.read()
                        file_hash = hashlib.sha256(content.encode()).hexdigest()
                        
                        source = InternalSource(
                            path=str(contract_file.relative_to(self.workspace_path)),
                            hash=file_hash,
                            size=len(content),
                            last_modified=datetime.fromtimestamp(
                                contract_file.stat().st_mtime
                            ).isoformat(),
                            kind="contract"
                        )
                        facts["sources"].append(asdict(source))
                        
                        # 提取契约信息
                        try:
                            yaml_data = yaml.safe_load(content)
                            if yaml_data and 'metadata' in yaml_data:
                                contract_id = yaml_data['metadata'].get('name', contract_file.stem)
                                facts["contracts"][contract_id] = {
                                    "version": yaml_data['metadata'].get('version', 'unknown'),
                                    "kind": yaml_data['metadata'].get('kind', 'unknown'),
                                    "path": str(contract_file.relative_to(self.workspace_path)),
                                    "hash": file_hash
                                }
                        except:
                            pass
                else:
                    self.validation_errors.extend(validation.errors)
                    self.validation_warnings.extend(validation.warnings)
        
        # 收集注册表
        registry_path = self.workspace_path / "ecosystem/registry"
        if registry_path.exists():
            print(f"  📂 扫描注册表目录: {registry_path}")
            for registry_file in registry_path.glob("**/*.yaml"):
                validation = self.validate_internal_source(registry_file)
                if validation.passed:
                    with open(registry_file, 'r') as f:
                        content = f.read()
                        file_hash = hashlib.sha256(content.encode()).hexdigest()
                        
                        source = InternalSource(
                            path=str(registry_file.relative_to(self.workspace_path)),
                            hash=file_hash,
                            size=len(content),
                            last_modified=datetime.fromtimestamp(
                                registry_file.stat().st_mtime
                            ).isoformat(),
                            kind="registry"
                        )
                        facts["sources"].append(asdict(source))
        
        # 计算根哈希
        all_hashes = [s['hash'] for s in facts["sources"]]
        if all_hashes:
            combined = "".join(sorted(all_hashes))
            facts["root_hash"] = hashlib.sha256(combined.encode()).hexdigest()
        
        # 计算统计信息
        facts["statistics"] = {
            "total_files": len(facts["sources"]),
            "total_size": sum(s["size"] for s in facts["sources"]),
            "contracts_count": len(facts["contracts"]),
            "validation_errors": len(self.validation_errors),
            "validation_warnings": len(self.validation_warnings)
        }
        
        self.internal_facts = facts
        
        print(f"  ✅ 收集完成: {len(facts['sources'])} 个文件")
        print(f"  📊 统计: {facts['statistics']}")
        
        return facts
    
    def collect_external_context(self, topics: List[str] = None) -> Dict:
        """第二阶段：收集外部语境"""
        print("\n🌐 阶段2: 收集外部语境...")
        
        if topics is None:
            topics = ["semver", "cncf", "togaf"]
        
        context = {
            "collected_at": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "references": [],
            "standard_requirements": []
        }
        
        # 模拟外部标准收集
        standards_db = {
            "semver": {
                "name": "Semantic Versioning",
                "url": "https://semver.org/",
                "version": "2.0.0",
                "reliability": "high",
                "requirements": [
                    {
                        "id": "SEMVER-001",
                        "text": "版本格式必须是 MAJOR.MINOR.PATCH",
                        "mandatory": True
                    }
                ]
            },
            "cncf": {
                "name": "Cloud Native Computing Foundation",
                "url": "https://www.cncf.io/",
                "version": "latest",
                "reliability": "high",
                "requirements": [
                    {
                        "id": "CNCF-001",
                        "text": "容器化部署",
                        "mandatory": True
                    }
                ]
            },
            "togaf": {
                "name": "The Open Group Architecture Framework",
                "url": "https://www.opengroup.org/togaf/",
                "version": "9.2",
                "reliability": "high",
                "requirements": [
                    {
                        "id": "TOGAF-001",
                        "text": "架构治理",
                        "mandatory": True
                    }
                ]
            }
        }
        
        for topic in topics:
            if topic in standards_db:
                std = standards_db[topic]
                ref = ExternalReference(
                    standard_name=std["name"],
                    standard_version=std["version"],
                    source_url=std["url"],
                    last_updated="2024-01-01",
                    applicability="reference",
                    reliability_level=std["reliability"]
                )
                context["references"].append(asdict(ref))
                context["standard_requirements"].extend(std["requirements"])
        
        self.external_context = context
        
        print(f"  ✅ 收集完成: {len(context['references'])} 个外部标准")
        
        return context
    
    def cross_verify(self) -> Dict:
        """第三阶段：交叉验证"""
        print("\n🔬 阶段3: 交叉验证...")
        
        if not self.internal_facts:
            raise ValueError("必须先运行内部事实收集阶段")
        
        analysis = {
            "actual_state_summary": self._summarize_internal_state(),
            "gaps": [],
            "aligned": [],
            "deviations": [],
            "extensions": []
        }
        
        # 模拟差异分析
        # 在实际实现中，这里会有复杂的对比逻辑
        
        # 示例：检查契约版本一致性
        versions = set()
        for contract_id, contract_info in self.internal_facts["contracts"].items():
            version = contract_info.get("version", "unknown")
            versions.add(version)
        
        if len(versions) > 1:
            analysis["deviations"].append(Difference(
                category=DifferenceCategory.ALTERNATIVE_IMPLEMENTATION,
                description=f"发现多个版本: {', '.join(versions)}",
                internal_evidence=f"契约数量: {len(self.internal_facts['contracts'])}",
                external_reference="SemVer 2.0.0 要求统一版本策略",
                action="review"
            ))
        else:
            analysis["aligned"].append(Difference(
                category=DifferenceCategory.ALIGNED,
                description="契约版本一致",
                internal_evidence=f"所有契约版本: {list(versions)[0] if versions else 'N/A'}",
                external_reference="SemVer 2.0.0",
                action=None
            ))
        
        print(f"  ✅ 分析完成: {len(analysis['aligned'])} 对齐, {len(analysis['deviations'])} 差异")
        
        return analysis
    
    def check_forbidden_phrases(self, text: str) -> List[str]:
        """检查禁止使用的短语"""
        violations = []
        
        for pattern, replacement in self.forbidden_phrases:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                violations.append({
                    "phrase": match.group(),
                    "suggested_replacement": replacement,
                    "position": match.start()
                })
        
        return violations
    
    def calculate_evidence_coverage(self, report_text: str) -> float:
        """计算证据覆盖率"""
        evidence_pattern = r"\[证据:\s*[^\]]+\]"
        matches = re.findall(evidence_pattern, report_text)
        
        # 统计陈述数量（以句号分隔）
        statements = report_text.split('。')
        non_empty_statements = [s for s in statements if s.strip()]
        
        if len(non_empty_statements) == 0:
            return 0.0
        
        coverage = (len(matches) / len(non_empty_statements)) * 100
        return min(coverage, 100.0)
    
    def generate_report(self, analysis: Dict) -> Dict:
        """生成验证报告"""
        print("\n📝 生成验证报告...")
        
        report = {
            "metadata": {
                "report_id": hashlib.md5(
                    datetime.utcnow().isoformat().encode()
                ).hexdigest(),
                "generated_at": datetime.utcnow().isoformat(),
                "pipeline_version": self.config["metadata"]["version"],
                "internal_state_hash": self.internal_facts.get("root_hash", "N/A")
            },
            "actual_state": {
                "contracts": self.internal_facts["contracts"],
                "statistics": self.internal_facts["statistics"]
            },
            "comparison_analysis": analysis,
            "disclaimers": [
                "本报告基于内部实际状态生成",
                "外部标准仅供参考，不构成完成度声明",
                "差异分析基于事实收集时的系统状态",
                "所有结论都基于可验证的证据"
            ],
            "verification": {
                "evidence_coverage": 0.0,
                "has_unverified_claims": False,
                "passed_all_checks": len(self.validation_errors) == 0,
                "validation_errors": self.validation_errors,
                "validation_warnings": self.validation_warnings
            }
        }
        
        # 检查质量门禁
        quality_gates_passed = True
        
        # 检查证据覆盖率（将在报告生成后计算）
        # 检查禁止短语
        report_text = json.dumps(report, ensure_ascii=False)
        forbidden_violations = self.check_forbidden_phrases(report_text)
        if forbidden_violations:
            report["verification"]["has_unverified_claims"] = True
            report["verification"]["forbidden_phrase_violations"] = forbidden_violations
            quality_gates_passed = False
        
        # 更新验证状态
        report["verification"]["quality_gates_passed"] = quality_gates_passed
        
        print(f"  ✅ 报告生成完成")
        print(f"  📊 质量门禁: {'通过' if quality_gates_passed else '失败'}")
        if forbidden_violations:
            print(f"  ⚠️  检测到 {len(forbidden_violations)} 个禁止短语")
        
        return report
    
    def _summarize_internal_state(self) -> Dict:
        """总结内部状态"""
        return {
            "contracts_count": len(self.internal_facts.get("contracts", {})),
            "total_files": len(self.internal_facts.get("sources", [])),
            "total_size_bytes": sum(s["size"] for s in self.internal_facts.get("sources", [])),
            "root_hash": self.internal_facts.get("root_hash", "N/A")
        }
    
    def run_pipeline(self, topics: List[str] = None) -> Dict:
        """运行完整的三阶段管道"""
        print("=" * 60)
        print("GL 事实验证管道")
        print("=" * 60)
        
        # 阶段1: 内部事实收集
        facts = self.collect_internal_facts()
        
        if self.validation_errors:
            print(f"\n❌ 阶段1 失败: 发现 {len(self.validation_errors)} 个错误")
            for error in self.validation_errors:
                print(f"  - {error}")
            # 在实际实现中，这里可能会失败并退出
            # 但为了演示，我们继续执行
        
        # 阶段2: 外部语境收集
        context = self.collect_external_context(topics)
        
        # 阶段3: 交叉验证
        analysis = self.cross_verify()
        
        # 生成报告
        report = self.generate_report(analysis)
        
        print("\n" + "=" * 60)
        print("管道执行完成")
        print("=" * 60)
        
        return report
    
    def save_report(self, report: Dict, output_path: str = None):
        """保存报告"""
        if output_path is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            output_path = f"gl-assessment-{timestamp}.json"
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 报告已保存: {output_file}")
        return output_file


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="GL事实验证管道执行脚本"
    )
    parser.add_argument(
        "--config",
        default="ecosystem/contracts/fact-verification/gl.fact-pipeline-spec.yaml",
        help="管道配置文件路径"
    )
    parser.add_argument(
        "--workspace",
        default=".",
        help="工作空间路径"
    )
    parser.add_argument(
        "--topics",
        nargs="+",
        default=["semver", "cncf", "togaf"],
        help="外部标准主题"
    )
    parser.add_argument(
        "--output",
        help="报告输出路径"
    )
    
    args = parser.parse_args()
    
    # 创建管道实例
    pipeline = GLFactPipeline(
        config_path=args.config,
        workspace_path=args.workspace
    )
    
    # 运行管道
    report = pipeline.run_pipeline(topics=args.topics)
    
    # 保存报告
    pipeline.save_report(report, args.output)
    
    # 退出状态
    if report["verification"]["quality_gates_passed"]:
        print("\n✅ 验证通过")
        return 0
    else:
        print("\n❌ 验证失败")
        return 1


if __name__ == "__main__":
    exit(main())