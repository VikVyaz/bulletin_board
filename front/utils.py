import requests
from django.conf import settings


def auth_header(token=None):
    return {'Authorization': f'Bearer {token}'} if token else {}


def res(response):
    if response.status_code in (200, 201, 204):
        try:
            return response.json() if response.content else {'status': 'success'}
        except:
            return {'status': 'success'}
    return {
        'status': 'error',
        'code': response.status_code,
        'message': response.text
    }


def api_get(url, token=None):
    response = requests.get(url, headers=auth_header(token))
    return res(response)


def api_post(url, data, token=None):
    response = requests.post(url, json=data, headers=auth_header(token))
    return res(response)


def api_put(url, data=None, token=None):
    """Полная замена объекта"""
    response = requests.put(url, json=data, headers=auth_header(token))
    return res(response)


def api_patch(url, data=None, token=None):
    """Частичное обновление"""
    response = requests.patch(url, json=data, headers=auth_header(token))
    return res(response)


def api_delete(url, token=None):
    response = requests.delete(url, headers=auth_header(token))
    return res(response)
