"""CacheFlow Agent 3: Cache Implementation Generator."""
from .base import BaseAgent


class CacheCodeGeneratorAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config, "CacheCodeGenerator")

    async def generate_code(self, strategy: dict, codebase_info: str) -> dict:
        system_prompt = """You are a caching implementation expert. Generate production-ready cache code.

Output JSON format:
{
    "implementations": [
        {
            "target": "endpoint/function",
            "language": "python/go/node",
            "code": "implementation code with comments",
            "config": "cache configuration",
            "dependencies": ["required packages"]
        }
    ],
    "middleware": {
        "cache_decorator": "reusable cache decorator code",
        "invalidation_hooks": "cache invalidation code"
    },
    "tests": [
        {
            "name": "test_name",
            "code": "test code"
        }
    ]
}"""

        user_prompt = f"""Generate cache implementation code based on:

Strategy: {strategy}

Codebase Context: {codebase_info}

Generate production-ready caching code."""

        return await self.call_llm(system_prompt, user_prompt)
