from urllib.parse import urlparse


def parse(url: str):
    parse_url = urlparse(url)
    return parse_url.scheme + '://' + parse_url.netloc
