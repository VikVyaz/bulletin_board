import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from board.models import Ad, Feedback
from users.models import User


class TestAdAPI:

    def setup_method(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username='test_admin',
            password='1234',
            first_name='test',
            last_name='test',
            phone='test',
            email='test_admin@mail.com',
            role='admin'
        )
        self.user = User.objects.create(
            username='test',
            password='1234',
            first_name='test',
            last_name='test',
            phone='test',
            email='test@mail.com',
            role='user'
        )
        self.client.force_authenticate(user=self.user)

        self.ad = Ad.objects.create(
            title='test_title',
            price=100,
            description='test_description',
            author=self.admin_user
        )
        self.feedback = Feedback.objects.create(
            text='test_text',
            related_ad=self.ad,
            author=self.admin_user
        )

    @pytest.mark.django_db
    def test_1_setup_created(self):
        """Тест создания объектов в setup"""

        assert User.objects.count() == 2
        assert Ad.objects.count() == 1
        assert Feedback.objects.count() == 1
        assert self.ad.author == self.admin_user
        assert self.feedback.author == self.admin_user

    @pytest.mark.django_db
    def test_2_url_create(self):
        """Тест создания через url"""

        ad_url = reverse('board:ad_create')
        new_ad_data = {
            'title': 'new_test',
            'price': 20,
            'description': 'new_description'
        }

        response = self.client.post(ad_url, new_ad_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['title'] == 'new_test'
        assert Ad.objects.filter(title=response.json()['title'])[0].author == self.user

        feedback_url = reverse('board:feedback_create')
        feedback_data = {
            'text': 'text_created',
            'related_ad': self.ad.pk
        }

        response = self.client.post(feedback_url, feedback_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['text'] == 'text_created'
        assert Feedback.objects.filter(text=response.json()['text'])[0].author == self.user

    @pytest.mark.django_db
    def test_3_str(self):
        """Тест str для Ad и Feedback"""

        assert str(self.ad) == 'Объявление №4 - "test_title"'
        assert str(self.feedback) == 'Отзыв №4 на объявление № 4'
        assert str(self.user) == 'Пользователь test test'

    @pytest.mark.django_db
    def test_4_unauth(self):
        """Тест str для Ad и Feedback"""

        self.client.force_authenticate(user=None)

        url = reverse('board:ad_list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        url = reverse('board:ad_create')
        response = self.client.post(url, {
            'title': 'fail',
            'price': 0,
            'description': 'fail'
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        url = reverse('users:user_create')
        response = self.client.post(url, {
            "username": "string",
            "password": "1234",
            "first_name": "string",
            "last_name": "string",
            "phone": "+79091234567",
            "email": "user@example.com",
            "role": "user"
        })
        assert response.status_code == status.HTTP_201_CREATED

        url = reverse('users:user_list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_5_search(self):
        """Тест board:search"""

        url = reverse('board:search')
        response = self.client.get(url, {'title': 'test_title'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    @pytest.mark.django_db
    def test_6_user_perms(self):
        """Тест perms на update/delete Ad/Feedback для role == 'user'"""

        ad_pk = self.ad.pk

        ad_for = ['board:ad_update', 'board:ad_delete', {'title': '123'}]
        feedback_for = ['board:feedback_update', 'board:feedback_delete', {'text': 'text_text'}]

        for data_list in [ad_for, feedback_for]:
            update_ad_url = reverse(data_list[0], args=(ad_pk,))
            delete_ad_url = reverse(data_list[1], args=(ad_pk,))

            update_response = self.client.patch(update_ad_url, data_list[2])
            delete_response = self.client.delete(delete_ad_url)

            assert update_response.status_code == status.HTTP_403_FORBIDDEN
            assert delete_response.status_code == status.HTTP_403_FORBIDDEN
            assert len(Feedback.objects.filter(pk=ad_pk)) == 1
            assert len(Ad.objects.filter(pk=ad_pk)) == 1

    @pytest.mark.django_db
    def test_7_admin_perms(self):
        """Тест perms на update/delete Ad/Feedback для role == 'user'"""

        self.client.force_authenticate(user=self.admin_user)
        test_user = User.objects.create(
            username='test123',
            password='1234',
            first_name='test',
            last_name='test',
            phone='test',
            email='test1234@mail.com',
            role='user'
        )
        test_ad = Ad.objects.create(
            title='test_title',
            price=100,
            description='test_description',
            author=test_user
        )

        update_ad_url = reverse('board:ad_update', args=(test_ad.pk,))
        delete_ad_url = reverse('board:ad_delete', args=(test_ad.pk,))

        update_response = self.client.patch(update_ad_url, {
            'title': '123'
        })
        delete_response = self.client.delete(delete_ad_url)

        assert update_response.status_code == status.HTTP_200_OK
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        assert len(Feedback.objects.filter(pk=test_ad.pk)) == 0
        assert len(Ad.objects.filter(pk=test_ad.pk)) == 0
