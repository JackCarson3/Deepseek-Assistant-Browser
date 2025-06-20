"""High level interfaces for browser automation."""

from .task_executor import TaskExecutor, Task, TaskResult
from .templates import TaskTemplate, TemplateLibrary

__all__ = [
    "TaskExecutor",
    "Task",
    "TaskResult",
    "TaskTemplate",
    "TemplateLibrary",
]
