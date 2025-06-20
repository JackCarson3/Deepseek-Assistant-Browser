"""Example: Summarize news articles about a specific topic."""

import asyncio
from deepseek_browser import TaskExecutor
from task_templates import task_templates


template = task_templates["research"]["news_summarization"].description


async def main(topic: str = "technology") -> None:
    executor = TaskExecutor()
    await executor.start()
    try:
        description = template.format(topic=topic)
        task = await executor.execute(description)
        print("Status:", task.status)
        if task.result:
            print("History:", task.result.history)
    finally:
        await executor.close()


if __name__ == "__main__":
    asyncio.run(main())
