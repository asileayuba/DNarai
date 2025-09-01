from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _

class CustomSetPasswordForm(SetPasswordForm):
    """
    Extends Django's SetPasswordForm to prevent the new password
    from being the same as the current password.
    """

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        if self.user.check_password(new_password1):
            raise forms.ValidationError(
                _("You cannot use your current password as your new password. Please choose a different one.")
            )
        return new_password1
