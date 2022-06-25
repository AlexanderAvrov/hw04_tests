from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """Класс формы для заполнения публикации поста"""

    class Meta:
        model = Post
        fields = ('text', 'group')
        help_texts = {
            'text': 'Текст новой публикации',
            'group': 'Сообщество к которой относится публикация',
        }
