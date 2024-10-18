from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()

class Image(models.Model):
    url = models.URLField(max_length=500, help_text="Link to the external image")
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    backup = models.BooleanField(default=False, help_text="Indicates if the image should be backed up locally")
    image = models.ImageField(upload_to='images/', blank=True, null=True, help_text="Local backup of the image")

    def clean(self):
        if self.backup and not self.image:
            raise ValidationError("When backup is True, you must provide a local image file.")

    def __str__(self):
        return self.url or self.image.url

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message in chat {self.chat.id} - {self.text[:50]}"
