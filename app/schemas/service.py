import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class HeroMetric(BaseModel):
    value: str = Field(min_length=1, max_length=40)
    label: str = Field(min_length=1, max_length=80)


class ProcessStep(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)


class Outcome(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=400)
    value: str | None = Field(None, max_length=40)


class FaqItem(BaseModel):
    question: str = Field(min_length=4, max_length=280)
    answer: str = Field(min_length=4, max_length=2000)


def _as_steps(value: Any) -> list[dict[str, str]]:
    if not value:
        return []
    steps: list[dict[str, str]] = []
    for item in value:
        if isinstance(item, str):
            steps.append({"title": item, "description": ""})
        elif isinstance(item, dict):
            steps.append(item)
        else:
            steps.append(item.model_dump())
    return steps


class ServiceBase(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    slug: str | None = Field(None, min_length=2, max_length=180)
    tagline: str = Field(min_length=8, max_length=280)
    description: str = Field(min_length=20, max_length=8000)
    category: str = Field(default="engineering", min_length=2, max_length=80)
    icon: str | None = Field(None, max_length=80)
    engagement_status: str = Field(default="Available", max_length=40)

    tech_stack: list[str] = Field(default_factory=list)
    hero_metrics: list[HeroMetric] = Field(default_factory=list)

    deliver_heading: str = Field(default="What we deliver", max_length=160)
    deliver_body: str = Field(default="", max_length=4000)
    capabilities: list[str] = Field(default_factory=list)
    deliverables_heading: str = Field(default="What You Receive", max_length=160)
    deliverables_kicker: str = Field(default="Included in every engagement", max_length=160)
    deliverables: list[str] = Field(default_factory=list)

    process_heading: str = Field(default="How we work", max_length=160)
    process_body: str = Field(default="", max_length=2000)
    process_steps: list[ProcessStep] = Field(default_factory=list)

    outcomes_heading: str = Field(default="Before → After", max_length=160)
    outcomes_body: str = Field(default="", max_length=2000)
    outcomes_disclaimer: str = Field(default="", max_length=400)
    outcomes: list[Outcome] = Field(default_factory=list)

    related_heading: str = Field(default="Related services", max_length=160)
    related_slugs: list[str] = Field(default_factory=list)

    faqs_heading: str = Field(default="Still have questions?", max_length=160)
    faqs_body: str = Field(default="", max_length=400)
    faqs: list[FaqItem] = Field(default_factory=list)

    cta_heading: str = Field(default="Ready to architect your digital future?", max_length=160)
    cta_body: str = Field(default="", max_length=800)
    cta_highlights: list[str] = Field(
        default_factory=lambda: ["Free Strategy Call", "NDA Available", "Senior Engineers"]
    )

    seo_title: str | None = Field(None, max_length=80)
    seo_description: str | None = Field(None, max_length=200)

    is_published: bool = True
    sort_order: int = 0

    @field_validator("process_steps", mode="before")
    @classmethod
    def _coerce_steps(cls, value: Any) -> Any:
        return _as_steps(value)


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=160)
    slug: str | None = Field(None, min_length=2, max_length=180)
    tagline: str | None = Field(None, min_length=8, max_length=280)
    description: str | None = Field(None, min_length=20, max_length=8000)
    category: str | None = Field(None, min_length=2, max_length=80)
    icon: str | None = Field(None, max_length=80)
    engagement_status: str | None = Field(None, max_length=40)
    tech_stack: list[str] | None = None
    hero_metrics: list[HeroMetric] | None = None
    deliver_heading: str | None = Field(None, max_length=160)
    deliver_body: str | None = Field(None, max_length=4000)
    capabilities: list[str] | None = None
    deliverables_heading: str | None = Field(None, max_length=160)
    deliverables_kicker: str | None = Field(None, max_length=160)
    deliverables: list[str] | None = None
    process_heading: str | None = Field(None, max_length=160)
    process_body: str | None = Field(None, max_length=2000)
    process_steps: list[ProcessStep] | None = None
    outcomes_heading: str | None = Field(None, max_length=160)
    outcomes_body: str | None = Field(None, max_length=2000)
    outcomes_disclaimer: str | None = Field(None, max_length=400)
    outcomes: list[Outcome] | None = None
    related_heading: str | None = Field(None, max_length=160)
    related_slugs: list[str] | None = None
    faqs_heading: str | None = Field(None, max_length=160)
    faqs_body: str | None = Field(None, max_length=400)
    faqs: list[FaqItem] | None = None
    cta_heading: str | None = Field(None, max_length=160)
    cta_body: str | None = Field(None, max_length=800)
    cta_highlights: list[str] | None = None
    seo_title: str | None = Field(None, max_length=80)
    seo_description: str | None = Field(None, max_length=200)
    is_published: bool | None = None
    sort_order: int | None = None

    @field_validator("process_steps", mode="before")
    @classmethod
    def _coerce_steps(cls, value: Any) -> Any:
        if value is None:
            return value
        return _as_steps(value)


class ServiceRead(ServiceBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    created_at: datetime
    updated_at: datetime


class ServiceSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    tagline: str
    icon: str | None = None
    is_published: bool
