from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from ..models import Post, Group

User = get_user_model()


class PostsPagesTests(TestCase):
    """Проверка вью функций приложения Posts"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Test_group',
            slug='test-slug',
            description='Test_description',
        )
        count = 0
        while count < 13:
            cls.post = Post.objects.create(
                author=cls.user,
                text='Тестовый пост',
                group=cls.group,
            )
            count += 1

    def setUp(self):
        # авторизованный клиент, автор поста
        self.user = User.objects.get(username='author')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """Вью использует правильные шаблоны."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': 'test-slug'}): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': 'author'}): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': '5'}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': '5'}): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index.html сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(post_author_0, 'author')
        self.assertEqual(post_group_0, 'Test_group')

    def test_paginator_posts_pages_contains_ten_records(self):
        """На страницы приложения posts выводится по 10 постов"""
        pages = (
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}),
            reverse('posts:profile', kwargs={'username': 'author'}),
        )
        for reverses in pages:
            with self.subTest(value=reverses):
                response = self.authorized_client.get(reverses)
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_posts_pages_contains_three_records(self):
        """Проверка: на второй странице паджинации должно быть три поста."""
        pages = (
            reverse('posts:index') + '?page=2',
            reverse(
                'posts:group_list',
                kwargs={'slug': 'test-slug'},
            ) + '?page=2',
            reverse(
                'posts:profile',
                kwargs={'username': 'author'},
            ) + '?page=2',
        )
        for reverses in pages:
            with self.subTest(value=reverses):
                response = self.authorized_client.get(reverses)
                self.assertEqual(len(response.context['page_obj']), 3)

    def test_group_page_show_correct_context(self):
        """Шаблон group_list.html сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:group_list',
            kwargs={'slug': 'test-slug'},
        ))
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        second_object = response.context['group']
        group_slug_0 = second_object.slug
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(post_author_0, 'author')
        self.assertEqual(post_group_0, 'Test_group')
        self.assertEqual(group_slug_0, 'test-slug')

    def test_profile_page_show_correct_context(self):
        """Шаблон profile.html сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:profile',
            kwargs={'username': 'author'},
        ))
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        second_object = response.context['author']
        author_username_0 = second_object.username
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(post_author_0, 'author')
        self.assertEqual(post_group_0, 'Test_group')
        self.assertEqual(author_username_0, 'author')

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail.html сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_detail',
            kwargs={'post_id': '5'},
        ))
        first_object = response.context['post']
        post_text = first_object.text
        post_id = first_object.id
        self.assertEqual(post_text, 'Тестовый пост')
        self.assertEqual(post_id, 5)

    def test_create_post_page_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_edit_post_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_edit',
            kwargs={'post_id': '5'}
        ))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        self.assertEqual(response.context['post'].text, 'Тестовый пост')

    def test_group_shows_new_post_on_pages(self):
        """Пост попадает на главную и только в свою группу и профиль автора"""
        self.user = User.objects.create_user(username='new_author')
        self.group = Group.objects.create(title='new_group', slug='new-slug')
        self.post = Post.objects.create(
            author=self.user,
            text='новый пост',
            group=self.group,
            id=135,
        )
        pages = (
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'new-slug'}),
            reverse('posts:profile', kwargs={'username': 'new_author'}),
        )
        for reverses in pages:
            with self.subTest(value=reverses):
                response = self.authorized_client.get(reverses)
                self.assertEqual(
                    response.context.get('page_obj').object_list[0],
                    self.post,
                )
        response = self.authorized_client.get(reverse(
            'posts:group_list',
            kwargs={'slug': 'test-slug'}
        ))
        self.assertNotIn(
            self.post,
            response.context.get('page_obj').object_list,
        )
