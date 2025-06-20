import asyncio
import json

from deepseek_browser.task_executor import TaskExecutor
from deepseek_browser.monitoring import Monitor


class DummyAgent:
    async def create_agent(self):
        pass

    async def run_task(self, description: str, task_id=None):
        return ["ok"]

    async def close(self):
        pass


def test_monitor_collects_metrics(tmp_path):
    async def run():
        mon = Monitor()
        executor = TaskExecutor(agent=DummyAgent(), monitor=mon)
        await executor.start()
        await executor.execute("demo")
        await executor.close()
        path = tmp_path / "stats.json"
        executor.export_metrics(str(path))
        return mon, path

    mon, path = asyncio.run(run())
    assert len(mon.tasks) == 1
    assert mon.tasks[0].status == "success"
    assert path.exists()
    data = json.loads(path.read_text())
    assert "tasks" in data


def test_resource_usage():
    mon = Monitor()
    usage = mon.resource_usage()
    assert "cpu_percent" in usage
