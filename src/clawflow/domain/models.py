from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


def utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


@dataclass(slots=True)
class Intent:
    prompt: str
    domain: str
    objective: str
    deliverables: list[str]
    constraints: list[str] = field(default_factory=list)
    scope: str = "standard"


@dataclass(slots=True)
class TaskNode:
    id: str
    name: str
    description: str
    expected_output: str
    system_prompt: str
    dependencies: list[str] = field(default_factory=list)
    assigned_agent: str | None = None
    retryable: bool = True


@dataclass(slots=True)
class TaskResult:
    task_id: str
    status: TaskStatus
    agent_name: str
    output: str
    latency_ms: int
    attempts: int = 1
    error: str | None = None


@dataclass(slots=True)
class PipelineRun:
    id: str
    prompt: str
    intent: Intent
    tasks: list[TaskNode]
    results: list[TaskResult]
    final_output: str
    status: TaskStatus
    started_at: datetime = field(default_factory=utcnow)
    completed_at: datetime | None = None

