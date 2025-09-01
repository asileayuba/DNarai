from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomSetPasswordForm 

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("verify-email/<uuid:token>/", views.verify_email, name="verify_email"),
    path("login/", views.login_view, name="login"),
    path("check-username/", views.check_username, name="check_username"),
    path("logout/", views.logout_view, name="logout"),

    # -----------------------------
    # Custom Password Reset Flow
    # -----------------------------
    path(
        "password_reset/",
        views.user_password_reset_request,
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password-reset/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password-reset/password_reset_confirm.html",
            form_class=CustomSetPasswordForm,  # Use custom form here
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password-reset/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
