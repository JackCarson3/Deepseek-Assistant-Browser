# API Reference

This page documents the public classes and methods provided by **DeepSeek Browser Automation**.

## `BrowserAgentConfig`
Configuration options for `BrowserAgent`.

| Field | Type | Description |
|-------|------|-------------|
| `model_name` | `str` | Name of the LLM model used by Ollama. |
| `ollama_url` | `str` | Base URL of the Ollama server. |
| `temperature` | `float` | Sampling temperature for the model. |
| `headless` | `bool` | Whether to launch the browser in headless mode. |
| `viewport` | `tuple[int, int] \| None` | Custom viewport size. |
| `disable_security` | `bool` | Disable browser security features. |
| `deterministic_rendering` | `bool` | Render pages deterministically for reproducible output. |
| `browser_args` | `list[str]` | Additional Chromium arguments. |
| `browser_options` | `dict[str, Any]` | Extra options forwarded to the browser. |
| `retries` | `int` | Number of times to retry a failed task. |

## `BrowserAgent`
Wraps `browser_use.Agent` and manages a `BrowserSession`.

### Methods
- `create_agent() -> None`
  - Initialize the language model and browser session.
  - Raises an exception if the session fails to start.

- `run_task(task_description: str) -> list[Any]`
  - Execute a natural language task with automatic reconnection and retries.
  - Returns the interaction history with the assistant.

- `close() -> None`
  - Shut down the browser session and clean up resources.

**Usage example**
```python
from ollama_config import BrowserAgent, BrowserAgentConfig

config = BrowserAgentConfig(model_name="deepseek")
agent = BrowserAgent(config)
await agent.create_agent()
result = await agent.run_task("Open example.com")
await agent.close()
```

## `TaskExecutor`
High-level interface for running tasks via `BrowserAgent`.

### Methods
- `start() -> None`
  - Create the underlying `BrowserAgent` instance.

- `execute(description: str, timeout: int | None = None) -> Task`
  - Run a task and wait for completion.

- `execute_stream(description: str, timeout: int | None = None)`
  - Async generator yielding progress updates while executing the task.

- `history() -> list[Task]`
  - Return the list of previously executed tasks.

- `close() -> None`
  - Close the agent and release resources.

**Usage example**
```python
from deepseek_browser import TaskExecutor

executor = TaskExecutor()
await executor.start()

# Run a single task
result = await executor.execute("Open example.com")
print(result.status, result.result.history)

# Stream progress
async for update in executor.execute_stream("Open example.com"):
    print(update)

await executor.close()
```

## Error Codes
`Task.status` may be one of:

- `"success"` – task completed without error.
- `"failed"` – an exception occurred (details in `Task.error`).
- `"timeout"` – execution exceeded the timeout.

Check the `error` attribute for troubleshooting information. If the browser session becomes disconnected, `BrowserAgent` automatically recreates it and retries according to `retries`.

## Performance Tips
- Run multiple tasks concurrently using `asyncio.gather` as shown in `examples/performance_patterns.py`.
- Adjust the `retries` option of `BrowserAgentConfig` to balance reliability and latency.
- Use `execute_stream` to process partial results in long-running tasks.

## Integration Examples
The library is compatible with `playwright` and other automation frameworks. A typical integration looks like:
```python
from deepseek_browser import TaskExecutor
from playwright.async_api import async_playwright

async with async_playwright() as p:
    executor = TaskExecutor()
    await executor.start()
    await executor.execute("Capture screenshot of example.com")
    await executor.close()
```

## OpenAPI/Swagger
This package exposes no HTTP endpoints, so an OpenAPI specification is not applicable.

