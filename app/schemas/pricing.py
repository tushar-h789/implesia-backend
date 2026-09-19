import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PathCard(BaseModel):
    icon: str | None = Field(None, max_length=80)
    kicker: str = Field(default="", max_length=80)
    title: str = Field(min_length=2, max_length=160)
    body: str = Field(min_length=8, max_length=800)
    note: str = Field(default="", max_length=160)
    cta_label: str = Field(default="", max_length=80)
    anchor: str = Field(default="", max_length=80)


class CommercialTerm(BaseModel):
    icon: str | None = Field(None, max_length=80)
    title: str = Field(min_length=2, max_length=80)
    body: str = Field(min_length=4, max_length=400)


class ProcessStep(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)


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


class PricingPageBase(BaseModel):
    slug: str = Field(default="pricing", min_length=2, max_length=80)
    hero_heading: str = Field(min_length=4, max_length=200)
    hero_body: str = Field(min_length=8, max_length=2000)
    paths_kicker: str = Field(default="", max_length=120)
    paths_heading: str = Field(default="", max_length=200)
    paths_body: str = Field(default="", max_length=800)
    paths: list[PathCard] = Field(default_factory=list)
    models_kicker: str = Field(default="", max_length=120)
    models_heading: str = Field(default="", max_length=200)
    models_body: str = Field(default="", max_length=800)
    models_currency_note: str = Field(default="", max_length=200)
    models_disclaimer: str = Field(default="", max_length=2000)
    packages_kicker: str = Field(default="", max_length=120)
    packages_heading: str = Field(default="", max_length=200)
    packages_body: str = Field(default="", max_length=800)
    packages_currency_note: str = Field(default="", max_length=200)
    commercial_terms: list[CommercialTerm] = Field(default_factory=list)
    packages_disclaimer: str = Field(default="", max_length=4000)
    process_kicker: str = Field(default="", max_length=120)
    process_heading: str = Field(default="", max_length=200)
    process_body: str = Field(default="", max_length=800)
    process_steps: list[ProcessStep] = Field(default_factory=list)
    faqs_kicker: str = Field(default="", max_length=120)
    faqs_heading: str = Field(default="", max_length=200)
    faqs: list[FaqItem] = Field(default_factory=list)
    cta_heading: str = Field(default="", max_length=200)
    cta_body: str = Field(default="", max_length=800)
    cta_highlights: list[str] = Field(default_factory=list)
    cta_primary_label: str = Field(default="", max_length=80)
    cta_secondary_label: str = Field(default="", max_length=80)
    seo_title: str | None = Field(None, max_length=80)
    seo_description: str | None = Field(None, max_length=200)
    bdt_per_usd: int = Field(default=123, ge=1, le=1000)

    @field_validator("process_steps", mode="before")
    @classmethod
    def _coerce_steps(cls, value: Any) -> Any:
        return _as_steps(value)


class PricingPageUpdate(BaseModel):
    hero_heading: str | None = Field(None, min_length=4, max_length=200)
    hero_body: str | None = Field(None, min_length=8, max_length=2000)
    paths_kicker: str | None = Field(None, max_length=120)
    paths_heading: str | None = Field(None, max_length=200)
    paths_body: str | None = Field(None, max_length=800)
    paths: list[PathCard] | None = None
    models_kicker: str | None = Field(None, max_length=120)
    models_heading: str | None = Field(None, max_length=200)
    models_body: str | None = Field(None, max_length=800)
    models_currency_note: str | None = Field(None, max_length=200)
    models_disclaimer: str | None = Field(None, max_length=2000)
    packages_kicker: str | None = Field(None, max_length=120)
    packages_heading: str | None = Field(None, max_length=200)
    packages_body: str | None = Field(None, max_length=800)
    packages_currency_note: str | None = Field(None, max_length=200)
    commercial_terms: list[CommercialTerm] | None = None
    packages_disclaimer: str | None = Field(None, max_length=4000)
    process_kicker: str | None = Field(None, max_length=120)
    process_heading: str | None = Field(None, max_length=200)
    process_body: str | None = Field(None, max_length=800)
    process_steps: list[ProcessStep] | None = None
    faqs_kicker: str | None = Field(None, max_length=120)
    faqs_heading: str | None = Field(None, max_length=200)
    faqs: list[FaqItem] | None = None
    cta_heading: str | None = Field(None, max_length=200)
    cta_body: str | None = Field(None, max_length=800)
    cta_highlights: list[str] | None = None
    cta_primary_label: str | None = Field(None, max_length=80)
    cta_secondary_label: str | None = Field(None, max_length=80)
    seo_title: str | None = Field(None, max_length=80)
    seo_description: str | None = Field(None, max_length=200)
    bdt_per_usd: int | None = Field(None, ge=1, le=1000)

    @field_validator("process_steps", mode="before")
    @classmethod
    def _coerce_steps(cls, value: Any) -> Any:
        if value is None:
            return value
        return _as_steps(value)


class PricingPageRead(PricingPageBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class EngagementModelBase(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    slug: str | None = Field(None, min_length=2, max_length=180)
    icon: str | None = Field(None, max_length=80)
    kicker: str = Field(default="", max_length=120)
    badge: str | None = Field(None, max_length=80)
    price_label: str = Field(min_length=2, max_length=80)
    price_amount: int | None = Field(None, ge=0)
    currency: str = Field(default="USD", max_length=8)
    cadence: str = Field(default="one_time", max_length=20)
    subtitle: str = Field(default="", max_length=200)
    description: str = Field(min_length=8, max_length=2000)
    inclusions: list[str] = Field(default_factory=list)
    ideal_for: str = Field(default="", max_length=160)
    cta_label: str = Field(default="Discuss this model", max_length=80)
    is_published: bool = True
    sort_order: int = 0


class EngagementModelCreate(EngagementModelBase):
    pass


class EngagementModelUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=160)
    slug: str | None = Field(None, min_length=2, max_length=180)
    icon: str | None = Field(None, max_length=80)
    kicker: str | None = Field(None, max_length=120)
    badge: str | None = Field(None, max_length=80)
    price_label: str | None = Field(None, min_length=2, max_length=80)
    price_amount: int | None = Field(None, ge=0)
    currency: str | None = Field(None, max_length=8)
    cadence: str | None = Field(None, max_length=20)
    subtitle: str | None = Field(None, max_length=200)
    description: str | None = Field(None, min_length=8, max_length=2000)
    inclusions: list[str] | None = None
    ideal_for: str | None = Field(None, max_length=160)
    cta_label: str | None = Field(None, max_length=80)
    is_published: bool | None = None
    sort_order: int | None = None


class EngagementModelRead(EngagementModelBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    created_at: datetime
    updated_at: datetime


class PricingPackageBase(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    slug: str | None = Field(None, min_length=2, max_length=180)
    icon: str | None = Field(None, max_length=80)
    tagline: str = Field(min_length=4, max_length=200)
    badge: str | None = Field(None, max_length=80)
    price_label: str = Field(min_length=2, max_length=80)
    price_amount_bdt: int = Field(ge=0)
    timeline_label: str = Field(default="", max_length=80)
    bugfix_label: str = Field(default="", max_length=80)
    audience: str = Field(default="", max_length=160)
    description: str = Field(min_length=8, max_length=2000)
    dashboard_heading: str = Field(default="", max_length=120)
    dashboard_body: str = Field(default="", max_length=800)
    inclusions: list[str] = Field(default_factory=list)
    exclusions: list[str] = Field(default_factory=list)
    cta_label: str = Field(default="", max_length=120)
    is_published: bool = True
    sort_order: int = 0


class PricingPackageCreate(PricingPackageBase):
    pass


class PricingPackageUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=160)
    slug: str | None = Field(None, min_length=2, max_length=180)
    icon: str | None = Field(None, max_length=80)
    tagline: str | None = Field(None, min_length=4, max_length=200)
    badge: str | None = Field(None, max_length=80)
    price_label: str | None = Field(None, min_length=2, max_length=80)
    price_amount_bdt: int | None = Field(None, ge=0)
    timeline_label: str | None = Field(None, max_length=80)
    bugfix_label: str | None = Field(None, max_length=80)
    audience: str | None = Field(None, max_length=160)
    description: str | None = Field(None, min_length=8, max_length=2000)
    dashboard_heading: str | None = Field(None, max_length=120)
    dashboard_body: str | None = Field(None, max_length=800)
    inclusions: list[str] | None = None
    exclusions: list[str] | None = None
    cta_label: str | None = Field(None, max_length=120)
    is_published: bool | None = None
    sort_order: int | None = None


class PricingPackageRead(PricingPackageBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    created_at: datetime
    updated_at: datetime


class PricingPagePublic(PricingPageRead):
    models: list[EngagementModelRead] = Field(default_factory=list)
    packages: list[PricingPackageRead] = Field(default_factory=list)
