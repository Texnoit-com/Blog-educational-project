from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.models import Post, Group, Comment


User = get_user_model()


class PostFormTests(TestCase):

    def setUp(self):
        self.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        self.uploaded = SimpleUploadedFile(name='small.gif',
                                           content=self.small_gif,
                                           content_type='image/gif')
        self.guest_client = Client()
        self.user = User.objects.create_user(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(title='Тестовая группа',
                                          slug='test-group',
                                          description='Описание')

    def test_create_post(self):
        '''Проверка создания поста'''
        posts_count = Post.objects.count()
        form_data = {'text': 'Текст записанный в форму',
                     'group': self.group.id,
                     'image': self.uploaded}
        response = self.authorized_client.post(reverse('posts:post_create'),
                                               data=form_data,
                                               follow=True)
        error_name1 = 'Данные поста не совпадают'
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Post.objects.filter(
                        text='Текст записанный в форму',
                        group=self.group.id,
                        author=self.user
                        ).exists(), error_name1)
        error_name2 = 'Поcт не добавлен в базу данных'
        self.assertEqual(Post.objects.count(),
                         posts_count + 1,
                         error_name2)

    def test_can_edit_post(self):
        '''Проверка прав редактирования'''
        self.post = Post.objects.create(text='Тестовый текст',
                                        author=self.user,
                                        group=self.group,
                                        image=self.uploaded)
        old_text = self.post
        self.group2 = Group.objects.create(title='Тестовая группа2',
                                           slug='test-group2',
                                           description='Описание')
        form_data = {'text': 'Текст записанный в форму',
                     'group': self.group2.id}
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': old_text.id}),
            data=form_data,
            follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error_name1 = 'Данные поста не совпадают'
        self.assertTrue(Post.objects.filter(
                        group=self.group2.id,
                        author=self.user,
                        pub_date=self.post.pub_date
                        ).exists(), error_name1)
        error_name1 = 'Пользователь не может изменить содержание поста'
        self.assertNotEqual(old_text.text, form_data['text'], error_name1)
        error_name2 = 'Пользователь не может изменить группу поста'
        self.assertNotEqual(old_text.group, form_data['group'], error_name2)

    def test_group_null(self):
        '''Проверка что группу можно не указывать'''
        self.post = Post.objects.create(text='Тестовый текст',
                                        author=self.user,
                                        group=self.group,
                                        image=self.uploaded)
        old_text = self.post
        form_data = {'text': 'Текст записанный в форму',
                     'group': ''}
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': old_text.id}),
            data=form_data,
            follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error_name2 = 'Пользователь не может оставить поле нулевым'
        self.assertNotEqual(old_text.group, form_data['group'], error_name2)

    def test_reddirect_guest_client(self):
        '''Проверка редиректа неавторизованного пользователя'''
        self.post = Post.objects.create(text='Тестовый текст',
                                        author=self.user,
                                        group=self.group,
                                        image=self.uploaded)
        form_data = {'text': 'Текст записанный в форму'}
        response = self.guest_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response,
                             f'/auth/login/?next=/posts/{self.post.id}/edit/')

    def test_no_edit_post(self):
        '''Проверка запрета редактирования не авторизованого пользователя'''
        posts_count = Post.objects.count()
        form_data = {'text': 'Текст записанный в форму',
                     'group': self.group.id}
        response = self.guest_client.post(reverse('posts:post_create'),
                                          data=form_data,
                                          follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error_name2 = 'Поcт добавлен в базу данных по ошибке'
        self.assertNotEqual(Post.objects.count(),
                            posts_count + 1,
                            error_name2)


class CommentFormTest(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(title='Тестовая группа',
                                          slug='test-group',
                                          description='Описание')
        self.post = Post.objects.create(text='Тестовый текст',
                                        author=self.user,
                                        group=self.group)
        self.comment = Comment.objects.create(post_id=self.post.id,
                                              author=self.user,
                                              text='Тестовый коммент')

    def test_create_comment(self):
        '''Проверка создания комментария'''
        comment_count = Comment.objects.count()
        form_data = {'post_id': self.post.id,
                     'author': self.user,
                     'text': 'Тестовый коммент2'}
        response = self.authorized_client.post(
                reverse('posts:add_comment',
                        kwargs={'post_id': self.post.id}),
                data=form_data, follow=True)
        error_name1 = 'Данные комментария не совпадают'
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Comment.objects.filter(
                        text='Тестовый коммент2',
                        post=self.post.id,
                        author=self.user
                        ).exists(), error_name1)
        error_name2 = 'Комментарий не добавлен в базу данных'
        self.assertEqual(Comment.objects.count(),
                         comment_count + 1,
                         error_name2)

    def test_no_edit_comment(self):
        '''Проверка запрета комментирования не авторизованого пользователя'''
        posts_count = Comment.objects.count()
        form_data = {'post_id': self.post.id,
                     'author': self.user,
                     'text': 'Тестовый коммент2'}
        response = self.guest_client .post(reverse('posts:add_comment',
                                           kwargs={'post_id': self.post.id}),
                                           data=form_data,
                                           follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error_name2 = 'Комментарий добавлен в базу данных по ошибке'
        self.assertNotEqual(Post.objects.count(),
                            posts_count + 1,
                            error_name2)
