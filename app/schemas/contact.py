import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HeroMetric(BaseModel):
    value: str = Field(min_length=1, max_length=40)
    label: str = Field(min_length=1, max_length=80)


class Channel(BaseModel):
    icon: str | None = Field(None, max_length=80)
    title: str = Field(min_length=2, max_length=80)
    value: str = Field(min_length=2, max_length=160)
    body: str = Field(default="", max_length=200)
    href: str | None = Field(None, max_length=255)


class OfficeHour(BaseModel):
    days: str = Field(min_length=2, max_length=80)
    hours: str = Field(min_length=2, max_length=80)


class FormOption(BaseModel):
    value: str = Field(min_length=1, max_length=80)
    label: str = Field(min_length=1, max_length=120)


class ProcessStep(BaseModel):
    number: str = Field(default="", max_length=8)
    icon: str | None = Field(None, max_length=80)
    timing: str = Field(default="", max_length=40)
    title: str = Field(min_length=2, max_length=160)
    body: str = Field(min_length=8, max_length=800)


class FaqItem(BaseModel):
    question: str = Field(min_length=4, max_length=280)
    answer: str = Field(min_length=4, max_length=2000)


class ContactPageBase(BaseModel):
    slug: str = Field(default="contact", min_length=2, max_length=80)
    hero_kicker: str = Field(default="", max_length=120)
    hero_heading: str = Field(min_length=4, max_length=200)
    hero_body: str = Field(min_length=8, max_length=2000)
    hero_highlights: list[str] = Field(default_factory=list)
    hero_metrics: list[HeroMetric] = Field(default_factory=list)
    form_intro: str = Field(default="", max_length=800)
    channels_kicker: str = Field(default="", max_length=120)
    channels_heading: str = Field(default="", max_length=200)
    channels_body: str = Field(default="", max_length=800)
    channels: list[Channel] = Field(default_factory=list)
    office_hours_heading: str = Field(default="", max_length=120)
    office_hours: list[OfficeHour] = Field(default_factory=list)
    office_hours_note: str = Field(default="", max_length=400)
    form_heading: str = Field(default="", max_length=200)
    form_body: str = Field(default="", max_length=400)
    form_privacy: str = Field(default="", max_length=800)
    form_submit_label: str = Field(default="", max_length=80)
    form_action: str = Field(default="/api/v1/leads", max_length=120)
    service_options: list[FormOption] = Field(default_factory=list)
    timeline_options: list[FormOption] = Field(default_factory=list)
    process_kicker: str = Field(default="", max_length=120)
    process_heading: str = Field(default="", max_length=200)
    process_body: str = Field(default="", max_length=800)
    process_steps: list[ProcessStep] = Field(default_factory=list)
    process_quote: str = Field(default="", max_length=800)
    faqs_kicker: str = Field(default="", max_length=120)
    faqs_heading: str = Field(default="", max_length=200)
    faqs_body: str = Field(default="", max_length=800)
    faq_highlights: list[str] = Field(default_factory=list)
    faqs: list[FaqItem] = Field(default_factory=list)
    faqs_cta_heading: str = Field(default="", max_length=200)
    faqs_cta_body: str = Field(default="", max_length=400)
    agreement_note: str = Field(default="", max_length=400)
    agreement_kicker: str = Field(default="", max_length=160)
    cta_heading: str = Field(default="", max_length=200)
    cta_body: str = Field(default="", max_length=800)
    cta_highlights: list[str] = Field(default_factory=list)
    cta_primary_label: str = Field(default="", max_length=80)
    cta_secondary_label: str = Field(default="", max_length=80)
    seo_title: str | None = Field(None, max_length=80)
    seo_description: str | None = Field(None, max_length=200)


class ContactPageUpdate(BaseModel):
    hero_kicker: str | None = Field(None, max_length=120)
    hero_heading: str | None = Field(None, min_length=4, max_length=200)
    hero_body: str | None = Field(None, min_length=8, max_length=2000)
    hero_highlights: list[str] | None = None
    hero_metrics: list[HeroMetric] | None = None
    form_intro: str | None = Field(None, max_length=800)
    channels_kicker: str | None = Field(None, max_length=120)
    channels_heading: str | None = Field(None, max_length=200)
    channels_body: str | None = Field(None, max_length=800)
    channels: list[Channel] | None = None
    office_hours_heading: str | None = Field(None, max_length=120)
    office_hours: list[OfficeHour] | None = None
    office_hours_note: str | None = Field(None, max_length=400)
    form_heading: str | None = Field(None, max_length=200)
    form_body: str | None = Field(None, max_length=400)
    form_privacy: str | None = Field(None, max_length=800)
    form_submit_label: str | None = Field(None, max_length=80)
    form_action: str | None = Field(None, max_length=120)
    service_options: list[FormOption] | None = None
    timeline_options: list[FormOption] | None = None
    process_kicker: str | None = Field(None, max_length=120)
    process_heading: str | None = Field(None, max_length=200)
    process_body: str | None = Field(None, max_length=800)
    process_steps: list[ProcessStep] | None = None
    process_quote: str | None = Field(None, max_length=800)
    faqs_kicker: str | None = Field(None, max_length=120)
    faqs_heading: str | None = Field(None, max_length=200)
    faqs_body: str | None = Field(None, max_length=800)
    faq_highlights: list[str] | None = None
    faqs: list[FaqItem] | None = None
    faqs_cta_heading: str | None = Field(None, max_length=200)
    faqs_cta_body: str | None = Field(None, max_length=400)
    agreement_note: str | None = Field(None, max_length=400)
    agreement_kicker: str | None = Field(None, max_length=160)
    cta_heading: str | None = Field(None, max_length=200)
    cta_body: str | None = Field(None, max_length=800)
    cta_highlights: list[str] | None = None
    cta_primary_label: str | None = Field(None, max_length=80)
    cta_secondary_label: str | None = Field(None, max_length=80)
    seo_title: str | None = Field(None, max_length=80)
    seo_description: str | None = Field(None, max_length=200)
    internal_notes: str | None = Field(None, max_length=4000)


class ContactPagePublic(ContactPageBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ContactPageAdmin(ContactPagePublic):
    internal_notes: str | None = None
