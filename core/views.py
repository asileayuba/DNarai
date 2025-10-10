import uuid
import logging
from datetime import timedelta, timezone as dt_timezone  # Updated for Django 5
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timezone import make_naive
from django.contrib.auth.decorators import login_required

from .forms import LeadershipSessionBookingForm
from .models import LeadershipSessionBooking, SendMessage
from DNarai.tasks import (
    send_session_completion_email,
    send_email_task,
)

logger = logging.getLogger(__name__)


def index(request):
    """Homepage view"""
    return render(request, "core/index.html")


@login_required(login_url="accounts:login")
def booking_view(request):
    """Handles session booking by mentees"""
    if request.method == "POST":
        form = LeadershipSessionBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.mentor_confirmation_token = uuid.uuid4().hex
            booking.session_completion_token = uuid.uuid4().hex
            booking.token_generated_at = timezone.now()
            booking.save()

            # Schedule session completion reminder email
            session_duration = booking.session_duration.get_timedelta()
            run_eta = booking.preferred_datetime + session_duration
            send_session_completion_email.apply_async(
                (booking.id,),
                eta=make_naive(run_eta, timezone=dt_timezone.utc)  # Fixed for Django 5
            )
            logger.info(f"Scheduled completion email for booking ID {booking.id} at {run_eta}")

            # Send confirmation to mentee (async)
            html_mentee = render_to_string("emails/mentee_confirmation.html", {"booking": booking})
            send_email_task.delay(
                "Mentorship Session Booking Confirmation",
                html_mentee,
                [booking.email],
                settings.DEFAULT_FROM_EMAIL,
            )
            logger.info(f"Queued booking confirmation to mentee: {booking.email}")

            # Send invite to mentor (async)
            mentor_email = getattr(settings, "DEFAULT_MENTOR_EMAIL", "admin@example.com")
            mentor_link = request.build_absolute_uri(
                f"/confirm-session/{booking.mentor_confirmation_token}/"
            )
            html_mentor = render_to_string(
                "emails/mentor_invite.html", {"booking": booking, "mentor_link": mentor_link}
            )
            send_email_task.delay(
                "New Mentorship Session Request",
                html_mentor,
                [mentor_email],
                settings.DEFAULT_FROM_EMAIL,
            )
            logger.info(f"Queued mentor invite email to: {mentor_email}")

            return redirect("core:booking_success")
    else:
        form = LeadershipSessionBookingForm()

    return render(request, "core/booking.html", {"form": form})


@login_required(login_url="accounts:login")
def booking_success_view(request):
    """Booking success page"""
    return render(request, "core/booking_success.html")


@login_required(login_url="accounts:login")
def confirm_session_view(request, token):
    """Mentor confirms session"""
    booking = get_object_or_404(LeadershipSessionBooking, mentor_confirmation_token=token)

    if hasattr(booking, "is_token_valid") and not booking.is_token_valid():
        return HttpResponse("This link has expired. Please request a new confirmation.")

    if booking.is_mentor_confirmed:
        return HttpResponse("This session has already been confirmed.")

    booking.is_mentor_confirmed = True
    booking.confirmed_at = timezone.now()
    booking.save()

    # Notify mentee (async)
    html_content = render_to_string("emails/session_confirmed_mentee.html", {"booking": booking})
    send_email_task.delay(
        "Your Mentorship Session is Confirmed!",
        html_content,
        [booking.email],
        settings.DEFAULT_FROM_EMAIL,
    )
    logger.info(f"Session {booking.id} confirmed by mentor")

    return render(request, "core/mentor_confirmation_msg.html")


def complete_session_view(request, token):
    """Mentee confirms session completion"""
    booking = get_object_or_404(LeadershipSessionBooking, session_completion_token=token)

    if hasattr(booking, "is_token_valid") and not booking.is_token_valid():
        return HttpResponse("This link has expired.")

    if booking.is_session_completed:
        return HttpResponse("Session already marked as completed.")

    booking.is_session_completed = True
    booking.completed_at = timezone.now()
    booking.save()

    return HttpResponse("Thanks for confirming! The session is now marked as completed.")


@login_required(login_url="accounts:login")
def mark_session_held(request, token):
    """Admin marks session as held"""
    booking = get_object_or_404(LeadershipSessionBooking, session_completion_token=token)
    booking.is_session_held = True
    booking.is_session_completed = True
    booking.completed_at = timezone.now()
    booking.save()
    return HttpResponse("Thanks! You've confirmed the session was held.")


@login_required(login_url="accounts:login")
def mark_session_not_held(request, token):
    """Admin marks session as not held"""
    booking = get_object_or_404(LeadershipSessionBooking, session_completion_token=token)
    booking.is_session_held = False
    booking.is_session_completed = False
    booking.completed_at = timezone.now()
    booking.save()
    return HttpResponse("Thanks! You've indicated that the session did not take place.")


def send_message(request):
    """Contact form for general messages"""
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        message_content = request.POST.get("message")

        if full_name and email and message_content:
            five_minutes_ago = timezone.now() - timedelta(minutes=5)
            duplicate = SendMessage.objects.filter(
                email=email, message=message_content, created_at__gte=five_minutes_ago
            ).exists()

            if duplicate:
                messages.error(request, "You've already sent this message recently. Please wait before sending again.")
            else:
                first_name = full_name.split()[0]

                # Save message
                SendMessage.objects.create(full_name=full_name, email=email, message=message_content)

                # Confirmation email to sender (async)
                html_message_user = render_to_string(
                    "emails/confirmation_email.html",
                    {"first_name": first_name, "message": message_content},
                )
                send_email_task.delay(
                    "Thank you for contacting us",
                    html_message_user,
                    [email],
                    settings.DEFAULT_FROM_EMAIL,
                )

                # Notification email to admin (async)
                html_message_admin = render_to_string(
                    "emails/admin_notification_email.html",
                    {"full_name": full_name, "email": email, "message": message_content},
                )
                send_email_task.delay(
                    f"New contact message from {full_name}",
                    html_message_admin,
                    [settings.EMAIL_HOST_USER],
                    settings.DEFAULT_FROM_EMAIL,
                )

                messages.success(request, "Your message has been sent. Please check your email for confirmation.")
        else:
            messages.error(request, "Please fill out all the fields.")

        messages_html = render_to_string("partials/messages.html", {"messages": messages.get_messages(request)})

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return HttpResponse(messages_html)

        return render(request, "core/index.html")

    return render(request, "core/index.html")


def custom_404(request, exception):
    """Custom 404 handler"""
    logger.info("404 at %s", request.build_absolute_uri())
    context = {"path": request.path}
    response = render(request, "404.html", context=context, status=404)
    response["Cache-Control"] = "no-store"
    return response
