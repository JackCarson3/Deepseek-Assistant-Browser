import asyncio
from deepseek_browser import TaskExecutor


async def main():
    executor = TaskExecutor()
    await executor.start()

    task = await executor.execute("Open example.com")
    print(task)

    await executor.close()


if __name__ == "__main__":
    asyncio.run(main())
