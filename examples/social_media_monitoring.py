"""Example: Monitor social media for posts mentioning a keyword."""

import asyncio
from deepseek_browser import TaskExecutor
from task_templates import task_templates


template = task_templates["social_media"]["monitoring"].description


async def main(keyword: str = "deep learning") -> None:
    executor = TaskExecutor()
    await executor.start()
    try:
        description = template.format(keyword=keyword)
        task = await executor.execute(description)
        print("Status:", task.status)
        if task.result:
            print("History:", task.result.history)
    finally:
        await executor.close()


if __name__ == "__main__":
    asyncio.run(main())
