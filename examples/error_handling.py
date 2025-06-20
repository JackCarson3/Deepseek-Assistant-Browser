"""Error handling best practices when executing tasks."""

import asyncio
from deepseek_browser import TaskExecutor
from deepseek_browser.task_executor import Task


async def safe_execute(executor: TaskExecutor, description: str) -> Task:
    try:
        task = await executor.execute(description)
    except Exception as exc:
        print("Error running task:", exc)
        raise
    if task.status != "success":
        print("Task finished with status", task.status)
        if task.error:
            print("Error message:", task.error)
    return task


async def main() -> None:
    executor = TaskExecutor()
    await executor.start()
    try:
        await safe_execute(executor, "Open invalid_url")
    finally:
        await executor.close()


if __name__ == "__main__":
    asyncio.run(main())
