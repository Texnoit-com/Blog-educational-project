from django.contrib.auth import get_user_model
from django.test import TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Group, Post


User = get_user_model()


class PostModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовое описание поста',
            image=cls.uploaded
        )

    def test_models_have_correct_object_names(self):
        '''Проверка длины __str__ post'''
        error_name = f"Вывод не имеет {settings.LEN_OF_POSTS} символов"
        self.assertEqual(self.post.__str__(),
                         self.post.text[:settings.LEN_OF_POSTS],
                         error_name)

    def test_title_label(self):
        '''Проверка заполнения verbose_name'''
        field_verboses = {'text': 'Текст поста',
                          'pub_date': 'Дата публикации',
                          'group': 'Группа',
                          'author': 'Автор',
                          'image': 'Картинка'}
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                error_name = f'Поле {field} ожидало значение {expected_value}'
                self.assertEqual(
                    self.post._meta.get_field(field).verbose_name,
                    expected_value, error_name)

    def test_title_help_text(self):
        '''Проверка заполнения help_text'''
        field_help_texts = {'text': 'Введите текст поста',
                            'group': 'Группа, относительно поста',
                            'image': 'Картинка'}
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                error_name = f'Поле {field} ожидало значение {expected_value}'
                self.assertEqual(
                    self.post._meta.get_field(field).help_text,
                    expected_value, error_name)


class GroupModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Группа',
            slug='Адрес',
            description='описание',
        )

    def test_models_have_correct_title_names(self):
        '''Проверка заполнения str group'''
        group = GroupModelTest.group
        title = group.__str__()
        self.assertEqual(title, group.title)

    def test_title_label(self):
        '''Проверка заполнения verbose_name'''
        group = GroupModelTest.group
        field_verboses = {'title': 'Жанр',
                          'slug': 'Параметр',
                          'description': 'Содержание'}
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name, expected_value)

    def test_title_help_text(self):
        '''Проверка заполнения help_text'''
        group = GroupModelTest.group
        field_help_texts = {'title': 'Укажите жанр',
                            'slug': 'Адрес',
                            'description': 'Содержание'}
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).help_text, expected_value)