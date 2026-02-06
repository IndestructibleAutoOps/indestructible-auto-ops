#!/usr/bin/env python3
"""
Semanticizer - Language-Neutral Semantic Tokenization System

Converts natural language input from any language to English semantic tokens/AST.
This enables language-neutral canonical hashing for cross-language governance sealing.

Author: IndestructibleAutoOps
Version: 1.0
Date: 2024-02-05
"""

import json
import re
import sys
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime


class Language(Enum):
    """Supported source languages"""
    ZH = "zh"  # Chinese (Simplified)
    EN = "en"  # English (Semantic Anchor)
    JA = "ja"  # Japanese
    KO = "ko"  # Korean
    DE = "de"  # German
    FR = "fr"  # French


class SemanticAction(Enum):
    """Semantic action types"""
    RESTART_SERVICE = "restart_service"
    DEPLOY_ARTIFACT = "deploy_artifact"
    PATCH_VULNERABILITY = "patch_vulnerability"
    ROLLBACK_DEPLOYMENT = "rollback_deployment"
    SCALE_COMPONENT = "scale_component"
    CONFIGURE_SYSTEM = "configure_system"
    VALIDATE_COMPLIANCE = "validate_compliance"
    EXECUTE_REMEDIATION = "execute_remediation"
    GENERATE_REPORT = "generate_report"
    SEAL_ERA = "seal_era"
    VERIFY_HASH = "verify_hash"
    MIGRATE_DATA = "migrate_data"
    BACKUP_DATA = "backup_data"
    RESTORE_DATA = "restore_data"


class SemanticResult(Enum):
    """Semantic result types"""
    SUCCESS = "success"
    FAILURE = "failure"
    IN_PROGRESS = "in_progress"
    PARTIAL = "partial"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class SemanticTokenAST:
    """
    Abstract Syntax Tree of semantic tokens.
    This is the canonical representation used for hashing.
    """
    action: str
    target: Optional[str]
    timestamp: str
    actor: str
    result: str
    metadata: Dict[str, str]
    parameters: Optional[Dict[str, str]] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to canonical JSON"""
        return json.dumps(self.to_dict(), indent=2, sort_keys=True, ensure_ascii=False)


class Semanticizer:
    """
    Language-Neutral Semantic Tokenization Engine
    
    Converts natural language input from any supported language to
    English semantic tokens/AST for language-neutral hashing.
    """
    
    # Action patterns for different languages
    ACTION_PATTERNS = {
        Language.ZH: {
            SemanticAction.RESTART_SERVICE: r"(?:重新啟動|restart|重啟)(?:了|過|著)?\s+(?P<target>[\w\-\.]+)",
            SemanticAction.DEPLOY_ARTIFACT: r"(?:部署|deploy|發布|release)(?:了|過|著)?\s+(?P<target>[\w\-\.]+)",
            SemanticAction.PATCH_VULNERABILITY: r"(?:修復|修補|patch|fix)(?:了|過|著)?\s+(?P<target>[\w\-\.]+)",
            SemanticAction.ROLLBACK_DEPLOYMENT: r"(?:回滾|rollback|撤回|revert)(?:了|過|著)?\s+(?P<target>[\w\-\.]+)",
            SemanticAction.SCALE_COMPONENT: r"(?:擴展|scale|擴容|擴縮)(?:了|過|著)?\s+(?P<target>[\w\-\.]+)",
            SemanticAction.CONFIGURE_SYSTEM: r"(?:配置|configure|設定|setup)(?:了|過|著)?\s+(?P<target>[\w\-\.]+)",
            SemanticAction.VALIDATE_COMPLIANCE: r"(?:驗證|validate|檢查|check)(?:了|過|著)?\s+(?P<target>[\w\-\.]+)",
            SemanticAction.EXECUTE_REMEDIATION: r"(?:執行|execute|實施|implement)(?:了|過|著)?\s+(?P<target>[\w\-\.]+)",
        },
        Language.EN: {
            SemanticAction.RESTART_SERVICE: r"(?:restarted|restart|reboot).*?(?:\s+|\s+the\s+)(?P<target>[\w\-\.]+)",
            SemanticAction.DEPLOY_ARTIFACT: r"(?:deployed|deploy|release|publish).*?(?:\s+|\s+the\s+)(?P<target>[\w\-\.]+)",
            SemanticAction.PATCH_VULNERABILITY: r"(?:patched|patch|fixed|fix|repair).*?(?:\s+|\s+the\s+)(?P<target>[\w\-\.]+)",
            SemanticAction.ROLLBACK_DEPLOYMENT: r"(?:rolled back|rollback|revert).*?(?:\s+|\s+the\s+)(?P<target>[\w\-\.]+)",
            SemanticAction.SCALE_COMPONENT: r"(?:scaled|scale|expand|shrink).*?(?:\s+|\s+the\s+)(?P<target>[\w\-\.]+)",
            SemanticAction.CONFIGURE_SYSTEM: r"(?:configured|configure|setup).*?(?:\s+|\s+the\s+)(?P<target>[\w\-\.]+)",
            SemanticAction.VALIDATE_COMPLIANCE: r"(?:validated|validate|verified|verify|checked|check).*?(?:\s+|\s+the\s+)(?P<target>[\w\-\.]+)",
            SemanticAction.EXECUTE_REMEDIATION: r"(?:executed|execute|implemented|implement).*?(?:\s+|\s+the\s+)(?P<target>[\w\-\.]+)",
        },
        Language.JA: {
            SemanticAction.RESTART_SERVICE: r"(?P<target>[\w\-\.]+)\s*(?:を| Wo)?\s*(?:再起動|restart|再起)し(?:まし|ました)?",
            SemanticAction.DEPLOY_ARTIFACT: r"(?P<target>[\w\-\.]+)\s*(?:を| Wo)?\s*(?:展開|deploy|デプロイ)し(?:まし|ました)?",
            SemanticAction.PATCH_VULNERABILITY: r"(?P<target>[\w\-\.]+)\s*(?:を| Wo)?\s*(?:修正|patch|fix)し(?:まし|ました)?",
            SemanticAction.ROLLBACK_DEPLOYMENT: r"(?P<target>[\w\-\.]+)\s*(?:を| Wo)?\s*(?:ロールバック|rollback)し(?:まし|ました)?",
            SemanticAction.SCALE_COMPONENT: r"(?P<target>[\w\-\.]+)\s*(?:を| Wo)?\s*(?:拡張|scale|スケール)し(?:まし|ました)?",
            SemanticAction.CONFIGURE_SYSTEM: r"(?P<target>[\w\-\.]+)\s*(?:を| Wo)?\s*(?:設定|configure|セットアップ)し(?:まし|ました)?",
            SemanticAction.VALIDATE_COMPLIANCE: r"(?P<target>[\w\-\.]+)\s*(?:を| Wo)?\s*(?:検証|validate|チェック)し(?:まし|ました)?",
            SemanticAction.EXECUTE_REMEDIATION: r"(?P<target>[\w\-\.]+)\s*(?:を| Wo)?\s*(?:実行|execute|適用)し(?:まし|ました)?",
        },
        Language.KO: {
            SemanticAction.RESTART_SERVICE: r"(재시작|restart|재부팅)",
            SemanticAction.DEPLOY_ARTIFACT: r"(배포|deploy)",
            SemanticAction.PATCH_VULNERABILITY: r"(수정|patch|fix)",
            SemanticAction.ROLLBACK_DEPLOYMENT: r"(롤백|rollback)",
            SemanticAction.SCALE_COMPONENT: r"(확장|scale|스케일)",
            SemanticAction.CONFIGURE_SYSTEM: r"(설정|configure|셋업)",
            SemanticAction.VALIDATE_COMPLIANCE: r"(검증|validate|확인|check)",
            SemanticAction.EXECUTE_REMEDIATION: r"(실행|execute|적용|apply)",
        },
    }
    
    # Result patterns
    RESULT_PATTERNS = {
        Language.ZH: {
            SemanticResult.SUCCESS: r"(成功|完成|順利|completed|successful)",
            SemanticResult.FAILURE: r"(失敗|錯誤|異常|failed|error)",
            SemanticResult.IN_PROGRESS: r"(進行中|執行中|processing|in_progress)",
            SemanticResult.PARTIAL: r"(部分|局部|partial)",
            SemanticResult.SKIPPED: r"(跳過|跳過|skipped)",
            SemanticResult.ERROR: r"(錯誤|異常|error)",
        },
        Language.EN: {
            SemanticResult.SUCCESS: r"(success|successful|completed|done)",
            SemanticResult.FAILURE: r"(failed|failure|error|unsuccessful)",
            SemanticResult.IN_PROGRESS: r"(processing|in_progress|running)",
            SemanticResult.PARTIAL: r"(partial|partially)",
            SemanticResult.SKIPPED: r"(skipped|skip)",
            SemanticResult.ERROR: r"(error|exception)",
        },
        Language.JA: {
            SemanticResult.SUCCESS: r"(成功|完了|正常)",
            SemanticResult.FAILURE: r"(失敗|異常|エラー)",
            SemanticResult.IN_PROGRESS: r"(進行中|処理中)",
            SemanticResult.PARTIAL: r"(部分|一部)",
            SemanticResult.SKIPPED: r"(スキップ|skip)",
            SemanticResult.ERROR: r"(エラー|異常)",
        },
        Language.KO: {
            SemanticResult.SUCCESS: r"(성공|완료|정상)",
            SemanticResult.FAILURE: r"(실패|오류|이상)",
            SemanticResult.IN_PROGRESS: r"(진행 중|처리 중)",
            SemanticResult.PARTIAL: r"(부분|일부)",
            SemanticResult.SKIPPED: r"(건너뜀|skip)",
            SemanticResult.ERROR: r"(오류|이상|error)",
        },
    }
    
    # Common service/component names
    COMMON_TARGETS = {
        "nginx", "redis", "postgres", "postgresql", "mysql", "mongodb",
        "frontend", "backend", "database", "db", "api", "gateway",
        "production", "staging", "development", "dev", "test",
        "kubernetes", "k8s", "docker", "container", "pod", "service",
    }
    
    # Default actor
    DEFAULT_ACTOR = "indestructible_auto_ops_system"
    
    def __init__(self):
        """Initialize the semanticizer"""
        self.cache = {}
    
    def detect_language(self, text: str) -> Language:
        """
        Detect source language from text.
        Simple heuristic based on character sets.
        """
        # Check for Chinese characters
        if re.search(r'[\u4e00-\u9fff]', text):
            return Language.ZH
        
        # Check for Japanese characters
        if re.search(r'[\u3040-\u309f\u30a0-\u30ff]', text):
            return Language.JA
        
        # Check for Korean characters
        if re.search(r'[\uac00-\ud7af]', text):
            return Language.KO
        
        # Check for German characters (ä, ö, ü, ß)
        if re.search(r'[äöüß]', text):
            return Language.DE
        
        # Check for French characters (é, è, ê, ë, à, â, ô, î, ï, û, ù, ç)
        if re.search(r'[éèêëàâôîïûùç]', text):
            return Language.FR
        
        # Default to English
        return Language.EN
    
    def extract_action_and_target(self, text: str, lang: Language) -> Tuple[Optional[SemanticAction], Optional[str]]:
        """
        Extract semantic action and target from text.
        
        Returns:
            (action, target) tuple
        """
        patterns = self.ACTION_PATTERNS.get(lang, self.ACTION_PATTERNS[Language.EN])
        
        for action, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                target = match.group('target') if 'target' in match.groupdict() else None
                return action, target
        
        # Try to extract target from common targets
        for target in self.COMMON_TARGETS:
            if target.lower() in text.lower():
                return None, target
        
        return None, None
    
    def extract_result(self, text: str, lang: Language) -> Optional[SemanticResult]:
        """
        Extract semantic result from text.
        """
        patterns = self.RESULT_PATTERNS.get(lang, self.RESULT_PATTERNS[Language.EN])
        
        for result, pattern in patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                return result
        
        return None
    
    def semanticize(self, text: str, lang: Optional[str] = None) -> SemanticTokenAST:
        """
        Convert natural language to English semantic tokens.
        
        Args:
            text: Input text in any supported language
            lang: Source language code (zh, en, ja, ko, de, fr)
                 If None, auto-detect from text
        
        Returns:
            SemanticTokenAST: Abstract syntax tree of semantic tokens
        """
        # Detect language if not provided
        if lang is None:
            detected_lang = self.detect_language(text)
            lang_code = detected_lang.value
        else:
            lang_code = lang
            detected_lang = Language(lang)
        
        # Extract action and target
        action, target = self.extract_action_and_target(text, detected_lang)
        
        # Extract result
        result = self.extract_result(text, detected_lang)
        
        # Build semantic token AST
        ast = SemanticTokenAST(
            action=action.value if action else "unknown_action",
            target=target,
            timestamp=datetime.utcnow().isoformat() + "Z",
            actor=self.DEFAULT_ACTOR,
            result=result.value if result else "unknown_result",
            metadata={
                "original_lang": lang_code,
                "original_text": text,
                "detected_lang": detected_lang.value,
            }
        )
        
        return ast
    
    def create_language_map(self, semantic_ast: SemanticTokenAST, 
                           translations: Dict[str, str]) -> Dict:
        """
        Create language map for cross-language sealing.
        
        Args:
            semantic_ast: The semantic token AST
            translations: Dictionary of language_code -> text
        
        Returns:
            Language map dictionary
        """
        return {
            "semantic-tokens": semantic_ast.to_dict(),
            "languages": {
                lang_code: {
                    "text": text,
                    "canonical_text": text  # Could be normalized
                }
                for lang_code, text in translations.items()
            }
        }


def main():
    """Command-line interface for semanticizer"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Language-Neutral Semantic Tokenization System"
    )
    parser.add_argument(
        "text",
        help="Input text to semanticize"
    )
    parser.add_argument(
        "--lang", "-l",
        choices=["zh", "en", "ja", "ko", "de", "fr"],
        help="Source language (default: auto-detect)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: stdout)"
    )
    parser.add_argument(
        "--language-map",
        help="Generate language map (JSON file with translations)"
    )
    
    args = parser.parse_args()
    
    # Create semanticizer
    semanticizer = Semanticizer()
    
    # Semanticize
    ast = semanticizer.semanticize(args.text, lang=args.lang)
    
    # Output
    output = ast.to_json()
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✅ Semantic tokens written to: {args.output}", file=sys.stderr)
    else:
        print(output)
    
    # Generate language map if requested
    if args.language_map:
        # Example translations (in practice, would use translation API)
        translations = {
            "zh": args.text,
            "en": "We restarted nginx",  # Placeholder
            "ja": "nginx を再起動しました",  # Placeholder
        }
        
        lang_map = semanticizer.create_language_map(ast, translations)
        
        with open(args.language_map, 'w', encoding='utf-8') as f:
            json.dump(lang_map, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Language map written to: {args.language_map}", file=sys.stderr)


if __name__ == "__main__":
    main()