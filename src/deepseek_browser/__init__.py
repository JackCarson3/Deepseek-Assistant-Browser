"""High level interfaces for browser automation with optional monitoring."""

__all__ = [
    "TaskExecutor",
    "Task",
    "TaskResult",
    "Monitor",
    "TaskTemplate",
    "TemplateLibrary",
]


def __getattr__(name):
    if name in {"TaskExecutor", "Task", "TaskResult"}:
        from . import task_executor as mod
        return getattr(mod, name)
    if name == "Monitor":
        from .monitoring import Monitor
        return Monitor
    if name in {"TaskTemplate", "TemplateLibrary"}:
        from . import templates as mod
        return getattr(mod, name)
    raise AttributeError(name)
