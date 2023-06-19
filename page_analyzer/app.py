from flask import Flask, render_template, \
    request, redirect, flash, get_flashed_messages
import psycopg2
from page_analyzer.config import DATABASE_URL, SECRET_KEY
from page_analyzer.validator import validate
from page_analyzer.parser import parse
from datetime import date
from page_analyzer.constants import INVALID, EMPTY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def main():
    try:
        connect = psycopg2.connect(DATABASE_URL)
        connect.autocommit = True
        with connect.cursor() as curs:
            curs.execute(
                        'DROP TABLE IF EXISTS urls'
                    )
            curs.execute(
                '''CREATE TABLE urls (
                id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                name VARCHAR(255),
                created_at DATE NOT NULL);'''
            )
    except Exception as err:
        return err
    url = {'url': ''}

    return render_template('main.html', url=url)


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

    try:
        connect = psycopg2.connect(DATABASE_URL)
        with connect.cursor() as curs:
            curs.execute('''
            SELECT * FROM urls;
            '''
                         )
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
            ''', (url, date.today())
                         )

        with connect.cursor() as curs:
            curs.execute('''
            SELECT id FROM urls WHERE name=%s;
            ''', (url,))
            url_id = curs.fetchone()[0]
            # return redirect(url_for('urls', id={curs.fetchone()[0]}))

    except Exception as err:
        return err

    flash('Страница успешно добавлена', 'success')

    return redirect(f'/urls/{url_id}')


@app.get('/urls/<int:url_id>')
def get_url(url_id):
    messages = get_flashed_messages(with_categories=True)

    try:
        connect = psycopg2.connect(DATABASE_URL)
        with connect.cursor() as curs:
            curs.execute('''
            SELECT * FROM urls WHERE id=%s;
            ''', (url_id,))
            data = curs.fetchall()

    except Exception as err:
        return err

    return render_template('url.html', data=data, messages=messages)


@app.get('/urls')
def get_urls():
    try:
        connect = psycopg2.connect(DATABASE_URL)
        with connect.cursor() as curs:
            curs.execute('''
            SELECT * FROM urls ORDER BY id DESC;
            ''')
            data = curs.fetchall()

    except Exception as err:
        return err

    return render_template('urls.html', data=data)
