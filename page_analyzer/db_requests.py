import psycopg2
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
connect = psycopg2.connect(DATABASE_URL)
connect.autocommit = True


def create_tables():
    with connect.cursor() as curs:
        curs.execute(
            '''CREATE TABLE IF NOT EXISTS urls (
            id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            name VARCHAR(255),
            created_at DATE NOT NULL);''')

        curs.execute(
            '''CREATE TABLE IF NOT EXISTS url_checks (
            id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            url_id bigint REFERENCES urls (id),
            status_code INTEGER,
            h1 VARCHAR(255),
            title VARCHAR(255),
            description VARCHAR(255),
            created_at DATE);''')


def get_added_data():
    with connect.cursor() as curs:
        curs.execute('''
        SELECT * FROM urls;
        ''')
    data = curs.fetchall()
    return data


def get_id_by_url(url):
    with connect.cursor() as curs:
        curs.execute('''
        SELECT id FROM urls WHERE name=%s;
        ''', (url,))
        url_id = curs.fetchone()[0]
    return url_id


def add_data(url):
    with connect.cursor() as curs:
        curs.execute('''
        INSERT INTO urls (name, created_at)
        VALUES (%s, %s);
        ''', (url, date.today()))


def get_different():
    with connect.cursor() as curs:
        curs.execute('''
        SELECT id, name
        FROM urls
        WHERE NOT EXISTS (SELECT urls.id
                          FROM url_checks
                          WHERE urls.id = url_checks.url_id);''')
        unadded_data = curs.fetchall()
    return unadded_data


def get_data_by_id(url_id):
    with connect.cursor() as curs:
        curs.execute('''
        SELECT * FROM urls WHERE id=%s
        ''', (url_id,))
        data = curs.fetchall()

        curs.execute('''
        SELECT * FROM url_checks WHERE url_id=%s ORDER BY id DESC
        ''', (url_id,))
        info = curs.fetchall()
    return data, info


def get_url_by_id(url_id):
    with connect.cursor() as curs:
        curs.execute('''
        SELECT name FROM urls WHERE id = %s
        ''', (url_id,))
        name = curs.fetchall()[0][0]
    return name


def add_check(response):
    with connect.cursor() as curs:
        curs.execute('''
        INSERT INTO url_checks (url_id, h1, title,
        description, status_code, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (response['url_id'], response['h1'], response['title'],
              response['description'], response['status'], date.today(),))


def get_similar():
    with connect.cursor() as curs:
        curs.execute('''
        SELECT url_checks.url_id, urls.name,
        MAX(url_checks.created_at), url_checks.status_code
        FROM url_checks
        JOIN urls
        ON urls.id = url_checks.url_id
        GROUP BY url_checks.url_id, urls.name, url_checks.status_code
        ORDER BY url_checks.url_id DESC;
        ''')
        added_data = curs.fetchall()
    return added_data
