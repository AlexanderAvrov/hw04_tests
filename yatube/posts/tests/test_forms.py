from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class FormsTests(TestCase):
    """Проверка форм приложения Posts"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Test_group',
            slug='test-slug',
            description='Test_description',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
        )

    def setUp(self):
        self.user = User.objects.get(username='author')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post_by_authorized_client(self):
        """Валидная форма создает новый пост авторизованным пользователем."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Уникальный текст для проверки форм',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': 'author'},
        ))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(
            Post.objects.filter(text=form_data['text']).get().text,
            form_data['text'],
        )
        self.assertEqual(
            Post.objects.filter(text=form_data['text']).get().group.id,
            form_data['group'],
        )
        self.assertEqual(
            Post.objects.filter(text=form_data['text']).get().author,
            self.user,
        )

    def test_edit_post_form_by_atorized_client(self):
        """Валидная форма изменяет пост от авторизованного автора поста"""
        posts_count = Post.objects.count()
        form_data = {'text': 'Изменённый текст', 'group': self.group.id}
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.id},
        ))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(
            Post.objects.filter(text=form_data['text']).get().text,
            form_data['text'],
        )
        self.assertEqual(
            Post.objects.filter(text=form_data['text']).get().group.id,
            form_data['group'],
        )
        self.assertEqual(
            Post.objects.filter(text=form_data['text']).get().author,
            self.user,
        )
