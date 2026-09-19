import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HeroMetric(BaseModel):
    value: str = Field(min_length=1, max_length=40)
    label: str = Field(min_length=1, max_length=80)


class Pillar(BaseModel):
    icon: str | None = Field(None, max_length=80)
    title: str = Field(min_length=2, max_length=160)
    body: str = Field(min_length=8, max_length=800)


class FounderHighlight(BaseModel):
    label: str = Field(min_length=1, max_length=80)
    value: str = Field(min_length=1, max_length=120)


class Commitment(BaseModel):
    icon: str | None = Field(None, max_length=80)
    kicker: str = Field(default="", max_length=80)
    timing: str = Field(default="", max_length=40)
    title: str = Field(min_length=4, max_length=200)
    body: str = Field(min_length=8, max_length=1200)


class Tenet(BaseModel):
    icon: str | None = Field(None, max_length=80)
    kicker: str = Field(default="", max_length=80)
    title: str = Field(min_length=2, max_length=120)
    body: str = Field(min_length=8, max_length=800)


class Foundation(BaseModel):
    icon: str | None = Field(None, max_length=80)
    kicker: str = Field(default="", max_length=80)
    title: str = Field(min_length=2, max_length=120)
    body: str = Field(min_length=8, max_length=800)


class CultureItem(BaseModel):
    icon: str | None = Field(None, max_length=80)
    title: str = Field(min_length=2, max_length=120)
    body: str = Field(min_length=8, max_length=800)


class AboutPageBase(BaseModel):
    slug: str = Field(default="about-us", min_length=2, max_length=80)
    hero_kicker: str = Field(default="", max_length=120)
    hero_heading: str = Field(min_length=4, max_length=200)
    hero_body: str = Field(min_length=8, max_length=2000)
    hero_primary_label: str = Field(default="", max_length=80)
    hero_secondary_label: str = Field(default="", max_length=80)
    hero_highlights: list[str] = Field(default_factory=list)
    hero_metrics: list[HeroMetric] = Field(default_factory=list)
    quote_kicker: str = Field(default="", max_length=120)
    quote_text: str = Field(default="", max_length=800)
    quote_attribution: str = Field(default="", max_length=160)
    story_kicker: str = Field(default="", max_length=120)
    story_heading: str = Field(default="", max_length=200)
    story_body: str = Field(default="", max_length=2000)
    story_emphasis: str = Field(default="", max_length=280)
    story_body_secondary: str = Field(default="", max_length=2000)
    pillars: list[Pillar] = Field(default_factory=list)
    operating_principles_heading: str = Field(default="", max_length=120)
    operating_principles: list[str] = Field(default_factory=list)
    founder_name: str = Field(default="", max_length=120)
    founder_role: str = Field(default="", max_length=120)
    founder_org: str = Field(default="", max_length=120)
    founder_kicker: str = Field(default="", max_length=120)
    founder_heading: str = Field(default="", max_length=200)
    founder_lede: str = Field(default="", max_length=800)
    founder_body: str = Field(default="", max_length=4000)
    founder_close: str = Field(default="", max_length=400)
    founder_signoff: str = Field(default="", max_length=80)
    founder_location: str = Field(default="", max_length=120)
    founder_cta_label: str = Field(default="", max_length=80)
    founder_highlights: list[FounderHighlight] = Field(default_factory=list)
    purpose_kicker: str = Field(default="", max_length=120)
    purpose_heading: str = Field(default="", max_length=200)
    purpose_body: str = Field(default="", max_length=800)
    commitments: list[Commitment] = Field(default_factory=list)
    tenets_kicker: str = Field(default="", max_length=120)
    tenets_heading: str = Field(default="", max_length=200)
    tenets_body: str = Field(default="", max_length=800)
    tenets: list[Tenet] = Field(default_factory=list)
    stability_kicker: str = Field(default="", max_length=120)
    stability_heading: str = Field(default="", max_length=200)
    stability_body: str = Field(default="", max_length=800)
    stability_quote_kicker: str = Field(default="", max_length=120)
    stability_quote: str = Field(default="", max_length=800)
    foundations: list[Foundation] = Field(default_factory=list)
    culture_kicker: str = Field(default="", max_length=120)
    culture_heading: str = Field(default="", max_length=200)
    culture_body: str = Field(default="", max_length=800)
    culture_items: list[CultureItem] = Field(default_factory=list)
    culture_cta_label: str = Field(default="", max_length=80)
    cta_heading: str = Field(default="", max_length=200)
    cta_body: str = Field(default="", max_length=800)
    cta_highlights: list[str] = Field(default_factory=list)
    cta_primary_label: str = Field(default="", max_length=80)
    cta_secondary_label: str = Field(default="", max_length=80)
    seo_title: str | None = Field(None, max_length=80)
    seo_description: str | None = Field(None, max_length=200)


class AboutPageUpdate(BaseModel):
    hero_kicker: str | None = Field(None, max_length=120)
    hero_heading: str | None = Field(None, min_length=4, max_length=200)
    hero_body: str | None = Field(None, min_length=8, max_length=2000)
    hero_primary_label: str | None = Field(None, max_length=80)
    hero_secondary_label: str | None = Field(None, max_length=80)
    hero_highlights: list[str] | None = None
    hero_metrics: list[HeroMetric] | None = None
    quote_kicker: str | None = Field(None, max_length=120)
    quote_text: str | None = Field(None, max_length=800)
    quote_attribution: str | None = Field(None, max_length=160)
    story_kicker: str | None = Field(None, max_length=120)
    story_heading: str | None = Field(None, max_length=200)
    story_body: str | None = Field(None, max_length=2000)
    story_emphasis: str | None = Field(None, max_length=280)
    story_body_secondary: str | None = Field(None, max_length=2000)
    pillars: list[Pillar] | None = None
    operating_principles_heading: str | None = Field(None, max_length=120)
    operating_principles: list[str] | None = None
    founder_name: str | None = Field(None, max_length=120)
    founder_role: str | None = Field(None, max_length=120)
    founder_org: str | None = Field(None, max_length=120)
    founder_kicker: str | None = Field(None, max_length=120)
    founder_heading: str | None = Field(None, max_length=200)
    founder_lede: str | None = Field(None, max_length=800)
    founder_body: str | None = Field(None, max_length=4000)
    founder_close: str | None = Field(None, max_length=400)
    founder_signoff: str | None = Field(None, max_length=80)
    founder_location: str | None = Field(None, max_length=120)
    founder_cta_label: str | None = Field(None, max_length=80)
    founder_highlights: list[FounderHighlight] | None = None
    purpose_kicker: str | None = Field(None, max_length=120)
    purpose_heading: str | None = Field(None, max_length=200)
    purpose_body: str | None = Field(None, max_length=800)
    commitments: list[Commitment] | None = None
    tenets_kicker: str | None = Field(None, max_length=120)
    tenets_heading: str | None = Field(None, max_length=200)
    tenets_body: str | None = Field(None, max_length=800)
    tenets: list[Tenet] | None = None
    stability_kicker: str | None = Field(None, max_length=120)
    stability_heading: str | None = Field(None, max_length=200)
    stability_body: str | None = Field(None, max_length=800)
    stability_quote_kicker: str | None = Field(None, max_length=120)
    stability_quote: str | None = Field(None, max_length=800)
    foundations: list[Foundation] | None = None
    culture_kicker: str | None = Field(None, max_length=120)
    culture_heading: str | None = Field(None, max_length=200)
    culture_body: str | None = Field(None, max_length=800)
    culture_items: list[CultureItem] | None = None
    culture_cta_label: str | None = Field(None, max_length=80)
    cta_heading: str | None = Field(None, max_length=200)
    cta_body: str | None = Field(None, max_length=800)
    cta_highlights: list[str] | None = None
    cta_primary_label: str | None = Field(None, max_length=80)
    cta_secondary_label: str | None = Field(None, max_length=80)
    seo_title: str | None = Field(None, max_length=80)
    seo_description: str | None = Field(None, max_length=200)
    internal_notes: str | None = Field(None, max_length=4000)


class AboutPagePublic(AboutPageBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class AboutPageAdmin(AboutPagePublic):
    internal_notes: str | None = None
