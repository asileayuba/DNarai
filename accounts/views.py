from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.http import JsonResponse
from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
import random
import uuid

from .models import CustomUser, EmailVerificationToken


# -----------------------------
# Custom Set Password Form
# -----------------------------
class CustomSetPasswordForm(SetPasswordForm):
    """
    Prevents users from setting the same password as their current one.
    """
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if self.user.check_password(password1):
            raise forms.ValidationError(
                _("You cannot use your current password as your new password. Please choose a different one.")
            )
        return password1


# -----------------------------
# Username Helpers
# -----------------------------
def generate_unique_username(first_name, last_name):
    base_username = slugify(f"{first_name}{last_name}")
    username = base_username
    counter = 0
    while CustomUser.objects.filter(username=username).exists():
        counter += 1
        username = f"{base_username}{counter}"
    return username

def suggest_username(base_username):
    for _ in range(5):
        suggestion = f"{base_username}{random.randint(100, 999)}"
        if not CustomUser.objects.filter(username=suggestion).exists():
            return suggestion
    return f"{base_username}{uuid.uuid4().hex[:6]}"


# -----------------------------
# Check username availability
# -----------------------------
def check_username(request):
    username = request.GET.get("username", "").strip().lower()
    if not username:
        return JsonResponse({"available": False, "error": "Username cannot be empty"})
    is_taken = CustomUser.objects.filter(username=username).exists()
    return JsonResponse({"available": not is_taken})


# -----------------------------
# Signup View
# -----------------------------
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")
    
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not username:
            username = generate_unique_username(first_name, last_name)
        else:
            if CustomUser.objects.filter(username=username).exists():
                suggested = suggest_username(username)
                return render(
                    request,
                    "accounts/signup.html",
                    {
                        "error": "Username already taken",
                        "suggested_username": suggested,
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email
                    }
                )

        if CustomUser.objects.filter(email=email).exists():
            return render(request, "accounts/signup.html", {"error": "Email already taken"})

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=False
        )

        send_verification_email(user)
        return render(request, "accounts/email_sent.html", {"email": email})

    return render(request, "accounts/signup.html")


# -----------------------------
# Email Verification
# -----------------------------
def send_verification_email(user):
    existing_token = EmailVerificationToken.objects.filter(user=user, is_used=False).last()
    if existing_token and not existing_token.is_expired():
        return
    token = EmailVerificationToken.objects.create(user=user)
    link = f"{settings.BASE_URL}/accounts/verify-email/{token.token}/"

    subject = "Verify Your Account"
    html_content = render_to_string("accounts/verification_email.html", {"link": link, "user": user})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    email.attach_alternative(html_content, "text/html")
    email.send()


def verify_email(request, token):
    try:
        token_obj = EmailVerificationToken.objects.get(token=token, is_used=False)
    except EmailVerificationToken.DoesNotExist:
        return render(request, "accounts/verification_failed.html", {"error": "Invalid or already used token"})

    if token_obj.is_expired():
        return render(request, "accounts/verification_failed.html", {"error": "Token expired"})

    user = token_obj.user
    user.is_active = True
    user.save()

    token_obj.is_used = True
    token_obj.save()

    login(request, user, backend='accounts.auth_backends.UsernameOrEmailBackend')
    return render(request, "accounts/verification_success.html", {"auto_login": True})


# -----------------------------
# Login View
# -----------------------------
def login_view(request):
    if request.method == "POST":
        # Automatically log out current user if switching accounts
        if request.user.is_authenticated:
            logout(request)

        username_or_email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=username_or_email, password=password)
        if not user:
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user_obj = User.objects.filter(email=username_or_email).first()
                if user_obj:
                    user = authenticate(request, username=user_obj.username, password=password)
            except Exception:
                pass

        if user:
            login(request, user)
            return redirect("core:index")

        return render(request, "accounts/login.html", {
            "error": "Invalid credentials or account not verified"
        })

    return render(request, "accounts/login.html")

# -----------------------------
# Logout View
# -----------------------------
def logout_view(request):
    logout(request)
    return redirect("accounts:login")


# -----------------------------
# Password Reset Request View
# -----------------------------
def user_password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                email_template_name="accounts/password-reset/password_reset_email.html",
                html_email_template_name="accounts/password-reset/password_reset_email.html",
            )
            return redirect("accounts:password_reset_done")
    else:
        form = PasswordResetForm()
    return render(request, "accounts/password-reset/password_reset_form.html", {"form": form})
