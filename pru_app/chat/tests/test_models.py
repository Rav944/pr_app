from chat.models import Image, Chat, Message
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

User = get_user_model()

class ImageModelTest(TestCase):

    def test_create_image(self):
        image = Image.objects.create(
            url='https://example.com/image1.jpg',
            title='Test Image',
            description='A test image'
        )
        self.assertEqual(image.url, 'https://example.com/image1.jpg')
        self.assertEqual(image.title, 'Test Image')

    def test_image_with_backup_requires_image_field(self):
        image = Image(
            url='https://example.com/image2.jpg',
            title='Test Image 2',
            description='Another test image',
            backup=True
        )
        with self.assertRaises(ValidationError):
            image.clean()

    def test_image_with_valid_backup(self):
        _ = Image.objects.create(
            url='https://example.com/image3.jpg',
            title='Test Image 3',
            description='Another test image',
            backup=True,
            image='images/test_image.jpg'
        )

    def test_image_str_method(self):
        image = Image.objects.create(
            url='https://example.com/image4.jpg',
            title='Test Image 4',
            description='Another test image'
        )
        self.assertEqual(str(image), 'https://example.com/image4.jpg')


class ChatModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_chat(self):
        chat = Chat.objects.create(user=self.user)
        self.assertEqual(chat.user, self.user)

    def test_chat_str_method(self):
        chat = Chat.objects.create(user=self.user)
        self.assertEqual(str(chat), 'testuser')


class MessageModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.chat = Chat.objects.create(user=self.user)
        self.image = Image.objects.create(
            url='https://example.com/image1.jpg',
            title='Test Image',
            description='A test image'
        )

    def test_create_message_with_image(self):
        message = Message.objects.create(
            chat=self.chat,
            text='This is a test message with an image',
            image=self.image
        )
        self.assertEqual(message.chat, self.chat)
        self.assertEqual(message.text, 'This is a test message with an image')
        self.assertEqual(message.image, self.image)

    def test_create_message_without_image(self):
        message = Message.objects.create(
            chat=self.chat,
            text='This is a test message without an image'
        )
        self.assertEqual(message.chat, self.chat)
        self.assertEqual(message.text, 'This is a test message without an image')
        self.assertIsNone(message.image)

    def test_message_str_method(self):
        message = Message.objects.create(
            chat=self.chat,
            text='This is a test message with an image',
            image=self.image
        )
        self.assertEqual(str(message), f'Message in chat {self.chat.id} - This is a test message with an image')
