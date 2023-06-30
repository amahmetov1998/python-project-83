import requests


def check_url(url):
    status = requests.get(url).status_code
    if status != 200:
        raise requests.RequestException
    return status
