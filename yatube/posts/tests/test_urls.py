from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from ..models import Post, Group

User = get_user_model()


class PostsUrlTests(TestCase):
    """Тесты для проверки urls приложения Posts"""

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
            id='5',
        )

    def setUp(self):
        # неавторизованный клиент
        self.guest_client = Client()
        # авторизованный клиент
        self.user = User.objects.create_user(username='noname')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        # авторизованный клиент, автор поста
        self.user_author = User.objects.get(username='author')
        self.post_author = Client()
        self.post_author.force_login(self.user_author)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/author/': 'posts/profile.html',
            '/posts/5/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            '/posts/5/edit/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.post_author.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_exists_at_desired_location_authorized(self):
        """Тесты доступности страниц для неавторизованного пользователя"""
        urls = (
            '/',
            '/group/test-slug/',
            '/profile/author/',
            '/posts/5/',
        )
        for url in urls:
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_create_page_exists(self):
        """Тест доступа к /create/ для авторизованного пользователя"""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_edit_page_exists(self):
        """Тест доступа к post_edit для авторизованного пользователя"""
        response = self.post_author.get('/posts/5/edit/')
        self.assertEqual(response.status_code, 200)

    def test_unexisting_page(self):
        """Тест несуществующей страницы"""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)
