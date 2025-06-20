import asyncio

from deepseek_browser.task_executor import TaskExecutor


class MockAgent:
    async def create_agent(self):
        pass

    async def run_task(self, description: str):
        return [f"handled {description}"]

    async def close(self):
        pass


def test_execute_success():
    async def run():
        executor = TaskExecutor(agent=MockAgent())
        await executor.start()
        task = await executor.execute("do something")
        await executor.close()
        return task, executor.history()

    task, history = asyncio.run(run())
    assert task.status == "success"
    assert task.result.history == ["handled do something"]
    assert len(history) == 1


class SlowAgent(MockAgent):
    async def run_task(self, description: str):
        await asyncio.sleep(0.2)
        return ["slow"]


def test_execute_timeout():
    async def run():
        executor = TaskExecutor(agent=SlowAgent(), default_timeout=0.05)
        await executor.start()
        task = await executor.execute("slow task")
        await executor.close()
        return task

    task = asyncio.run(run())
    assert task.status == "timeout"
