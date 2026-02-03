#!/usr/bin/env python3
"""
域名過濾器
Domain Filter

@GL-governed
@GL-layer: GL30-39
@GL-semantic: reasoning-external-filter

用於過濾和驗證外部搜尋結果：
- 域名白名單/黑名單
- 內容安全過濾
- 可信度評估
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from urllib.parse import urlparse
from datetime import datetime, timezone


@dataclass
class FilterResult:
    """過濾結果"""
    url: str
    allowed: bool
    reason: str
    trust_score: float  # 0.0 - 1.0
    category: str  # trusted, neutral, untrusted, blocked


@dataclass
class DomainRule:
    """域名規則"""
    pattern: str
    action: str  # allow, block, warn
    category: str
    trust_score: float
    description: str = ""


class DomainFilter:
    """
    域名過濾器
    
    功能：
    1. 域名白名單/黑名單管理
    2. URL 安全檢查
    3. 內容可信度評估
    4. 自動學習和更新規則
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else None
        
        # 預設的可信域名（技術文檔和官方源）
        self.trusted_domains: Dict[str, float] = {
            # 官方文檔
            "docs.python.org": 1.0,
            "docs.microsoft.com": 1.0,
            "developer.mozilla.org": 1.0,
            "kubernetes.io": 1.0,
            "docs.docker.com": 1.0,
            "docs.github.com": 1.0,
            "cloud.google.com": 1.0,
            "aws.amazon.com": 1.0,
            "docs.aws.amazon.com": 1.0,
            "azure.microsoft.com": 1.0,
            "golang.org": 1.0,
            "rust-lang.org": 1.0,
            "nodejs.org": 1.0,
            "reactjs.org": 1.0,
            "vuejs.org": 1.0,
            "angular.io": 1.0,
            
            # 技術社區
            "stackoverflow.com": 0.9,
            "github.com": 0.9,
            "gitlab.com": 0.85,
            "bitbucket.org": 0.85,
            "dev.to": 0.8,
            "medium.com": 0.7,
            "hashnode.dev": 0.75,
            
            # 技術博客和教程
            "realpython.com": 0.85,
            "digitalocean.com": 0.85,
            "freecodecamp.org": 0.8,
            "geeksforgeeks.org": 0.75,
            "tutorialspoint.com": 0.7,
            "w3schools.com": 0.7,
            
            # 學術和研究
            "arxiv.org": 0.95,
            "acm.org": 0.95,
            "ieee.org": 0.95,
            "scholar.google.com": 0.9,
            
            # 安全相關
            "owasp.org": 0.95,
            "cve.mitre.org": 0.95,
            "nvd.nist.gov": 0.95,
        }
        
        # 黑名單域名
        self.blocked_domains: Set[str] = {
            # 已知的惡意或低質量域名
            "example-malware.com",
            "spam-site.net",
        }
        
        # 可疑模式
        self.suspicious_patterns: List[str] = [
            r"free.*download",
            r"crack.*software",
            r"keygen",
            r"warez",
            r"torrent",
            r"pirat",
        ]
        
        # 域名規則
        self.rules: List[DomainRule] = self._load_default_rules()
    
    def _load_default_rules(self) -> List[DomainRule]:
        """載入預設規則"""
        return [
            DomainRule(
                pattern=r".*\.gov$",
                action="allow",
                category="government",
                trust_score=0.95,
                description="政府網站"
            ),
            DomainRule(
                pattern=r".*\.edu$",
                action="allow",
                category="education",
                trust_score=0.9,
                description="教育機構"
            ),
            DomainRule(
                pattern=r".*\.org$",
                action="allow",
                category="organization",
                trust_score=0.8,
                description="非營利組織"
            ),
            DomainRule(
                pattern=r".*\.io$",
                action="allow",
                category="tech",
                trust_score=0.7,
                description="技術網站"
            ),
            DomainRule(
                pattern=r".*\.(xyz|tk|ml|ga|cf)$",
                action="warn",
                category="suspicious_tld",
                trust_score=0.3,
                description="可疑頂級域名"
            ),
        ]
    
    def _extract_domain(self, url: str) -> str:
        """提取域名"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            # 移除 www. 前綴
            if domain.startswith("www."):
                domain = domain[4:]
            return domain
        except Exception:
            return ""
    
    def _check_suspicious_content(self, url: str, title: str = "", snippet: str = "") -> bool:
        """檢查可疑內容"""
        content = f"{url} {title} {snippet}".lower()
        
        for pattern in self.suspicious_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def _get_trust_score(self, domain: str) -> float:
        """獲取域名信任分數"""
        # 直接匹配
        if domain in self.trusted_domains:
            return self.trusted_domains[domain]
        
        # 子域名匹配
        parts = domain.split(".")
        for i in range(len(parts)):
            parent = ".".join(parts[i:])
            if parent in self.trusted_domains:
                # 子域名略低於父域名
                return self.trusted_domains[parent] * 0.95
        
        # 規則匹配
        for rule in self.rules:
            if re.match(rule.pattern, domain):
                return rule.trust_score
        
        # 默認分數
        return 0.5
    
    def filter_url(self, url: str, title: str = "", snippet: str = "") -> FilterResult:
        """過濾單個 URL"""
        domain = self._extract_domain(url)
        
        if not domain:
            return FilterResult(
                url=url,
                allowed=False,
                reason="無效的 URL",
                trust_score=0.0,
                category="invalid"
            )
        
        # 檢查黑名單
        if domain in self.blocked_domains:
            return FilterResult(
                url=url,
                allowed=False,
                reason="域名在黑名單中",
                trust_score=0.0,
                category="blocked"
            )
        
        # 檢查可疑內容
        if self._check_suspicious_content(url, title, snippet):
            return FilterResult(
                url=url,
                allowed=False,
                reason="內容包含可疑模式",
                trust_score=0.1,
                category="suspicious"
            )
        
        # 獲取信任分數
        trust_score = self._get_trust_score(domain)
        
        # 確定類別
        if trust_score >= 0.8:
            category = "trusted"
        elif trust_score >= 0.5:
            category = "neutral"
        else:
            category = "untrusted"
        
        return FilterResult(
            url=url,
            allowed=trust_score >= 0.3,
            reason="通過過濾" if trust_score >= 0.3 else "信任分數過低",
            trust_score=trust_score,
            category=category
        )
    
    def filter_results(self, results: List[Dict[str, Any]], 
                       min_trust_score: float = 0.3) -> List[Dict[str, Any]]:
        """過濾搜尋結果列表"""
        filtered = []
        
        for result in results:
            url = result.get("url", "")
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            
            filter_result = self.filter_url(url, title, snippet)
            
            if filter_result.allowed and filter_result.trust_score >= min_trust_score:
                result["_filter"] = {
                    "trust_score": filter_result.trust_score,
                    "category": filter_result.category
                }
                filtered.append(result)
        
        # 按信任分數排序
        filtered.sort(key=lambda x: x.get("_filter", {}).get("trust_score", 0), reverse=True)
        
        return filtered
    
    def add_trusted_domain(self, domain: str, trust_score: float = 0.8):
        """添加可信域名"""
        domain = domain.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        self.trusted_domains[domain] = min(max(trust_score, 0.0), 1.0)
    
    def add_blocked_domain(self, domain: str):
        """添加黑名單域名"""
        domain = domain.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        self.blocked_domains.add(domain)
    
    def get_domain_info(self, url: str) -> Dict[str, Any]:
        """獲取域名信息"""
        domain = self._extract_domain(url)
        filter_result = self.filter_url(url)
        
        return {
            "domain": domain,
            "url": url,
            "trust_score": filter_result.trust_score,
            "category": filter_result.category,
            "allowed": filter_result.allowed,
            "reason": filter_result.reason,
            "is_trusted": domain in self.trusted_domains,
            "is_blocked": domain in self.blocked_domains
        }
    
    def export_rules(self) -> Dict[str, Any]:
        """導出規則"""
        return {
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trusted_domains": self.trusted_domains,
            "blocked_domains": list(self.blocked_domains),
            "suspicious_patterns": self.suspicious_patterns,
            "rules": [
                {
                    "pattern": r.pattern,
                    "action": r.action,
                    "category": r.category,
                    "trust_score": r.trust_score,
                    "description": r.description
                }
                for r in self.rules
            ]
        }


def main():
    """主函數"""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Domain Filter - 域名過濾器")
    parser.add_argument("url", nargs="?", help="要檢查的 URL")
    parser.add_argument("--export", action="store_true", help="導出規則")
    parser.add_argument("--add-trusted", type=str, help="添加可信域名")
    parser.add_argument("--add-blocked", type=str, help="添加黑名單域名")
    
    args = parser.parse_args()
    
    filter = DomainFilter()
    
    if args.export:
        rules = filter.export_rules()
        print(json.dumps(rules, indent=2, ensure_ascii=False))
    elif args.add_trusted:
        filter.add_trusted_domain(args.add_trusted)
        print(f"已添加可信域名: {args.add_trusted}")
    elif args.add_blocked:
        filter.add_blocked_domain(args.add_blocked)
        print(f"已添加黑名單域名: {args.add_blocked}")
    elif args.url:
        info = filter.get_domain_info(args.url)
        print(f"域名: {info['domain']}")
        print(f"信任分數: {info['trust_score']:.2f}")
        print(f"類別: {info['category']}")
        print(f"允許: {'是' if info['allowed'] else '否'}")
        print(f"原因: {info['reason']}")
    else:
        print("請提供 URL 或使用 --export 導出規則")


if __name__ == "__main__":
    main()