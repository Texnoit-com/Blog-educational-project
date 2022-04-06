from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

from core.models import CreatedModel

User = get_user_model()


class Post(CreatedModel):
    text = models.TextField(verbose_name='Текст поста',
                            help_text='Введите текст поста')
    group = models.ForeignKey('Group',
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name='posts',
                              verbose_name='Группа',
                              help_text='Группа, относительно поста')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts',
                               verbose_name='Автор')
    image = models.ImageField(verbose_name='Картинка',
                              upload_to='posts/',
                              blank=True,
                              help_text='Картинка')

    def __str__(self):
        return self.text[:settings.LEN_OF_POSTS]

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date', 'author')


class Group(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Жанр',
                             help_text='Укажите жанр')
    slug = models.SlugField(max_length=255,
                            unique=True,
                            verbose_name='Параметр',
                            help_text='Адрес')
    description = models.TextField(verbose_name='Содержание',
                                   help_text='Содержание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('title',)


class Comment(CreatedModel):
    post = models.ForeignKey('Post',
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Текст поста',
                             blank=True,
                             null=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор')
    text = models.TextField(verbose_name='Комментарий',
                            help_text='Напишите комментарий')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='follower',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='following',
                               on_delete=models.CASCADE)

    class Meta:
        ordering = ['-author']
        verbose_name = 'Лента автора'
        verbose_name_plural = 'Лента авторов'
