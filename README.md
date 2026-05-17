# CacheFlow

多 Agent 协作缓存策略优化流水线，基于 Claude Code 开发、DeepSeek API 驱动。

## 核心架构

4 个 Agent 角色分工明确，形成完整优化闭环：

| Agent | 职责 | 输入 | 输出 |
|-------|------|------|------|
| CachePatternAnalyzer | 缓存模式分析 | 代码库 | 缓存机会分析 |
| CacheStrategist | 缓存策略设计 | 分析报告 | 优化策略方案 |
| CacheCodeGenerator | 实现代码生成 | 策略方案 | 生产级缓存代码 |
| CacheMonitor | 监控方案设计 | 策略 + 代码 | 监控告警方案 |

## 快速开始

```bash
pip install -r requirements.txt
copy .env.example .env
python -m src.main analyze ./demo/sample_project.py -o cacheflow_report.json
```

## 技术栈

- Python 3.10+ / Click / Rich / httpx / DeepSeek API

## 单次运行消耗

约 200-400 万 Token
