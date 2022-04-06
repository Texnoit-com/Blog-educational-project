from http.client import OK
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class StaticURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_static_page(self):
        pages = ['/auth/signup/',
                 '/auth/logout/',
                 '/auth/login/',
                 '/auth/password_reset/']
        for page in pages:
            response = self.guest_client.get(page)
            error_name = f'Ошибка: нет доступа до страницы {page}'
            self.assertEqual(response.status_code, OK, error_name)

    def test_urls_authorized_client(self):
        """Доступ авторизованного пользователя"""
        pages = ['/auth/password_change/',
                 '/auth/password_change/done/']
        for page in pages:
            response = self.authorized_client.get(page)
            error_name = f'Ошибка: нет доступа до страницы {page}'
            self.assertEqual(response.status_code, OK, error_name)

    def test_urls_guest_client_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/auth/logout/': 'users/logged_out.html',
            '/auth/signup/': 'users/signup.html',
            '/auth/login/': 'users/login.html',
            '/auth/password_reset/': 'users/password_reset_form.html'
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                error_name = f'Ошибка: {adress} ожидал шаблон {template}'
                self.assertTemplateUsed(response, template, error_name)

    def test_urls_authorized_client_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/auth/password_change/': 'users/password_change.html',
            '/auth/password_change/done/': 'users/password_change_done.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                error_name = f'Ошибка: {adress} ожидал шаблон {template}'
                self.assertTemplateUsed(response, template, error_name)
