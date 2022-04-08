from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus

User = get_user_model()


class PostFormTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_create_post(self):
        '''Проверка создания пользователя'''
        user_count = User.objects.count()
        form_data = {'first_name': 'Имя',
                     'last_name': 'Фамилия',
                     'username': 'user-test',
                     'email': "test@ya.ru",
                     'password1': 'pass12345',
                     'password2': 'pass12345'}
        response = self.guest_client.post(reverse('users:signup'),
                                          data=form_data,
                                          follow=True)
        error_name = 'Пользователь не добавлен в базу данных'
        self.assertEqual(User.objects.count(), user_count + 1, error_name)
        self.assertEqual(response.status_code, HTTPStatus.OK)
