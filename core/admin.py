from django.contrib import admin
from .models import (
    SessionType,
    SessionDuration,
    SessionFormat,
    LeadershipSessionBooking,
    SendMessage,
)


class SessionTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


class SessionDurationAdmin(admin.ModelAdmin):
    list_display = ("label",)


class SessionFormatAdmin(admin.ModelAdmin):
    list_display = ("name",)


class LeadershipSessionBookingAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "session_type",
        "session_duration",
        "session_format",
        "goals",
        "created_at",
    )
    readonly_fields = (
        "mentor_confirmation_token",
        "session_completion_token",
        "confirmed_at",
        "completed_at",
    )


class SendMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "created_at")
    readonly_fields = ("full_name", "email", "message", "created_at")
    ordering = ("-created_at",)


admin.site.register(SessionType, SessionTypeAdmin)
admin.site.register(SessionDuration, SessionDurationAdmin)
admin.site.register(SessionFormat, SessionFormatAdmin)
admin.site.register(LeadershipSessionBooking, LeadershipSessionBookingAdmin)
admin.site.register(SendMessage, SendMessageAdmin)
