import asyncio
import time

from deepseek_browser.task_executor import TaskExecutor


class FastAgent:
    async def create_agent(self):
        pass

    async def run_task(self, description: str):
        return ["ok"]

    async def close(self):
        pass


def test_task_execution_benchmark():
    async def run():
        executor = TaskExecutor(agent=FastAgent())
        await executor.start()
        start = time.perf_counter()
        for _ in range(5):
            await executor.execute("bench")
        duration = time.perf_counter() - start
        await executor.close()
        return duration

    total = asyncio.run(run())
    assert total < 1.0
