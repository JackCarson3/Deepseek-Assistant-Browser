import json
import logging
import psutil
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional


@dataclass
class TaskMetric:
    task_id: int
    description: str
    status: str
    duration: float
    error: Optional[str] = None


@dataclass
class ModelCallMetric:
    task_id: int
    duration: float


class Monitor:
    """Collect execution and performance metrics."""

    def __init__(self) -> None:
        self.tasks: List[TaskMetric] = []
        self.model_calls: List[ModelCallMetric] = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def record_task(self, task, duration: float) -> None:
        self.tasks.append(
            TaskMetric(
                task_id=task.task_id,
                description=task.description,
                status=task.status,
                duration=duration,
                error=task.error,
            )
        )
        self.logger.debug("Recorded task %s (%s)", task.task_id, task.status)

    def record_model_call(self, task_id: int, duration: float) -> None:
        self.model_calls.append(ModelCallMetric(task_id=task_id, duration=duration))
        self.logger.debug("Recorded model call for task %s", task_id)

    def resource_usage(self):
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory": psutil.virtual_memory()._asdict(),
        }

    def export_json(self, path: str) -> None:
        data = {
            "tasks": [asdict(t) for t in self.tasks],
            "model_calls": [asdict(m) for m in self.model_calls],
            "resource_usage": self.resource_usage(),
            "generated_at": datetime.utcnow().isoformat(),
        }
        with open(path, "w") as fh:
            json.dump(data, fh, indent=2)

