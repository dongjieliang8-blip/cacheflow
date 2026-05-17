"""CacheFlow - Multi-agent caching strategy optimization pipeline."""
import asyncio
import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import Config
from .agents.analyzer import CachePatternAnalyzerAgent
from .agents.strategist import CacheStrategistAgent
from .agents.codegen import CacheCodeGeneratorAgent
from .agents.monitor import CacheMonitorAgent

console = Console()


class CacheFlowPipeline:
    def __init__(self, config: Config):
        self.config = config
        self.analyzer = CachePatternAnalyzerAgent(config)
        self.strategist = CacheStrategistAgent(config)
        self.codegen = CacheCodeGeneratorAgent(config)
        self.monitor = CacheMonitorAgent(config)

    async def run(self, target_path: str, requirements: str = "", output: str = "cacheflow_report.json"):
        console.print(Panel("[bold cyan]CacheFlow Pipeline[/bold cyan]", title="Caching Strategy Optimization"))

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Reading project...", total=None)

            # Collect codebase info
            target = Path(target_path)
            if target.is_file():
                codebase_info = target.read_text(encoding="utf-8")
            else:
                files = []
                for f in target.rglob("*"):
                    if f.is_file() and f.suffix in (".py", ".js", ".ts", ".go", ".java", ".yaml", ".yml", ".json"):
                        try:
                            files.append(f"--- {f.relative_to(target)} ---\n{f.read_text(encoding='utf-8')[:2000]}")
                        except Exception:
                            pass
                codebase_info = "\n\n".join(files[:20])

            # Agent 1: Analyze
            progress.update(task, description="[cyan]Agent 1/4: Analyzing cache patterns...[/cyan]")
            analysis = await self.analyzer.analyze(codebase_info)
            progress.update(task, description="[green]Agent 1/4: Cache patterns analyzed[/green]")

            # Agent 2: Strategy
            progress.update(task, description="[cyan]Agent 2/4: Designing strategy...[/cyan]")
            strategy = await self.strategist.design_strategy(analysis, requirements)
            progress.update(task, description="[green]Agent 2/4: Strategy designed[/green]")

            # Agent 3: Code generation
            progress.update(task, description="[cyan]Agent 3/4: Generating implementation...[/cyan]")
            implementations = await self.codegen.generate_code(strategy, codebase_info)
            progress.update(task, description="[green]Agent 3/4: Implementation generated[/green]")

            # Agent 4: Monitoring
            progress.update(task, description="[cyan]Agent 4/4: Designing monitoring...[/cyan]")
            monitoring = await self.monitor.generate_monitoring(strategy, implementations)
            progress.update(task, description="[green]Agent 4/4: Monitoring designed[/green]")

        final = {
            "pipeline": "CacheFlow",
            "analysis": analysis,
            "strategy": strategy,
            "implementations": implementations,
            "monitoring": monitoring,
        }
        Path(output).write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")

        table = Table(title="CacheFlow Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        if "estimated_total_improvement" in strategy:
            for k, v in strategy["estimated_total_improvement"].items():
                table.add_row(k, str(v))
        if "cache_candidates" in analysis:
            table.add_row("Cache Candidates", str(len(analysis["cache_candidates"])))
        console.print(table)
        console.print(f"\n[bold green]Report saved to {output}[/bold green]")


@click.group()
def cli():
    pass


@cli.command()
@click.argument("target_path")
@click.option("--requirements", "-r", default="", help="Additional requirements")
@click.option("--output", "-o", default="cacheflow_report.json", help="Output file")
def analyze(target_path, requirements, output):
    """Analyze and optimize caching strategies."""
    config = Config()
    if not config.api_key:
        console.print("[red]Error: DEEPSEEK_API_KEY not set.[/red]")
        sys.exit(1)
    pipeline = CacheFlowPipeline(config)
    asyncio.run(pipeline.run(target_path, requirements, output))


if __name__ == "__main__":
    cli()
