from chat.models import Chat, Image, Message
from chat.utils import create_messages_for_chats
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class CreateMessagesForChatsTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')

        self.chat1 = Chat.objects.create(user=self.user1)
        self.chat2 = Chat.objects.create(user=self.user2)

        self.image1 = Image.objects.create(
            url='https://example.com/image1.jpg',
            title='Test Image 1',
            description='Description for test image 1'
        )
        self.image2 = Image.objects.create(
            url='https://example.com/image2.jpg',
            title='Test Image 2',
            description='Description for test image 2'
        )

    def test_create_messages_for_selected_images(self):
        selected_images = Image.objects.filter(id__in=[self.image1.id, self.image2.id])

        message_count = create_messages_for_chats(selected_images)

        self.assertEqual(Message.objects.count(), 4)
        self.assertEqual(message_count, 4)

    def test_no_duplicate_messages(self):
        Message.objects.create(
            chat=self.chat1,
            text=self.image1.description,
            image=self.image1
        )

        selected_images = Image.objects.filter(id__in=[self.image1.id, self.image2.id])

        message_count = create_messages_for_chats(selected_images)

        self.assertEqual(Message.objects.count(), 4)
        self.assertEqual(message_count, 3)
