"""CacheFlow Agent 4: Cache Monitor & Optimizer."""
from .base import BaseAgent


class CacheMonitorAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config, "CacheMonitor")

    async def generate_monitoring(self, strategy: dict, implementations: dict) -> dict:
        system_prompt = """You are a cache monitoring expert. Design monitoring and optimization plans.

Output JSON format:
{
    "metrics": [
        {
            "name": "metric_name",
            "description": "what it measures",
            "alert_threshold": "value",
            "dashboard_panel": "panel config"
        }
    ],
    "alerts": [
        {
            "condition": "trigger condition",
            "severity": "critical/warning/info",
            "action": "response action"
        }
    ],
    "optimization_plan": [
        {
            "phase": "phase name",
            "actions": ["action 1", "action 2"],
            "expected_impact": "impact description"
        }
    ],
    "runbook": {
        "cache_miss_spike": "response steps",
        "memory_pressure": "response steps",
        "stale_data_incident": "response steps"
    }
}"""

        user_prompt = f"""Design cache monitoring and optimization for:

Strategy: {strategy}
Implementations: {implementations}

Create a comprehensive monitoring plan."""

        return await self.call_llm(system_prompt, user_prompt)
