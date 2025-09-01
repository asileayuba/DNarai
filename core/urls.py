from django.urls import path
from . import views
from .views import custom_404

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("booking/", views.booking_view, name="booking"),
    path("booking-success/", views.booking_success_view, name="booking_success"),
    path(
        "confirm-session/<str:token>/",
        views.confirm_session_view,
        name="confirm_session",
    ),
    path(
        "complete-session/<str:token>/held/",
        views.mark_session_held,
        name="mark_session_held",
    ),
    path(
        "complete-session/<str:token>/not-held/",
        views.mark_session_not_held,
        name="mark_session_not_held",
    ),
    path("send_message/", views.send_message, name="send_message"),
    
    # Test-404 -- Remove before deployment
    path('test-404/', lambda request: custom_404(request, None)),
]
