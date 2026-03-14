from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from clawflow.domain.models import TaskNode, TaskResult


@dataclass(slots=True)
class AgentProfile:
    name: str
    capabilities: set[str]
    reliability_score: float
    response_latency_ms: int


class OpenClawGateway(Protocol):
    def connect(self) -> bool:
        """Connect to the OpenClaw runtime."""

    def discover_agents(self) -> list[AgentProfile]:
        """Return available agents from the registry."""

    def execute_task(self, task: TaskNode) -> TaskResult:
        """Dispatch a task to OpenClaw and return its result."""

