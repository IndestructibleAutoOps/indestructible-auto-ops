#!/usr/bin/env python3
"""
MNGA Network and External Service Validator
內網+外網交互驗證系統
"""

# MNGA-002: Import organization needs review
import socket
import urllib.request
import urllib.error
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import subprocess
import time


@dataclass
class NetworkTestResult:
    """網絡測試結果"""
    test_name: str
    status: str  # PASS, FAIL, WARNING
    latency_ms: float
    details: str
    timestamp: str
    test_type: str  # INTERNAL, EXTERNAL, HYBRID


class NetworkValidator:
    """網絡驗證器 - 驗證內網和外網連接性"""
    
    def __init__(self):
        self.results: List[NetworkTestResult] = []
    
    def test_internal_connectivity(self) -> NetworkTestResult:
        """測試內網連接性"""
        test_name = "Internal Connectivity Test"
        start_time = time.time()
        
        try:
            # 測試本地服務端口
            test_ports = [22, 80, 443, 3000, 8080]
            reachable_ports = []
            
            for port in test_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('127.0.0.1', port))
                if result == 0:
                    reachable_ports.append(port)
                sock.close()
            
            latency = (time.time() - start_time) * 1000
            
            if reachable_ports:
                return NetworkTestResult(
                    test_name=test_name,
                    status="PASS",
                    latency_ms=latency,
                    details=f"Reachable ports: {reachable_ports}",
                    timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    test_type="INTERNAL"
                )
            else:
                return NetworkTestResult(
                    test_name=test_name,
                    status="WARNING",
                    latency_ms=latency,
                    details="No standard ports reachable",
                    timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    test_type="INTERNAL"
                )
        except Exception as e:
            return NetworkTestResult(
                test_name=test_name,
                status="FAIL",
                latency_ms=0,
                details=f"Internal connectivity test failed: {str(e)}",
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                test_type="INTERNAL"
            )
    
    def test_dns_resolution(self) -> NetworkTestResult:
        """測試 DNS 解析"""
        test_name = "DNS Resolution Test"
        start_time = time.time()
        
        test_domains = [
            ("github.com", "EXTERNAL"),
            ("localhost", "INTERNAL"),
            ("example.com", "EXTERNAL")
        ]
        
        results = []
        for domain, domain_type in test_domains:
            try:
                socket.gethostbyname(domain)
                results.append(f"{domain} ({domain_type}): OK")
            except socket.gaierror:
                results.append(f"{domain} ({domain_type}): FAIL")
        
        latency = (time.time() - start_time) * 1000
        
        all_passed = all("OK" in r for r in results)
        
        return NetworkTestResult(
            test_name=test_name,
            status="PASS" if all_passed else "WARNING",
            latency_ms=latency,
            details=f"DNS results: {', '.join(results)}",
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            test_type="HYBRID"
        )
    
    def test_http_connectivity(self, url: str, test_type: str = "EXTERNAL") -> NetworkTestResult:
        """測試 HTTP 連接性"""
        test_name = f"HTTP Connectivity Test ({test_type})"
        start_time = time.time()
        
        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'MNGA-Network-Validator/1.0'
                },
                method='HEAD'
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                latency = (time.time() - start_time) * 1000
                
                return NetworkTestResult(
                    test_name=test_name,
                    status="PASS",
                    latency_ms=latency,
                    details=f"Status: {response.status}, Content-Type: {response.headers.get('Content-Type', 'N/A')}",
                    timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    test_type=test_type
                )
        except urllib.error.HTTPError as e:
            latency = (time.time() - start_time) * 1000
            return NetworkTestResult(
                test_name=test_name,
                status="FAIL",
                latency_ms=latency,
                details=f"HTTP Error: {e.code} {e.reason}",
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                test_type=test_type
            )
        except urllib.error.URLError as e:
            latency = (time.time() - start_time) * 1000
            return NetworkTestResult(
                test_name=test_name,
                status="FAIL",
                latency_ms=latency,
                details=f"URL Error: {str(e.reason)}",
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                test_type=test_type
            )
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return NetworkTestResult(
                test_name=test_name,
                status="FAIL",
                latency_ms=latency,
                details=f"Unexpected error: {str(e)}",
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                test_type=test_type
            )
    
    def test_github_api(self, token: Optional[str] = None) -> NetworkTestResult:
        """測試 GitHub API 連接性"""
        test_name = "GitHub API Test"
        start_time = time.time()
        
        try:
            url = "https://api.github.com/repos/MachineNativeOps/machine-native-ops"
            headers = {
                'User-Agent': 'MNGA-Network-Validator/1.0',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            if token:
                headers['Authorization'] = f'token {token}'
            
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                latency = (time.time() - start_time) * 1000
                
                return NetworkTestResult(
                    test_name=test_name,
                    status="PASS",
                    latency_ms=latency,
                    details=f"Repository: {data.get('name', 'N/A')}, Stars: {data.get('stargazers_count', 0)}, Forks: {data.get('forks_count', 0)}",
                    timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    test_type="EXTERNAL"
                )
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return NetworkTestResult(
                test_name=test_name,
                status="FAIL",
                latency_ms=latency,
                details=f"GitHub API test failed: {str(e)}",
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                test_type="EXTERNAL"
            )
    
    def run_all_tests(self) -> List[NetworkTestResult]:
        """運行所有網絡測試"""
        results = []
        
        # 內網測試
        results.append(self.test_internal_connectivity())
        
        # DNS 測試
        results.append(self.test_dns_resolution())
        
        # 外網 HTTP 測試
        results.append(self.test_http_connectivity("https://www.google.com", "EXTERNAL"))
        
        # GitHub API 測試
        results.append(self.test_github_api())
        
        self.results = results
        return results
    
    def generate_report(self) -> Dict:
        """生成測試報告"""
        passed = sum(1 for r in self.results if r.status == "PASS")
        total = len(self.results)
        
        avg_latency = sum(r.latency_ms for r in self.results if r.latency_ms > 0) / total
        
        return {
            "test_summary": {
                "total_tests": total,
                "passed": passed,
                "failed": total - passed,
                "success_rate": f"{(passed/total)*100:.1f}%",
                "average_latency_ms": f"{avg_latency:.2f}"
            },
            "tests": [
                {
                    "name": r.test_name,
                    "status": r.status,
                    "latency_ms": r.latency_ms,
                    "details": r.details,
                    "timestamp": r.timestamp,
                    "test_type": r.test_type
                }
                for r in self.results
            ],
            "recommendations": self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """生成建議"""
        recommendations = []
        
        # 檢查外網連接
        external_tests = [r for r in self.results if r.test_type == "EXTERNAL"]
        if all(r.status == "PASS" for r in external_tests):
            recommendations.append("✅ 外網連接正常，可以進行 GitHub 操作和外部 API 調用")
        else:
            recommendations.append("⚠️ 外網連接存在問題，請檢查網絡配置和防火牆設置")
        
        # 檢查延遲
        avg_latency = sum(r.latency_ms for r in self.results if r.latency_ms > 0) / len(self.results)
        if avg_latency > 1000:
            recommendations.append(f"⚠️ 平均延遲較高 ({avg_latency:.2f}ms)，可能影響性能")
        else:
            recommendations.append(f"✅ 網絡延遲正常 ({avg_latency:.2f}ms)")
        
        return recommendations


if __name__ == "__main__":
    validator = NetworkValidator()
    results = validator.run_all_tests()
    
    print(json.dumps(validator.generate_report(), indent=2, ensure_ascii=False))