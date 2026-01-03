from django.db import models
from chat import models as chat_md

class ScheduledMessage(models.Model):
    message = models.OneToOneField(
        chat_md.Message, on_delete=models.CASCADE
    )

    scheduled_time = models.DateTimeField()
    is_sent = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['scheduled_time']),
            models.Index(fields=["is_sent"]),
        ]