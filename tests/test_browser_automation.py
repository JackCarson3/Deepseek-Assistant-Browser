import asyncio

from deepseek_browser.task_executor import TaskExecutor


class MockAgent:
    async def create_agent(self):
        pass

    async def run_task(self, description: str):
        return [f"done {description}"]

    async def close(self):
        pass


class ErrorAgent(MockAgent):
    async def run_task(self, description: str):
        raise RuntimeError("boom")


def test_task_executor_with_mock_agent():
    async def run():
        executor = TaskExecutor(agent=MockAgent())
        await executor.start()
        task = await executor.execute("ping")
        await executor.close()
        return task

    task = asyncio.run(run())
    assert task.status == "success"
    assert task.result.history == ["done ping"]


def test_task_executor_error_case():
    async def run():
        executor = TaskExecutor(agent=ErrorAgent())
        await executor.start()
        task = await executor.execute("fail")
        await executor.close()
        return task

    task = asyncio.run(run())
    assert task.status == "failed"
    assert "boom" in task.error


def test_execute_stream():
    async def run():
        executor = TaskExecutor(agent=MockAgent())
        await executor.start()
        items = []
        async for update in executor.execute_stream("stream"):
            items.append(update)
        await executor.close()
        return items

    updates = asyncio.run(run())
    assert updates[0]["status"] == "running"
    assert updates[-1]["status"] == "success"
