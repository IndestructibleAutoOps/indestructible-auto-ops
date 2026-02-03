# monitoring/metrics_dashboard.py - Prometheus + Grafana集成
from prometheus_client import start_http_server, Gauge
import requests

GOVERNANCE_COMPLIANCE = Gauge('governance_compliance_score', 
                             '当前系统治理规范合规指数',
                             ['component', 'version'])

def fetch_compliance_data():
    # 从各验证器收集数据
    validators = ['math-validator', 'code-validator', 'security-validator']
    for v in validators:
        res = requests.get(f'http://{v}/metrics/compliance')
        score = res.json()['compliance_score']
        GOVERNANCE_COMPLIANCE.set(score, labels={
            'component': v,
            'version': res.json()['version']
        })

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        fetch_compliance_data()
        time.sleep(60)
