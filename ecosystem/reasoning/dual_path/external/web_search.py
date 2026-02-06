#!/usr/bin/env python3
"""
Web 搜尋集成
Web Search Integration

@GL-governed
@GL-layer: GL30-39
@GL-semantic: reasoning-external-search

用於集成外部 Web 搜尋服務：
- 搜尋引擎 API 集成
- 結果解析和過濾
- 緩存管理
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from urllib.parse import quote_plus


@dataclass
class SearchResult:
    """搜尋結果"""

    title: str
    url: str
    snippet: str
    source: str  # google, bing, duckduckgo, etc.
    relevance_score: float = 0.0
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchQuery:
    """搜尋查詢"""

    query: str
    filters: Dict[str, Any] = field(default_factory=dict)
    max_results: int = 10
    sources: List[str] = field(default_factory=lambda: ["all"])


class WebSearchClient:
    """
    Web 搜尋客戶端

    支持多個搜尋引擎：
    - Google Custom Search API
    - Bing Search API
    - DuckDuckGo (無需 API)
    - GitHub Code Search
    - Stack Overflow
    """

    def __init__(self, cache_dir: Optional[str] = None):
        self.cache_dir = (
            Path(cache_dir) if cache_dir else Path("ecosystem/indexes/external/cache")
        )
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # API 配置（從環境變量讀取）
        self.google_api_key = os.environ.get("GOOGLE_API_KEY")
        self.google_cx = os.environ.get("GOOGLE_CX")
        self.bing_api_key = os.environ.get("BING_API_KEY")
        self.github_token = os.environ.get("GITHUB_TOKEN")

        # 緩存設置
        self.cache_ttl_hours = 24

    def _get_cache_key(self, query: SearchQuery) -> str:
        """生成緩存鍵"""
        cache_input = f"{query.query}:{json.dumps(query.filters, sort_keys=True)}"
        return hashlib.sha256(cache_input.encode()).hexdigest()[:32]

    def _get_cached_results(self, cache_key: str) -> Optional[List[SearchResult]]:
        """獲取緩存結果"""
        cache_file = self.cache_dir / f"{cache_key}.json"

        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # 檢查緩存是否過期
                cached_time = datetime.fromisoformat(
                    data.get("timestamp", "2000-01-01T00:00:00+00:00")
                )
                now = datetime.now(timezone.utc)

                if (now - cached_time).total_seconds() < self.cache_ttl_hours * 3600:
                    return [SearchResult(**r) for r in data.get("results", [])]
            except Exception:
                pass

        return None

    def _save_to_cache(self, cache_key: str, results: List[SearchResult]):
        """保存到緩存"""
        cache_file = self.cache_dir / f"{cache_key}.json"

        data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "results": [asdict(r) for r in results],
        }

        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def search(self, query: SearchQuery) -> List[SearchResult]:
        """執行搜尋"""
        cache_key = self._get_cache_key(query)

        # 檢查緩存
        cached = self._get_cached_results(cache_key)
        if cached:
            return cached[: query.max_results]

        results = []

        # 根據指定的源執行搜尋
        sources = (
            query.sources
            if "all" not in query.sources
            else ["duckduckgo", "github", "stackoverflow"]
        )

        for source in sources:
            if source == "google" and self.google_api_key:
                results.extend(self._search_google(query))
            elif source == "bing" and self.bing_api_key:
                results.extend(self._search_bing(query))
            elif source == "duckduckgo":
                results.extend(self._search_duckduckgo(query))
            elif source == "github":
                results.extend(self._search_github(query))
            elif source == "stackoverflow":
                results.extend(self._search_stackoverflow(query))

        # 按相關性排序
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        results = results[: query.max_results]

        # 保存到緩存
        if results:
            self._save_to_cache(cache_key, results)

        return results

    def _search_google(self, query: SearchQuery) -> List[SearchResult]:
        """Google Custom Search"""
        results = []

        try:
            import urllib.request

            url = f"https://www.googleapis.com/customsearch/v1?key={self.google_api_key}&cx={self.google_cx}&q={quote_plus(query.query)}"

            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())

            for item in data.get("items", [])[: query.max_results]:
                results.append(
                    SearchResult(
                        title=item.get("title", ""),
                        url=item.get("link", ""),
                        snippet=item.get("snippet", ""),
                        source="google",
                        relevance_score=0.9,
                        metadata={"displayLink": item.get("displayLink", "")},
                    )
                )
        except Exception as e:
            pass

        return results

    def _search_bing(self, query: SearchQuery) -> List[SearchResult]:
        """Bing Search"""
        results = []

        try:
            import urllib.request

            url = f"https://api.bing.microsoft.com/v7.0/search?q={quote_plus(query.query)}"

            req = urllib.request.Request(url)
            req.add_header("Ocp-Apim-Subscription-Key", self.bing_api_key)

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())

            for item in data.get("webPages", {}).get("value", [])[: query.max_results]:
                results.append(
                    SearchResult(
                        title=item.get("name", ""),
                        url=item.get("url", ""),
                        snippet=item.get("snippet", ""),
                        source="bing",
                        relevance_score=0.85,
                    )
                )
        except Exception as e:
            pass

        return results

    def _search_duckduckgo(self, query: SearchQuery) -> List[SearchResult]:
        """DuckDuckGo Instant Answer API"""
        results = []

        try:
            import urllib.request

            url = f"https://api.duckduckgo.com/?q={quote_plus(query.query)}&format=json"

            req = urllib.request.Request(url)
            req.add_header("User-Agent", "MNGA-WebSearch/1.0")

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())

            # Abstract
            if data.get("Abstract"):
                results.append(
                    SearchResult(
                        title=data.get("Heading", query.query),
                        url=data.get("AbstractURL", ""),
                        snippet=data.get("Abstract", ""),
                        source="duckduckgo",
                        relevance_score=0.8,
                    )
                )

            # Related Topics
            for topic in data.get("RelatedTopics", [])[: query.max_results - 1]:
                if isinstance(topic, dict) and topic.get("Text"):
                    results.append(
                        SearchResult(
                            title=topic.get("Text", "")[:100],
                            url=topic.get("FirstURL", ""),
                            snippet=topic.get("Text", ""),
                            source="duckduckgo",
                            relevance_score=0.7,
                        )
                    )
        except Exception as e:
            pass

        return results

    def _search_github(self, query: SearchQuery) -> List[SearchResult]:
        """GitHub Code Search"""
        results = []

        try:
            import urllib.request

            url = f"https://api.github.com/search/code?q={quote_plus(query.query)}"

            req = urllib.request.Request(url)
            req.add_header("Accept", "application/vnd.github.v3+json")
            req.add_header("User-Agent", "MNGA-WebSearch/1.0")

            if self.github_token:
                req.add_header("Authorization", f"token {self.github_token}")

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())

            for item in data.get("items", [])[: query.max_results]:
                results.append(
                    SearchResult(
                        title=f"{item.get('repository', {}).get('full_name', '')}/{item.get('name', '')}",
                        url=item.get("html_url", ""),
                        snippet=item.get("path", ""),
                        source="github",
                        relevance_score=item.get("score", 0.5),
                        metadata={
                            "repository": item.get("repository", {}).get(
                                "full_name", ""
                            ),
                            "language": item.get("repository", {}).get("language", ""),
                        },
                    )
                )
        except Exception as e:
            pass

        return results

    def _search_stackoverflow(self, query: SearchQuery) -> List[SearchResult]:
        """Stack Overflow Search"""
        results = []

        try:
            import urllib.request

            url = f"https://api.stackexchange.com/2.3/search?order=desc&sort=relevance&intitle={quote_plus(query.query)}&site=stackoverflow"

            req = urllib.request.Request(url)
            req.add_header("Accept-Encoding", "identity")

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())

            for item in data.get("items", [])[: query.max_results]:
                results.append(
                    SearchResult(
                        title=item.get("title", ""),
                        url=item.get("link", ""),
                        snippet=f"Score: {item.get('score', 0)}, Answers: {item.get('answer_count', 0)}",
                        source="stackoverflow",
                        relevance_score=min(item.get("score", 0) / 100, 1.0),
                        metadata={
                            "tags": item.get("tags", []),
                            "is_answered": item.get("is_answered", False),
                        },
                    )
                )
        except Exception as e:
            pass

        return results

    def search_code(
        self, query: str, language: Optional[str] = None
    ) -> List[SearchResult]:
        """專門搜索代碼"""
        search_query = SearchQuery(
            query=f"{query} language:{language}" if language else query,
            sources=["github"],
            max_results=10,
        )
        return self.search(search_query)

    def search_docs(self, query: str, site: Optional[str] = None) -> List[SearchResult]:
        """專門搜索文檔"""
        q = f"site:{site} {query}" if site else query
        search_query = SearchQuery(
            query=q, sources=["duckduckgo", "stackoverflow"], max_results=10
        )
        return self.search(search_query)


def main():
    """主函數"""
    import argparse

    parser = argparse.ArgumentParser(description="Web Search - Web 搜尋集成")
    parser.add_argument("query", nargs="?", help="搜尋查詢")
    parser.add_argument(
        "--source",
        choices=["google", "bing", "duckduckgo", "github", "stackoverflow", "all"],
        default="all",
        help="搜尋源",
    )
    parser.add_argument("--max", type=int, default=5, help="最大結果數")
    parser.add_argument("--code", action="store_true", help="搜索代碼")
    parser.add_argument("--docs", action="store_true", help="搜索文檔")

    args = parser.parse_args()

    if not args.query:
        print("請提供搜尋查詢")
        return

    client = WebSearchClient()

    if args.code:
        results = client.search_code(args.query)
    elif args.docs:
        results = client.search_docs(args.query)
    else:
        query = SearchQuery(
            query=args.query,
            sources=[args.source] if args.source != "all" else ["all"],
            max_results=args.max,
        )
        results = client.search(query)

    print(f"找到 {len(results)} 個結果:\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r.source}] {r.title}")
        print(f"   URL: {r.url}")
        print(f"   {r.snippet[:150]}...")
        print()


if __name__ == "__main__":
    main()
