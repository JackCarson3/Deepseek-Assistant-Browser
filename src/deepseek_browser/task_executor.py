import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Optional

from .monitoring import Monitor

from ollama_config import BrowserAgent, BrowserAgentConfig


@dataclass
class TaskResult:
    """Structured result from a task."""

    success: bool
    history: Any


@dataclass
class Task:
    """Representation of a single task."""

    description: str
    task_id: int
    status: str = "pending"
    result: Optional[TaskResult] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None


class TaskExecutor:
    """Execute tasks using :class:`BrowserAgent` with progress tracking."""

    def __init__(
        self,
        agent_config: Optional[BrowserAgentConfig] = None,
        default_timeout: int = 300,
        agent: Optional[BrowserAgent] = None,
        monitor: Optional[Monitor] = None,
    ) -> None:
        self.agent = agent or BrowserAgent(agent_config)
        self.default_timeout = default_timeout
        self.tasks: List[Task] = []
        self.monitor = monitor
        self.logger = logging.getLogger(self.__class__.__name__)

    async def start(self) -> None:
        """Initialize the underlying agent."""
        await self.agent.create_agent()

    async def execute(self, description: str, timeout: Optional[int] = None) -> Task:
        """Execute a task and return a :class:`Task` with results."""
        task = Task(description=description, task_id=len(self.tasks) + 1)
        self.tasks.append(task)

        self.logger.info("Starting task %s: %s", task.task_id, description)
        task.status = "running"
        task.started_at = datetime.utcnow()

        try:
            history = await asyncio.wait_for(
                self.agent.run_task(description),
                timeout=timeout or self.default_timeout,
            )
            task.result = TaskResult(success=True, history=history)
            task.status = "success"
        except asyncio.TimeoutError:
            task.status = "timeout"
            task.error = "Task timed out"
            self.logger.warning("Task %s timed out", task.task_id)
        except Exception as exc:  # pragma: no cover - safety net
            task.status = "failed"
            task.error = str(exc)
            self.logger.exception("Task %s failed: %s", task.task_id, exc)
        finally:
            task.finished_at = datetime.utcnow()
            if self.monitor is not None:
                self.monitor.record_task(task)

        return task

    async def execute_stream(self, description: str, timeout: Optional[int] = None):
        """Execute a task and yield progress updates."""
        task = Task(description=description, task_id=len(self.tasks) + 1)
        self.tasks.append(task)
        task.status = "running"
        task.started_at = datetime.utcnow()
        yield {"task_id": task.task_id, "status": task.status}

        try:
            history = await asyncio.wait_for(
                self.agent.run_task(description),
                timeout=timeout or self.default_timeout,
            )
            task.result = TaskResult(success=True, history=history)
            task.status = "success"
            yield {"task_id": task.task_id, "status": task.status, "history": history}
        except asyncio.TimeoutError:
            task.status = "timeout"
            task.error = "Task timed out"
            yield {"task_id": task.task_id, "status": task.status}
        except Exception as exc:  # pragma: no cover - safety net
            task.status = "failed"
            task.error = str(exc)
            yield {"task_id": task.task_id, "status": task.status, "error": str(exc)}
        finally:
            task.finished_at = datetime.utcnow()
            if self.monitor is not None:
                self.monitor.record_task(task)

    def history(self) -> List[Task]:
        """Return the list of executed tasks."""
        return self.tasks

    async def close(self) -> None:
        """Close the underlying browser agent."""
        await self.agent.close()
