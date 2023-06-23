from flask import Flask, render_template, \
    request, redirect, flash, get_flashed_messages
import psycopg2
import requests
from page_analyzer.config import DATABASE_URL, SECRET_KEY
from page_analyzer.validator import validate
from page_analyzer.parser import parse
from datetime import date
from page_analyzer.constants import INVALID, EMPTY, TOO_LONG

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def main():
    try:
        connect = psycopg2.connect(DATABASE_URL)
        connect.autocommit = True
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

    except Exception as err:
        return err
    url = {'url': ''}

    return render_template('main.html', url=url)


@app.route('/drop')
def main_2():
    try:
        connect = psycopg2.connect(DATABASE_URL)
        connect.autocommit = True
        with connect.cursor() as curs:
            curs.execute(
                '''DROP TABLE IF EXISTS url_checks''')
            curs.execute(
                '''DROP TABLE IF EXISTS urls''')
        return 'True'

    except Exception as err:
        return err


@app.route('/urls', methods=['POST'])
def add_url():
    url_dict = request.form.to_dict()
    errors = validate(url_dict)
    url = url_dict['url']

    if not errors:
        url = parse(url)

    elif errors['url'] == EMPTY:
        flash('Некорректный URL', 'error')
        flash('URL обязателен', 'error')
        messages = get_flashed_messages(with_categories=True)
        return render_template('main.html', url=url, messages=messages)

    elif errors['url'] == INVALID:
        flash('Некорректный URL', 'error')
        messages = get_flashed_messages(with_categories=True)
        return render_template('main.html', url=url, messages=messages)

    elif errors['url'] == TOO_LONG:
        flash('URL превышает 255 символов', 'error')
        messages = get_flashed_messages(with_categories=True)
        return render_template('main.html', url=url, messages=messages)

    try:
        connect = psycopg2.connect(DATABASE_URL)
        with connect.cursor() as curs:
            curs.execute('''
            SELECT * FROM urls;
            ''')
            data = curs.fetchall()

    except Exception as err:
        return err

    for elem in data:
        if elem[1] == url:
            try:
                with connect.cursor() as curs:
                    curs.execute('''
                    SELECT id FROM urls WHERE name=%s;
                    ''', (url,))
                    url_id = curs.fetchone()[0]

            except Exception as err:
                return err

            flash('Страница уже существует', 'warning')
            return redirect(f'/urls/{url_id}')

    try:
        connect = psycopg2.connect(DATABASE_URL)
        connect.autocommit = True
        with connect.cursor() as curs:

            curs.execute('''
            INSERT INTO urls (name, created_at)
            VALUES (%s, %s);
            ''', (url, date.today()))

            curs.execute('''
            SELECT id FROM urls WHERE name=%s
            ''', (url,))
            url_id = curs.fetchone()[0]

    except Exception as err:
        return err

    flash('Страница успешно добавлена', 'success_add')
    return redirect(f'/urls/{url_id}')


@app.get('/urls/<int:url_id>')
def get_url(url_id):
    messages = get_flashed_messages(with_categories=True)

    try:
        connect = psycopg2.connect(DATABASE_URL)
        with connect.cursor() as curs:
            curs.execute('''
            SELECT * FROM urls WHERE id=%s
            ''', (url_id,))
            data = curs.fetchall()

            curs.execute('''
            SELECT * FROM url_checks WHERE url_id=%s
            ''', (url_id,))
            info = curs.fetchall()

    except Exception as err:
        return err

    return render_template('url.html', data=data, info=info, messages=messages)


@app.get('/urls')
def get_urls():
    try:
        connect = psycopg2.connect(DATABASE_URL)
        with connect.cursor() as curs:
            curs.execute('''
            SELECT id, name
            FROM urls
            WHERE NOT EXISTS (SELECT urls.id FROM url_checks WHERE urls.id = url_checks.url_id);''')
            not_added = curs.fetchall()
        with connect.cursor() as curs:
            curs.execute('''
            SELECT url_checks.url_id, urls.name, MAX(url_checks.created_at), url_checks.status_code
            FROM url_checks
            JOIN urls
            ON urls.id = url_checks.url_id
            GROUP BY url_checks.url_id, urls.name, url_checks.status_code
            ORDER BY url_checks.url_id DESC;
            ''')
            added = curs.fetchall()
        data = added + not_added

    except Exception as err:
        return err

    return render_template('urls.html', data=sorted(data, key=lambda x: x[0], reverse=True))


@app.route('/urls/<int:url_id>/checks', methods=['POST'])
def check_urls(url_id):

    try:
        connect = psycopg2.connect(DATABASE_URL)
        connect.autocommit = True
        with connect.cursor() as curs:
            curs.execute('''
            SELECT name FROM urls WHERE id = %s
            ''', (url_id,))
            name = curs.fetchall()[0][0]

    except Exception as err:
        return err

    try:
        status = requests.get(name).status_code
        connect = psycopg2.connect(DATABASE_URL)
        connect.autocommit = True
        with connect.cursor() as curs:
            curs.execute('''
            INSERT INTO url_checks (url_id, status_code, created_at)
            VALUES (%s, %s, %s)
            ''', (url_id, status, date.today(),))
        flash('Страница успешно проверена', 'success_check')
        return redirect(f'/urls/{url_id}')

    except ConnectionError:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(f'/urls/{url_id}')
