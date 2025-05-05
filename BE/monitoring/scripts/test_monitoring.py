import unittest
import requests
import time
import json
from datetime import datetime, timedelta

class MonitoringSystemTest(unittest.TestCase):
    def setUp(self):
        """设置测试环境"""
        self.prometheus_url = "http://localhost:9090"
        self.grafana_url = "http://localhost:3000"
        self.grafana_auth = ("admin", "admin")

    def test_prometheus_health(self):
        """测试Prometheus健康状态"""
        response = requests.get(f"{self.prometheus_url}/-/healthy")
        self.assertEqual(response.status_code, 200)

    def test_grafana_health(self):
        """测试Grafana健康状态"""
        response = requests.get(f"{self.grafana_url}/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("database", response.json())

    def test_prometheus_targets(self):
        """测试Prometheus目标状态"""
        response = requests.get(f"{self.prometheus_url}/api/v1/targets")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("data", data)
        
        # 检查所有目标是否都是up状态
        active_targets = data["data"]["activeTargets"]
        for target in active_targets:
            self.assertEqual(target["health"], "up", 
                           f"Target {target['labels']['instance']} is down")

    def test_grafana_datasources(self):
        """测试Grafana数据源配置"""
        response = requests.get(
            f"{self.grafana_url}/api/datasources",
            auth=self.grafana_auth
        )
        self.assertEqual(response.status_code, 200)
        datasources = response.json()
        
        # 检查是否存在Prometheus数据源
        prometheus_found = False
        for ds in datasources:
            if ds["type"] == "prometheus":
                prometheus_found = True
                self.assertTrue(ds["isDefault"])
                break
        self.assertTrue(prometheus_found, "Prometheus datasource not found")

    def test_basic_metrics(self):
        """测试基本指标是否存在"""
        metrics_to_check = [
            "http_requests_total",
            "http_request_duration_seconds",
            "process_cpu_seconds_total",
            "process_resident_memory_bytes"
        ]
        
        for metric in metrics_to_check:
            response = requests.get(
                f"{self.prometheus_url}/api/v1/query",
                params={"query": metric}
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("data", data)
            self.assertIn("result", data["data"])

    def test_alert_rules(self):
        """测试告警规则配置"""
        response = requests.get(f"{self.prometheus_url}/api/v1/rules")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("data", data)
        
        # 检查是否存在告警规则
        rules = data["data"]["groups"]
        self.assertTrue(len(rules) > 0, "No alert rules found")

    def test_metric_data_ingestion(self):
        """测试指标数据摄入"""
        # 获取5分钟前的时间戳
        five_mins_ago = int((datetime.now() - timedelta(minutes=5)).timestamp())
        
        # 检查是否有新数据摄入
        query = 'count_over_time(http_requests_total[5m])'
        response = requests.get(
            f"{self.prometheus_url}/api/v1/query",
            params={
                "query": query,
                "time": five_mins_ago
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data["data"]["result"]) > 0, 
                       "No metric data ingestion in last 5 minutes")

    def test_grafana_dashboard(self):
        """测试Grafana仪表板配置"""
        response = requests.get(
            f"{self.grafana_url}/api/dashboards/home",
            auth=self.grafana_auth
        )
        self.assertEqual(response.status_code, 200)
        
        # 检查默认仪表板
        response = requests.get(
            f"{self.grafana_url}/api/dashboards/uid/coffee_shop_backend",
            auth=self.grafana_auth
        )
        self.assertEqual(response.status_code, 200)
        dashboard = response.json()
        self.assertIn("dashboard", dashboard)

if __name__ == '__main__':
    unittest.main(verbosity=2)