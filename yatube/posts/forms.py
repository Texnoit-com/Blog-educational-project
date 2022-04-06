from django.forms import ModelForm

from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        help_text = {'text': 'Текст поста',
                     'group': 'Группа',
                     'image': 'Изображение'}


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
