import requests
from requests.auth import HTTPBasicAuth


def get_acess_token_bbrasil():
    """developer_application_key = '1684b6826718dfbf3323dd4b5847ddd7'"""

    client_id = 'eyJpZCI6IjMxMmI0MDY3LWU0OTUtNGZmNC04NTY1LTc0MTc2MTdjNjJjNCIsImNvZGlnb1B1YmxpY2Fkb3IiOjAsImNvZGlnb1NvZnR3YXJlIjoxMTQwMTEsInNlcXVlbmNpYWxJbnN0YWxhY2FvIjoxfQ'
    client_secret = 'eyJpZCI6IjlhZGY1ZGQtMzU2YS00MGNmLWJlNTQtZmJjODY3IiwiY29kaWdvUHVibGljYWRvciI6MCwiY29kaWdvU29mdHdhcmUiOjExNDAxMSwic2VxdWVuY2lhbEluc3RhbGFjYW8iOjEsInNlcXVlbmNpYWxDcmVkZW5jaWFsIjoxLCJhbWJpZW50ZSI6ImhvbW9sb2dhY2FvIiwiaWF0IjoxNzI5NzA0MTE5MjU0fQ'
    token_url = 'https://oauth.hm.bb.com.br/oauth/token'
    data = {
        'grant_type': 'client_credentials',
        'scope': 'cob.read cob.write pix.read pix.write'
    }
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic Basic ZXlKcFpDSTZJak14TW1JME1EWTNMV1UwT1RVdE5HWm1OQzA0TlRZMUxUYzBNVGMyTVRkak5qSmpOQ0lzSW1OdlpHbG5iMUIxWW14cFkyRmtiM0lpT2pBc0ltTnZaR2xuYjFOdlpuUjNZWEpsSWpveE1UUXdNVEVzSW5ObGNYVmxibU5wWVd4SmJuTjBZV3hoWTJGdklqb3hmUTpleUpwWkNJNklqbGhaR1kxWkdRdE16VTJZUzAwTUdObUxXSmxOVFF0Wm1Kak9EWTNJaXdpWTI5a2FXZHZVSFZpYkdsallXUnZjaUk2TUN3aVkyOWthV2R2VTI5bWRIZGhjbVVpT2pFeE5EQXhNU3dpYzJWeGRXVnVZMmxoYkVsdWMzUmhiR0ZqWVc4aU9qRXNJbk5sY1hWbGJtTnBZV3hEY21Wa1pXNWphV0ZzSWpveExDSmhiV0pwWlc1MFpTSTZJbWh2Ylc5c2IyZGhZMkZ2SWl3aWFXRjBJam94TnpJNU56QTBNVEU1TWpVMGZR"
    }
    resposta = requests.post(
        url=token_url,
        data=data,
        auth=HTTPBasicAuth(client_id, client_secret),
        headers=header
    )

    return resposta.json()


def get_acess_token_bbradesco():
    """developer_application_key = 'bc72d7a6141fbc85fbc42b05beae87e5'"""
    client_id = 'eyJpZCI6IjIiLCJjb2RpZ29QdWJsaWNhZG9yIjowLCJjb2RpZ29Tb2Z0d2FyZSI6MTEzMzI5LCJzZXF1ZW5jaWFsSW5zdGFsYWNhbyI6MX0'
    client_secret = 'eyJpZCI6ImIzZjEwY2EtOGM0MC00ZWRjLTgwNGUtODY5YzY0NzViYzdlN2Y1NGI5MTAtYzAyOCIsImNvZGlnb1B1YmxpY2Fkb3IiOjAsImNvZGlnb1NvZnR3YXJlIjoxMTMzMjksInNlcXVlbmNpYWxJbnN0YWxhY2FvIjoxLCJzZXF1ZW5jaWFsQ3JlZGVuY2lhbCI6MSwiYW1iaWVudGUiOiJob21vbG9nYWNhbyIsImlhdCI6MTcyOTE5MDY3NTI3NH0'
    token_url = 'https://qrpix-h.bradesco.com.br/oauth/token'
    data = {
        'grant_type': 'client_credentials',
        'scope': 'cob.read cob.write pix.read pix.write'
    }
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic ZXlKcFpDSTZJaklpTENKamIyUnBaMjlRZFdKc2FXTmhaRzl5SWpvd0xDSmpiMlJwWjI5VGIyWjBkMkZ5WlNJNk1URXpNekk1TENKelpYRjFaVzVqYVdGc1NXNXpkR0ZzWVdOaGJ5STZNWDA6ZXlKcFpDSTZJbUl6WmpFd1kyRXRPR00wTUMwMFpXUmpMVGd3TkdVdE9EWTVZelkwTnpWaVl6ZGxOMlkxTkdJNU1UQXRZekF5T0NJc0ltTnZaR2xuYjFCMVlteHBZMkZrYjNJaU9qQXNJbU52WkdsbmIxTnZablIzWVhKbElqb3hNVE16TWprc0luTmxjWFZsYm1OcFlXeEpibk4wWVd4aFkyRnZJam94TENKelpYRjFaVzVqYVdGc1EzSmxaR1Z1WTJsaGJDSTZNU3dpWVcxaWFXVnVkR1VpT2lKb2IyMXZiRzluWVdOaGJ5SXNJbWxoZENJNk1UY3lPVEU1TURZM05USTNOSDA="
    }
    resposta = requests.post(
        url=token_url,
        data=data,
        auth=HTTPBasicAuth(client_id, client_secret),
        headers=header
    )

    return print(resposta.json())


def get_acess_token_bsantander():
    """developer_application_key = 'bc72d7a6141fbc85fbc42b05beae87e5'"""
    client_id = 'Ms762q1PO7pDFlGOU8bJGYYl6ycAi2gw'
    client_secret = 'gtqI790K0BdTUhSd'
    token_url = 'https://pix.santander.com.br/sandbox/oauth/token'
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        'grant_type': 'client_credentials'
    }
    data = {
        'client_id': client_id,
        'client_secret': client_secret
    }
    resposta = requests.post(
        url=token_url,
        data=data,
        headers=header,
        params=params
    )

    return resposta.json()

