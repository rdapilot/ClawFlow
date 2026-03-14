from __future__ import annotations

from clawflow.adapters.openclaw.base import AgentProfile
from clawflow.domain.models import TaskNode


class AgentAllocator:
    def allocate(self, tasks: list[TaskNode], agents: list[AgentProfile]) -> list[TaskNode]:
        for task in tasks:
            task_terms = set(task.name.lower().split()) | set(task.description.lower().split())
            ranked = sorted(
                agents,
                key=lambda agent: (
                    len(task_terms & agent.capabilities),
                    agent.reliability_score,
                    -agent.response_latency_ms,
                ),
                reverse=True,
            )
            task.assigned_agent = ranked[0].name if ranked else None
        return tasks

