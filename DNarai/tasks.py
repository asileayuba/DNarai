import logging
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.template.loader import render_to_string
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
            'completion_link': f"{settings.SITE_URL}/complete-session/{booking.session_completion_token}/"
        })

        # Plain text fallback
        text_content = f"Hi {booking.full_name}, please confirm your session here: {settings.SITE_URL}/complete-session/{booking.session_completion_token}/"

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        logger.info(f"[Completion Email] Sent to {to_email} for booking ID {booking_id}")

    except ObjectDoesNotExist:
        logger.error(f"[Completion Email] Booking with ID {booking_id} not found.")
    except Exception as e:
        logger.exception(f"[Completion Email] Error sending for booking {booking_id}, retrying...")
        raise self.retry(exc=e)
