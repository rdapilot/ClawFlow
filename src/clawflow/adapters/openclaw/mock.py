from __future__ import annotations

from clawflow.adapters.openclaw.base import AgentProfile, OpenClawGateway
from clawflow.domain.models import TaskNode, TaskResult, TaskStatus


class MockOpenClawGateway(OpenClawGateway):
    def __init__(self) -> None:
        self._agents = [
            AgentProfile(
                name="research_agent",
                capabilities={"research", "analysis", "market"},
                reliability_score=0.98,
                response_latency_ms=120,
            ),
            AgentProfile(
                name="strategist_agent",
                capabilities={"strategy", "planning", "audience"},
                reliability_score=0.97,
                response_latency_ms=90,
            ),
            AgentProfile(
                name="copywriter_agent",
                capabilities={"copy", "content", "campaign", "messaging"},
                reliability_score=0.95,
                response_latency_ms=80,
            ),
            AgentProfile(
                name="design_agent",
                capabilities={"design", "visual", "creative", "assets"},
                reliability_score=0.92,
                response_latency_ms=140,
            ),
            AgentProfile(
                name="ops_agent",
                capabilities={"distribution", "scheduling", "launch", "delivery"},
                reliability_score=0.94,
                response_latency_ms=70,
            ),
        ]

    def connect(self) -> bool:
        return True

    def discover_agents(self) -> list[AgentProfile]:
        return self._agents

    def execute_task(self, task: TaskNode) -> TaskResult:
        agent_name = task.assigned_agent or "unassigned_agent"
        output = (
            f"{task.name} completed by {agent_name}. "
            f"Expected output delivered: {task.expected_output}."
        )
        return TaskResult(
            task_id=task.id,
            status=TaskStatus.completed,
            agent_name=agent_name,
            output=output,
            latency_ms=90,
        )

