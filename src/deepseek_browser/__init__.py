"""High level interfaces for browser automation."""

from .task_executor import TaskExecutor, Task, TaskResult
from .monitoring import Monitor

__all__ = ["TaskExecutor", "Task", "TaskResult", "Monitor"]
