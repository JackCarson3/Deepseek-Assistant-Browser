"""High level interfaces for browser automation."""

from .task_executor import TaskExecutor, Task, TaskResult

__version__ = "0.1.0"

__all__ = ["TaskExecutor", "Task", "TaskResult"]
