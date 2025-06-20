"""Run multiple tasks concurrently for higher throughput."""

import asyncio
from deepseek_browser import TaskExecutor
from task_templates import task_templates


async def run_many() -> None:
    executor = TaskExecutor()
    await executor.start()
    try:
        tasks = [
            executor.execute(task_templates["research"]["news_summarization"].description.format(topic="AI")),
            executor.execute(task_templates["e-commerce"]["price_comparison"].description.format(product="headphones")),
            executor.execute(task_templates["social_media"]["monitoring"].description.format(keyword="AI")),
        ]
        results = await asyncio.gather(*tasks)
        for t in results:
            print(t.task_id, t.status)
    finally:
        await executor.close()


if __name__ == "__main__":
    asyncio.run(run_many())
