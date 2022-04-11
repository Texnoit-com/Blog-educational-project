from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Comment, Post


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

    def clean_text(self):
        '''Самая примитивная реализация отбора'''
        old_comment = self.cleaned_data['text']
        comment = self.cleaned_data['text']
        regulation = ['Пушкин', 'Лермонтов']
        for element in range(len(regulation)):
            regulation[element] = regulation[element].upper()
        regulation = set(regulation)
        comment = comment.upper()
        comment = set(comment.split(' '))
        if comment.intersection(regulation):
            raise ValidationError("Forbidden word!")
        return old_comment
