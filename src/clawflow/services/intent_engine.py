from __future__ import annotations

from clawflow.domain.models import Intent


class IntentEngine:
    def analyze(self, prompt: str) -> Intent:
        lowered = prompt.lower()
        domain = "general"
        objective = "deliver a multi-agent outcome"
        deliverables = ["summary", "execution plan"]

        if any(term in lowered for term in ("marketing", "campaign", "brand", "social media")):
            domain = "marketing"
            objective = "build a campaign plan"
            deliverables = ["research report", "campaign strategy", "creative assets", "launch schedule"]
        elif any(term in lowered for term in ("product", "launch", "go to market")):
            domain = "product"
            objective = "prepare a launch program"
            deliverables = ["market brief", "launch plan", "messaging kit"]
        elif any(term in lowered for term in ("research", "study", "scientific")):
            domain = "research"
            objective = "produce a structured research workflow"
            deliverables = ["research brief", "analysis summary"]

        constraints = []
        if "startup" in lowered:
            constraints.append("optimize for lean startup resources")
        if "fast" in lowered:
            constraints.append("prioritize time-to-delivery")

        return Intent(
            prompt=prompt,
            domain=domain,
            objective=objective,
            deliverables=deliverables,
            constraints=constraints,
            scope="standard",
        )

