import logging
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from core.models import LeadershipSessionBooking

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_task(self, subject, html_content, recipient_list, from_email=None, text_content=None):
    """
    Generic email sending task.
    """
    try:
        from_email = from_email or settings.DEFAULT_FROM_EMAIL

        # fallback plain text
        if not text_content:
            text_content = "This is an HTML email. Please use a compatible email client."

        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        logger.info(f"[Email Task] Sent '{subject}' to {recipient_list}")

    except Exception as e:
        logger.exception(f"[Email Task] Failed to send '{subject}' to {recipient_list}, retrying...")
        raise self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_session_completion_email(self, booking_id):
    """
    Sends a session completion prompt email to the user for a LeadershipSessionBooking.
    """
    try:
        booking = LeadershipSessionBooking.objects.get(id=booking_id)

        if not booking.email:
            logger.warning(f"[Completion Email] Booking {booking_id} has no email address.")
            return

        subject = "Please Confirm Your Session Completion"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = booking.email

        # Render HTML template
        html_content = render_to_string('emails/session_completion_prompt.html', {
            'booking': booking,
            'completion_link': f"{settings.BASE_URL}/complete-session/{booking.session_completion_token}/"
        })

        # Plain text fallback
        text_content = f"Hi {booking.full_name}, please confirm your session here: {settings.BASE_URL}/complete-session/{booking.session_completion_token}/"

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        logger.info(f"[Completion Email] Sent to {to_email} for booking ID {booking_id}")

    except ObjectDoesNotExist:
        logger.error(f"[Completion Email] Booking with ID {booking_id} not found.")
    except Exception as e:
        logger.exception(f"[Completion Email] Error sending for booking {booking_id}, retrying...")
        raise self.retry(exc=e)


@shared_task
def send_pending_session_reminders():
    """
    Find bookings needing a reminder and send emails.
    """
    now = timezone.now()
    reminder_window = now + timedelta(hours=24)
    recent_reminder_cutoff = now - timedelta(hours=6)

    # Find bookings that need a reminder
    bookings = LeadershipSessionBooking.objects.filter(
        preferred_datetime__gte=now,
        preferred_datetime__lte=reminder_window,
        is_mentor_confirmed=False,
        is_session_completed=False
    ).exclude(
        last_reminder_sent_at__gte=recent_reminder_cutoff
    )

    for booking in bookings:
        html_content = render_to_string(
            "emails/session_reminder.html",
            {"booking": booking}
        )
        send_email_task.delay(
            "Session Reminder: Please Confirm Your Attendance",
            html_content,
            [booking.email],
            settings.DEFAULT_FROM_EMAIL
        )
        # Update last_reminder_sent_at
        booking.last_reminder_sent_at = now
        booking.save(update_fields=["last_reminder_sent_at"])
