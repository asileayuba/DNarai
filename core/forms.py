from django import forms
from .models import LeadershipSessionBooking
import pytz


class LeadershipSessionBookingForm(forms.ModelForm):
    timezone = forms.ChoiceField(
        choices=[(tz, tz) for tz in pytz.common_timezones],
        widget=forms.Select(attrs={"class": "form-select text-black"}),
        label="Timezone",
        required=True,  # or False if optional
    )

    class Meta:
        model = LeadershipSessionBooking
        fields = "__all__"
        widgets = {
            "preferred_datetime": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control text-black",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (
                f"{existing_classes} form-control text-black".strip()
            )
            field.widget.attrs["placeholder"] = field.label
