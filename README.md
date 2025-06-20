# DeepSeek Browser Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

DeepSeek Browser Automation provides tools and utilities to script browsers using modern Python libraries. It is designed to work well with [playwright](https://playwright.dev) and other frameworks to automate complex tasks.

## Installation
```bash
pip install -r requirements.txt
```

## Project Layout
- **src/** – library source code
- **tests/** – test suite
- **docs/** – project documentation
- **examples/** – usage examples

## License
Released under the MIT license.

## Task Execution System

The `TaskExecutor` class allows running natural language tasks using the DeepSeek R1 model through Ollama. It manages a browser session via `browser-use` and tracks the progress and result of each task.

```python
import asyncio
from deepseek_browser import TaskExecutor

async def main():
    executor = TaskExecutor()
    await executor.start()
    task = await executor.execute("Open example.com")
    print(task.status, task.result)
    await executor.close()

asyncio.run(main())
```
