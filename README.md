# DeepSeek Browser Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

DeepSeek Browser Automation provides tools and utilities to script browsers using modern Python libraries. It is designed to work well with [playwright](https://playwright.dev) and other frameworks to automate complex tasks. See the [API reference](docs/api_reference.md) for detailed usage information. Recent versions include built-in monitoring for tracking task metrics and exporting analytics.

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


## Deployment

The project ships with several options for running the automation stack:

### Docker

A multi‑stage `Dockerfile` builds an isolated runtime image. Build and run with:

```bash
docker build -t deepseek-browser .
docker run --env-file .env deepseek-browser
```

### Docker Compose

Use `docker-compose.yml` for a full stack including Prometheus and Grafana:

```bash
docker compose up
```

### Cloud Scripts

Scripts under `deploy/cloud/` push the Docker image to AWS, GCP or Azure and
create the corresponding container service. Each script requires the vendor’s CLI
and credentials.

### Local Installation

Helper scripts in `scripts/` install Python dependencies on Linux, macOS or
Windows. Run the script that matches your system to set up a local environment.

### Environment Configuration

Copy `.env.example` to `.env` and adjust values to configure model endpoints and
logging.

### Health Checks and Monitoring

A simple health check script is included at `scripts/healthcheck.sh`. Metrics can
be exported through the built-in `Monitor` class and visualised via the bundled
Prometheus/Grafana setup.

