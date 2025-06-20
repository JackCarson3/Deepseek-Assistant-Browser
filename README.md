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

## Example Task Templates

Several pre-built task templates are provided under `examples/`. They cover common use cases in research, data collection, e-commerce and social media automation. See [docs/examples.md](docs/examples.md) for details and expected outputs.

## Monitoring and Analytics

`deepseek_browser.Monitor` can be attached to a `TaskExecutor` to collect task
metrics, error details and browser resource usage. Collected analytics can be
exported to JSON for further analysis:

```python
from deepseek_browser import TaskExecutor, Monitor

monitor = Monitor()
executor = TaskExecutor(monitor=monitor)
asyncio.run(executor.start())
asyncio.run(executor.execute("Check example.com"))
asyncio.run(executor.close())
report = monitor.get_report()
monitor.export_json("metrics.json")
```

