"""Local configuration is never sourced from user messages."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from careguide.schemas import Protocol

ROOT = Path(__file__).resolve().parents[2]


class AppConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode: Literal["offline_demo", "claude_demo"] = "offline_demo"
    jurisdiction: str = "unspecified"
    emergency_contact: str | None = None
    max_input_chars: int = Field(default=3000, ge=32, le=3000)
    max_questions: int = Field(default=2, ge=0, le=5)
    session_ttl_minutes: int = Field(default=30, ge=1, le=1440)
    provider_timeout_seconds: float = Field(default=12, ge=1, le=120)
    provider_max_retries: int = Field(default=1, ge=0, le=2)

    @model_validator(mode="after")
    def reject_contact_with_unknown_jurisdiction(self) -> AppConfig:
        if self.jurisdiction == "unspecified" and self.emergency_contact:
            raise ValueError("local emergency contact requires known jurisdiction")
        return self


class Policy(BaseModel):
    model_config = ConfigDict(extra="forbid")
    policy_version: str
    uncertainty_instruction: str
    provider_failure_instruction: str
    unsupported_instruction: str
    emergency_fallback_instruction: str


def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected YAML object in {path.name}")
    return data


def load_config(root: Path = ROOT) -> tuple[AppConfig, Policy, Protocol]:
    conf = _load_yaml(root / "configs/application.yaml")
    conf["mode"] = os.getenv("CAREGUIDE_MODE", conf.get("mode", "offline_demo"))
    app = AppConfig.model_validate(conf)
    policy = Policy.model_validate(_load_yaml(root / "configs/safety_policy.yaml"))
    protocol = Protocol.model_validate(_load_yaml(root / "configs/clinical_rules.example.yaml"))
    if protocol.status != "DEMONSTRATION_ONLY":
        raise ValueError("Clinical/approved protocol operation is not supported by this demo build")
    # Missing provider credentials/model affect language generation, never deterministic rules.
    return app, policy, protocol
