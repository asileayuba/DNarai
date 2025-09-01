from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from django.core.mail.backends.console import EmailBackend as ConsoleBackend

class SMTPAndConsoleBackend:
    """
    Sends emails via SMTP and also prints them to the console.
    Useful for development environments.
    """
    def __init__(self, *args, **kwargs):
        self.smtp_backend = SMTPBackend(*args, **kwargs)
        self.console_backend = ConsoleBackend(*args, **kwargs)

    def send_messages(self, email_messages):
        smtp_sent = self.smtp_backend.send_messages(email_messages)
        self.console_backend.send_messages(email_messages)
        return smtp_sent
