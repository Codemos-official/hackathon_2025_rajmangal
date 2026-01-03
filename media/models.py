from django.db import models
from chat import models as chat_md

class MediaFile(models.Model):
    message = models.OneToOneField(
    chat_md.Message, on_delete=models.CASCADE, related_name='media'
    )

    file = models.FileField(upload_to='chat_media/')
    file_type = models.CharField(max_length=20) # image/ file
    uploaded_at = models.DateTimeField(auto_now_add=True)