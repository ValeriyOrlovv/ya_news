from http import HTTPStatus


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from news.models import Comment, News


User = get_user_model()

class TestRouts(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(title='Заголовок', text='Текст')
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.comment = Comment.objects.create(
            news=cls.news,
            author=cls.author,
            text='Текст комментария'
        )

    def test_pages_availability(self):
        user_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.OK),
        )
        for user , status in user_statuses:
            self.client.force_login(user)
            for name in ('news:edit', 'nes:delete'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.comment.id))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)
        urls = (
            ('news:home', None),
            ('news:detail', (self.news.id,)),
            ('news:login', None),
            ('news:logout', None),
            ('news:signup', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        for name in ('news:edit', 'news:delete')
        with self.subTest(name=name):
            url = reverse(name, )
            redirect_url = f'{login_url}?next={url}'

