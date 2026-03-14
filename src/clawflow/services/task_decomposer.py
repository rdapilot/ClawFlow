from __future__ import annotations

from clawflow.domain.models import Intent, TaskNode


class TaskDecomposer:
    def decompose(self, intent: Intent) -> list[TaskNode]:
        tasks = [
            TaskNode(
                id="research",
                name="research market",
                description=f"Investigate the {intent.domain} landscape for the requested objective.",
                expected_output="research findings and competitive observations",
                system_prompt="You are a research specialist focused on evidence-backed analysis.",
            ),
            TaskNode(
                id="audience",
                name="define audience",
                description="Identify target audience, segments, and needs.",
                expected_output="audience segments and personas",
                system_prompt="You translate research into actionable audience definitions.",
                dependencies=["research"],
            ),
            TaskNode(
                id="strategy",
                name="develop strategy",
                description=f"Create a strategy to achieve: {intent.objective}.",
                expected_output="strategic narrative and campaign approach",
                system_prompt="You create concise, high-value execution strategies.",
                dependencies=["research", "audience"],
            ),
            TaskNode(
                id="copy",
                name="create copy",
                description="Write campaign messaging and copy assets.",
                expected_output="copy deck and messaging hierarchy",
                system_prompt="You write clear, audience-specific campaign copy.",
                dependencies=["strategy"],
            ),
            TaskNode(
                id="design",
                name="design assets",
                description="Propose visual concepts and asset directions.",
                expected_output="visual asset recommendations",
                system_prompt="You design practical concepts aligned with strategy.",
                dependencies=["strategy"],
            ),
            TaskNode(
                id="launch",
                name="plan distribution",
                description="Sequence rollout, channels, and execution timeline.",
                expected_output="distribution schedule and rollout checklist",
                system_prompt="You design operational launch plans with clear sequencing.",
                dependencies=["copy", "design"],
            ),
        ]
        return tasks

