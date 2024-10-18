from django.contrib import admin, messages

from .models import  Chat, Message, Image
from .utils import create_messages_for_chats


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'url', 'created_at', 'backup')
    actions = ['send_images_as_message']

    def send_images_as_message(self, request, queryset):
        """
        Action to send selected images as messages to all chats.
        """
        if not queryset.exists():
            self.message_user(request, "No images selected.", messages.WARNING)
            return

        message_count = create_messages_for_chats(queryset)

        if message_count > 0:
            self.message_user(request, f"Successfully sent {message_count} images to all chats.", messages.SUCCESS)
        else:
            self.message_user(request, "No new messages were created.", messages.WARNING)

    send_images_as_message.short_description = "Send selected images as messages to all chats"



@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user_uuid",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("chat", "text", "created_at", "image")
    search_fields = ("chat__user", "text")