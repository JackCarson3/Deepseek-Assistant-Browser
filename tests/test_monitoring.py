import asyncio

from deepseek_browser.monitoring import Monitor
from deepseek_browser.task_executor import TaskExecutor


class ToggleAgent:
    def __init__(self):
        self.calls = 0

    async def create_agent(self):
        pass

    async def run_task(self, description: str):
        self.calls += 1
        if self.calls == 2:
            raise RuntimeError("boom")
        return ["ok"]

    async def close(self):
        pass


def test_monitor_collects_metrics(tmp_path):
    async def run():
        monitor = Monitor()
        executor = TaskExecutor(agent=ToggleAgent(), monitor=monitor)
        await executor.start()
        await executor.execute("one")
        await executor.execute("two")  # will fail
        await executor.close()
        path = tmp_path / "metrics.json"
        monitor.export_json(path)
        return monitor.metrics, path

    metrics, path = asyncio.run(run())
    assert metrics["tasks_total"] == 2
    assert metrics["tasks_failed"] == 1
    assert path.exists()
