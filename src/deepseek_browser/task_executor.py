import asyncio
import logging
import time
import inspect
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Optional

from ollama_config import BrowserAgent, BrowserAgentConfig
from .monitoring import Monitor


@dataclass
class TaskResult:
    """Result object returned after a task finishes.

    Attributes
    ----------
    success:
        Whether the task completed successfully.
    history:
        Raw interaction history returned by ``BrowserAgent``.
    """

    success: bool
    history: Any


@dataclass
class Task:
    """Representation of a user instruction executed by :class:`TaskExecutor`.

    Attributes
    ----------
    description:
        Natural language instruction provided by the user.
    task_id:
        Unique identifier assigned by ``TaskExecutor``.
    status:
        Current status. One of ``pending``, ``running``, ``success``, ``failed``
        or ``timeout``.
    result:
        Populated with a :class:`TaskResult` when the task finishes successfully.
    error:
        Error message when ``status`` is ``failed`` or ``timeout``.
    created_at:
        Timestamp when the task object was created.
    started_at:
        Timestamp when execution began.
    finished_at:
        Timestamp when execution finished.
    """

    description: str
    task_id: int
    status: str = "pending"
    result: Optional[TaskResult] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None


class TaskExecutor:
    """Execute tasks using :class:`BrowserAgent` with progress tracking.

    Parameters
    ----------
    agent_config:
        Optional :class:`BrowserAgentConfig` to customize the underlying agent.
    default_timeout:
        Timeout applied to :meth:`execute` and :meth:`execute_stream` when none
        is provided.
    agent:
        Existing :class:`BrowserAgent` instance. Mainly used for testing.
    """

    def __init__(
        self,
        agent_config: Optional[BrowserAgentConfig] = None,
        default_timeout: int = 300,
        agent: Optional[BrowserAgent] = None,
        monitor: Optional[Monitor] = None,
    ) -> None:
        self.monitor = monitor or Monitor()
        self.agent = agent or BrowserAgent(agent_config, monitor=self.monitor)
        self.default_timeout = default_timeout
        self.tasks: List[Task] = []
        self.logger = logging.getLogger(self.__class__.__name__)

    async def start(self) -> None:
        """Initialize the underlying :class:`BrowserAgent`.

        Must be called before executing any tasks.
        """
        await self.agent.create_agent()

    async def execute(self, description: str, timeout: Optional[int] = None) -> Task:
        """Execute a single task.

        Parameters
        ----------
        description:
            Natural language instruction for the agent.
        timeout:
            Optional per-task timeout in seconds.

        Returns
        -------
        Task
            Object containing status, result and metadata.
        """
        task = Task(description=description, task_id=len(self.tasks) + 1)
        self.tasks.append(task)

        self.logger.info("Starting task %s: %s", task.task_id, description)
        task.status = "running"
        task.started_at = datetime.utcnow()

        try:
            start = time.perf_counter()
            if 'task_id' in inspect.signature(self.agent.run_task).parameters:
                history = await asyncio.wait_for(
                    self.agent.run_task(description, task_id=task.task_id),
                    timeout=timeout or self.default_timeout,
                )
            else:
                history = await asyncio.wait_for(
                    self.agent.run_task(description),
                    timeout=timeout or self.default_timeout,
                )
            _ = time.perf_counter() - start
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
            if self.monitor:
                duration = (task.finished_at - task.started_at).total_seconds()
                self.monitor.record_task(task, duration)

        return task

    async def execute_stream(self, description: str, timeout: Optional[int] = None):
        """Execute a task and yield progress updates.

        Yields
        ------
        dict
            Progress dictionaries containing ``task_id``, ``status`` and
            optionally ``history`` or ``error``.
        """
        task = Task(description=description, task_id=len(self.tasks) + 1)
        self.tasks.append(task)
        task.status = "running"
        task.started_at = datetime.utcnow()
        yield {"task_id": task.task_id, "status": task.status}

        try:
            start = time.perf_counter()
            if 'task_id' in inspect.signature(self.agent.run_task).parameters:
                history = await asyncio.wait_for(
                    self.agent.run_task(description, task_id=task.task_id),
                    timeout=timeout or self.default_timeout,
                )
            else:
                history = await asyncio.wait_for(
                    self.agent.run_task(description),
                    timeout=timeout or self.default_timeout,
                )
            _ = time.perf_counter() - start
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
            if self.monitor:
                duration = (task.finished_at - task.started_at).total_seconds()
                self.monitor.record_task(task, duration)

    def history(self) -> List[Task]:
        """Return the list of executed tasks in order of submission."""
        return self.tasks

    async def close(self) -> None:
        """Close the underlying browser agent and free resources.

        It is safe to call this method multiple times.
        """
        await self.agent.close()

    def export_metrics(self, path: str) -> None:
        """Export collected analytics data to ``path``."""
        if self.monitor:
            self.monitor.export_json(path)
