"""Example: Compare prices for a product across e-commerce sites."""

import asyncio
from deepseek_browser import TaskExecutor
from task_templates import task_templates


template = task_templates["e-commerce"]["price_comparison"].description


async def main(product: str = "laptop") -> None:
    executor = TaskExecutor()
    await executor.start()
    try:
        description = template.format(product=product)
        task = await executor.execute(description)
        print("Status:", task.status)
        if task.result:
            print("History:", task.result.history)
    finally:
        await executor.close()


if __name__ == "__main__":
    asyncio.run(main())
