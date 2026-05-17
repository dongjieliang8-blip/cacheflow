"""CacheFlow Agent 2: Cache Strategy Designer."""
from .base import BaseAgent


class CacheStrategistAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config, "CacheStrategist")

    async def design_strategy(self, analysis_report: dict, requirements: str = "") -> dict:
        system_prompt = """You are a caching strategy architect. Design optimal caching strategies based on analysis.

Output JSON format:
{
    "strategies": [
        {
            "target": "endpoint/layer",
            "cache_type": "redis/memcached/in-memory/cdn/write-through/write-behind",
            "ttl_seconds": N,
            "invalidation_strategy": "time-based/event-based/hybrid",
            "key_pattern": "cache key format",
            "estimated_improvement": "latency reduction %",
            "complexity": "low/medium/high"
        }
    ],
    "architecture": {
        "layers": ["description of cache layers"],
        "fallback_strategy": "what happens on cache miss",
        "consistency_model": "eventual/strong"
    },
    "estimated_total_improvement": {
        "latency_reduction": "X%",
        "throughput_increase": "X%",
        "cost_savings": "$X/month"
    }
}"""

        user_prompt = f"""Design caching strategies based on:

Analysis Report: {analysis_report}

Additional Requirements: {requirements}

Create an optimal caching architecture."""

        return await self.call_llm(system_prompt, user_prompt)
