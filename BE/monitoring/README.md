# Coffee Shop Backend 监控系统

本监控系统使用Prometheus和Grafana来监控Coffee Shop后端服务的各项指标。

## 功能特点

1. 系统指标监控：
   - CPU使用率
   - 内存使用情况
   - 请求延迟统计
   - 错误率统计

2. 业务指标监控：
   - 商品访问统计
   - 活跃用户数量
   - 订单处理情况
   - 缓存命中率

3. 基础设施监控：
   - 数据库连接池状态
   - Redis连接状态
   - API响应时间
   - 系统资源使用情况

## 安装要求

- Docker
- Docker Compose
- Python 3.10+
- FastAPI应用依赖

## 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 启动监控服务：
```bash
cd monitoring
docker-compose up -d
```

3. 访问监控界面：
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000
     - 默认用户名：admin
     - 默认密码：admin

4. 导入Grafana仪表板：
   - 登录Grafana
   - 导航到 Dashboards > Import
   - 上传 grafana_dashboard.json 文件

## 监控指标说明

### HTTP请求指标
- `http_requests_total`: 总请求数
- `http_request_duration_seconds`: 请求处理时间

### 数据库指标
- `db_connections_in_use`: 当前使用的连接数
- `db_connections_total`: 连接池总连接数

### Redis指标
- `redis_connection_status`: Redis连接状态
- `redis_operations_total`: Redis操作计数

### 系统资源指标
- `memory_usage_bytes`: 内存使用量
- `cpu_usage_percent`: CPU使用率

### 业务指标
- `product_views_total`: 商品查看次数
- `active_users`: 活跃用户数
- `order_total`: 订单统计

## 告警规则

### 高延迟告警
- 触发条件：95%的请求处理时间超过2秒
- 严重程度：warning
- 持续时间：5分钟

### 高错误率告警
- 触发条件：5分钟内错误率超过10%
- 严重程度：critical
- 持续时间：5分钟

### 数据库连接告警
- 触发条件：连接池使用率超过90%
- 严重程度：warning
- 持续时间：5分钟

### Redis连接告警
- 触发条件：Redis连接断开
- 严重程度：critical
- 持续时间：1分钟

### 资源使用告警
- 内存使用：超过1GB
- CPU使用：超过80%
- 持续时间：5分钟

## 维护说明

1. 日志轮转：
   - Prometheus数据默认保留15天
   - 可通过prometheus.yml配置调整

2. 备份：
   - Grafana配置位于grafana-storage卷
   - 建议定期备份此卷

3. 扩展监控：
   - 在monitoring.py中添加新的指标
   - 更新Prometheus配置
   - 添加新的Grafana面板

4. 故障排除：
   - 检查服务状态：`docker-compose ps`
   - 查看日志：`docker-compose logs`
   - 重启服务：`docker-compose restart`

## 最佳实践

1. 监控指标：
   - 保持指标名称一致性
   - 添加适当的标签
   - 避免过多的基数

2. 告警配置：
   - 设置合理的阈值
   - 避免告警风暴
   - 定期review告警规则

3. 仪表板设计：
   - 关注关键指标
   - 使用适当的可视化
   - 保持简洁清晰

4. 性能优化：
   - 监控指标采集频率
   - 合理设置保留期
   - 优化查询性能