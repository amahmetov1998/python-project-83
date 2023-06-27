import validators
from page_analyzer.constants import INVALID, EMPTY, TOO_LONG


def validate(url):
    errors = {}
    if not url:
        errors['url'] = EMPTY
    elif not validators.url(url):
        errors['url'] = INVALID
    elif len(url) > 255:
        errors['url'] = TOO_LONG
    return errors
