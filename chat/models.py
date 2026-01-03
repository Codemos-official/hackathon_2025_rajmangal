from django.db import models
from django.conf import settings
# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
#     is_phone_verified = models.BooleanField(default=False)
#     is_email_verified = models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.username
    
class ChatGroup(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        # User, on_delete=models.CASCADE, related_name='created_groups'
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_groups'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class GroupMember(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group','user')

class Message(models.Model):
    TARGET_CHOICES = (
        ('user','User'),
        ('group','Group'),
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages'
    )

    target_type = models.CharField(max_length=10, choices=TARGET_CHOICES)

    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='received_messages'
    )

    target_group = models.ForeignKey(
        ChatGroup, null=True, blank=True, on_delete=models.CASCADE
    )

    content = models.TextField(blank=True)

    message_type = models.CharField(
        max_length=20,default='text'
    )    # text, image, file

    created_at = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['target_type']),
            models.Index(fields=['created_at']),
        ]