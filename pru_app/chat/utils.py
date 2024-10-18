from chat.models import Message, Chat

def create_messages_for_chats(selected_images):
    """
    This utility function creates messages for all chats with the selected images.
    It ensures that the same image is not sent twice to the same chat.
    """
    if not selected_images.exists():
        return 0

    message_count = 0

    for chat in Chat.objects.all():
        for image in selected_images:
            if not Message.objects.filter(chat=chat, image=image).exists():
                Message.objects.create(
                    chat=chat,
                    text=image.description,
                    image=image
                )
                message_count += 1

    return message_count
