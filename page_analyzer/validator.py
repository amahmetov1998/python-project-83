import validators
from page_analyzer.constants import INVALID, EMPTY


def validate(url):
    errors = {}
    if not url['url']:
        errors['url'] = EMPTY
    elif not validators.url(url['url']):
        errors['url'] = INVALID
    return errors
