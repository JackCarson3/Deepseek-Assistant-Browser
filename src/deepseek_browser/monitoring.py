import json
import logging
import time
from typing import Dict, List, TYPE_CHECKING

import psutil

if TYPE_CHECKING:  # pragma: no cover - avoid circular import
    from .task_executor import Task


class Monitor:
    """Collect analytics and performance metrics."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.metrics: Dict[str, List] = {
            "tasks_total": 0,
            "tasks_success": 0,
            "tasks_failed": 0,
            "tasks_timeout": 0,
            "durations": [],
            "errors": [],
            "resource_usage": [],
        }

    def record_task(self, task: "Task") -> None:
        """Record metrics for a completed task."""
        self.metrics["tasks_total"] += 1
        if task.status == "success":
            self.metrics["tasks_success"] += 1
        elif task.status == "failed":
            self.metrics["tasks_failed"] += 1
            if task.error:
                self.metrics["errors"].append(task.error)
        elif task.status == "timeout":
            self.metrics["tasks_timeout"] += 1

        if task.started_at and task.finished_at:
            duration = (task.finished_at - task.started_at).total_seconds()
            self.metrics["durations"].append(duration)

        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        self.metrics["resource_usage"].append(
            {"cpu": cpu, "memory": mem, "timestamp": time.time()}
        )

    def get_report(self) -> Dict[str, float | List]:
        """Return a summary of collected metrics."""
        total = self.metrics["tasks_total"]
        success_rate = (
            self.metrics["tasks_success"] / total if total else 0
        )
        avg_duration = (
            sum(self.metrics["durations"]) / len(self.metrics["durations"])
            if self.metrics["durations"]
            else 0
        )
        return {
            "total_tasks": total,
            "success_rate": success_rate,
            "avg_duration": avg_duration,
            "errors": self.metrics["errors"],
        }

    def export_json(self, path: str) -> None:
        """Export all metrics to a JSON file."""
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.metrics, fh, indent=2, default=str)
        self.logger.info("Analytics exported to %s", path)
