import validators
from urllib.parse import urlparse
import requests
from page_analyzer.db_requests import get_url_by_id
from bs4 import BeautifulSoup
from flask import flash


def validate(url):
    errors = {}
    if not url:
        errors['url'] = 'empty'
    elif not validators.url(url):
        errors['url'] = 'invalid'
    elif len(url) > 255:
        errors['url'] = 'too_long'
    return errors


def parse(url: str):
    parse_url = urlparse(url)
    return f'{parse_url.scheme}://{parse_url.netloc}'


def make_request(url_id):
    name = get_url_by_id(url_id)
    response = {}
    try:
        status = requests.get(name).status_code
        if status != 200:
            raise requests.RequestException

        html = requests.get(name).text
        soup = BeautifulSoup(html, 'lxml')

        response['url_id'] = url_id
        response['status'] = status

        h1 = soup.h1
        if not h1:
            response['h1'] = ''
        else:
            response['h1'] = h1.string

        title = soup.title
        if not title:
            response['title'] = ''
        else:
            response['title'] = title.string

        tag = soup.find('meta', attrs={'name': 'description'})
        if not tag:
            response['description'] = ''
        else:
            response['description'] = tag['content']
        return response

    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'error')
