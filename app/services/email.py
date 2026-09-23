from email.message import EmailMessage

import aiosmtplib

from app.core.config import settings
from app.core.logging import get_logger
from app.models.lead import Lead
from app.models.order import Order

logger = get_logger(__name__)


async def send_email(to: list[str], subject: str, body: str) -> None:
    """Send a plain-text email, or log it when SMTP is not configured."""
    if not to:
        return

    if not settings.emails_enabled:
        logger.info("email_skipped_no_smtp", to=to, subject=subject)
        return

    message = EmailMessage()
    message["From"] = f"{settings.email_from_name} <{settings.email_from}>"
    message["To"] = ", ".join(to)
    message["Subject"] = subject
    message.set_content(body)

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_user or None,
            password=settings.smtp_password or None,
            start_tls=settings.smtp_tls,
        )
        logger.info("email_sent", to=to, subject=subject)
    except Exception as exc:
        # A failed notification must never lose the lead that is already saved.
        logger.error("email_failed", to=to, subject=subject, error=str(exc))


def _lead_summary(lead: Lead) -> str:
    return "\n".join(
        [
            f"Name:         {lead.full_name}",
            f"Email:        {lead.email}",
            f"Phone:        {lead.phone or '-'}",
            f"Organisation: {lead.organisation or '-'}",
            f"Service:      {lead.service_area.value if lead.service_area else '-'}",
            f"Timeline:     {lead.timeline.value if lead.timeline else '-'}",
            f"Source page:  {lead.source_page or '-'}",
            "",
            "Brief:",
            lead.brief,
        ]
    )


async def notify_team_of_lead(lead: Lead) -> None:
    await send_email(
        to=settings.lead_notification_recipients,
        subject=f"New enquiry — {lead.full_name} ({lead.organisation or 'no org'})",
        body=_lead_summary(lead),
    )


def _order_target_name(order: Order) -> str:
    if order.service is not None:
        return order.service.name
    if order.package is not None:
        return order.package.name
    if order.model is not None:
        return order.model.name
    return "a catalogue item"


def _order_summary(order: Order) -> str:
    return "\n".join(
        [
            f"Service:      {order.service.name if order.service else '-'}",
            f"Package:      {order.package.name if order.package else '-'}",
            f"Model:        {order.model.name if order.model else '-'}",
            f"Name:         {order.full_name}",
            f"Email:        {order.email}",
            f"Phone:        {order.phone or '-'}",
            f"Organisation: {order.organisation or '-'}",
            f"Source page:  {order.source_page or '-'}",
            "",
            "Message:",
            order.message,
        ]
    )


async def notify_team_of_order(order: Order) -> None:
    """Best-effort inbox alert. Uses free Gmail SMTP when configured; otherwise logs."""
    target = _order_target_name(order)
    await send_email(
        to=settings.lead_notification_recipients,
        subject=f"New service order — {target} ({order.full_name})",
        body=_order_summary(order),
    )


async def acknowledge_order(order: Order) -> None:
    service_name = _order_target_name(order)
    body = (
        f"Hi {order.full_name},\n\n"
        f"Thank you for ordering {service_name}. Our team has the request and will "
        "reply within one business day.\n\n"
        "For anything urgent you can reach us on WhatsApp at +8801516527932.\n\n"
        "— Implesia IT Ltd."
    )
    await send_email(
        to=[order.email],
        subject=f"We received your order — {service_name}",
        body=body,
    )


async def acknowledge_lead(lead: Lead) -> None:
    body = (
        f"Hi {lead.full_name},\n\n"
        "Thank you for reaching out to Implesia IT. Your project brief has reached our "
        "team and a senior engineer will respond within one business day.\n\n"
        "For anything urgent you can reach us on WhatsApp at +8801516527932.\n\n"
        "— Implesia IT Ltd."
    )
    await send_email(to=[lead.email], subject="We received your project brief", body=body)
