"""CacheFlow Agent 1: Cache Pattern Analyzer."""
from .base import BaseAgent


class CachePatternAnalyzerAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config, "CachePatternAnalyzer")

    async def analyze(self, codebase_info: str) -> dict:
        system_prompt = """You are a caching strategy expert. Analyze the given codebase for caching opportunities.

Output JSON format:
{
    "endpoints": [{"path": "API path", "method": "GET/POST", "access_pattern": "read-heavy/write-heavy/balanced"}],
    "current_caches": [{"type": "none/redis/memcached/in-memory", "scope": "description"}],
    "cache_candidates": [{"path": "endpoint", "reason": "why it should be cached", "estimated_hit_rate": 0.0-1.0}],
    "anti_patterns": [{"issue": "description", "severity": "high/medium/low"}],
    "data_freshness_requirements": [{"path": "endpoint", "max_staleness": "duration"}]
}"""

        user_prompt = f"""Analyze this codebase for caching opportunities:

{codebase_info}

Provide a detailed cache pattern analysis."""

        return await self.call_llm(system_prompt, user_prompt)
