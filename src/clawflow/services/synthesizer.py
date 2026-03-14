from __future__ import annotations

from clawflow.domain.models import Intent, TaskResult


class ResultSynthesizer:
    def synthesize(self, intent: Intent, results: list[TaskResult]) -> str:
        sections = [
            f"Objective: {intent.objective}",
            f"Domain: {intent.domain}",
            "Deliverables:",
        ]
        sections.extend(f"- {deliverable}" for deliverable in intent.deliverables)
        sections.append("Task Outputs:")
        sections.extend(f"- {result.output}" for result in results)
        return "\n".join(sections)

