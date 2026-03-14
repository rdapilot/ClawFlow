from __future__ import annotations

from pydantic import BaseModel, Field


class RetryPolicy(BaseModel):
    max_attempts: int = 3
    backoff_seconds: float = 0.5


class ClawFlowSettings(BaseModel):
    app_name: str = "ClawFlow"
    environment: str = "development"
    adapter_name: str = "mock-openclaw"
    max_parallel_tasks: int = Field(default=50, ge=1)
    scheduler_latency_ms_target: int = Field(default=100, ge=1)
    startup_target_seconds: int = Field(default=3, ge=1)
    retry_policy: RetryPolicy = Field(default_factory=RetryPolicy)

