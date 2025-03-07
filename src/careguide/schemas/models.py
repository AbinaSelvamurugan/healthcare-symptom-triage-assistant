"""Strict boundary schemas. Synthetic text is untrusted and ephemeral."""
from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Category(StrEnum):
    EMERGENCY = "EMERGENCY"
    URGENT = "URGENT"
    GENERAL_INFO = "GENERAL_INFO"
    CLARIFICATION = "CLARIFICATION"
    CLINICIAN_REFERRAL = "CLINICIAN_REFERRAL"
    UNSUPPORTED = "UNSUPPORTED"
    PROVIDER_FAILURE = "PROVIDER_FAILURE"


class Input(StrictModel):
    narrative: str = Field(min_length=1, max_length=3000)

    @field_validator("narrative")
    @classmethod
    def validate_content(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("empty input")
        if any(ord(ch) < 32 and ch not in "\t\n\r" for ch in value):
            raise ValueError("control characters are not allowed")
        return " ".join(value.split())  # whitespace only; retains substantive words/punctuation


class Question(StrictModel):
    id: str = Field(pattern=r"^Q_[A-Z0-9_]+$")
    field: str = Field(min_length=2)
    prompt: str = Field(min_length=10)


class Rule(StrictModel):
    id: str = Field(pattern=r"^[A-Z][A-Z0-9_-]+$")
    version: str = Field(min_length=1)
    approval_status: Literal["DEMONSTRATION_ONLY", "APPROVED"]
    applicable_population: str = Field(min_length=4)
    trigger_any: list[str] = Field(min_length=1)
    required_information: list[str] = Field(min_length=1)
    escalation_category: Literal["EMERGENCY", "URGENT", "GENERAL_INFO"]
    user_instruction: str = Field(min_length=25)
    source: str = Field(min_length=8)
    review_date: date | None
    reviewer: str | None
    limitations: str = Field(min_length=8)

    @field_validator("trigger_any")
    @classmethod
    def clean_patterns(cls, v: list[str]) -> list[str]:
        if any(len(p) < 4 or len(p) > 100 for p in v):
            raise ValueError("triggers must be 4-100 characters")
        return v

    @model_validator(mode="after")
    def check_approval(self) -> Rule:
        if self.approval_status == "APPROVED" and (not self.review_date or not self.reviewer):
            raise ValueError("approved rules must have review date and reviewer")
        return self


class Protocol(StrictModel):
    protocol_id: str
    protocol_version: str
    source: str
    status: Literal["DEMONSTRATION_ONLY", "APPROVED"]
    jurisdiction: str
    population: str
    review_date: date | None
    reviewer: str | None
    limitations: str
    questions: list[Question]
    rules: list[Rule]

    @model_validator(mode="after")
    def validate_protocol(self) -> Protocol:
        ids = [r.id for r in self.rules]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate rule identifiers")
        if self.status == "APPROVED":
            if not self.review_date or not self.reviewer:
                raise ValueError("approved protocol needs reviewer and review date")
            if any(r.approval_status != "APPROVED" for r in self.rules):
                raise ValueError("approved protocol cannot contain demo rules")
        return self


class ModelProposal(StrictModel):
    user_message: str = Field(min_length=1, max_length=1200)
    proposed_response_category: Category
    follow_up_question: str | None = None
    missing_information: list[str]
    referenced_rule_ids: list[str]
    refusal: bool
    escalation_recommendation: Category | None = None
    validation_status: Literal["proposed"]


class Decision(StrictModel):
    category: Category
    message: str
    rule_ids: list[str] = Field(default_factory=list)
    next_question: str | None = None
    validation_status: Literal["accepted", "fallback", "rejected"] = "accepted"
    provider_latency_ms: int | None = None
    state: str = ""
