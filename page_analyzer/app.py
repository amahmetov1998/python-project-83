from flask import Flask, render_template, \
    request, redirect, flash, get_flashed_messages, url_for
import os
from page_analyzer.urls import validate, parse, make_request
from page_analyzer.db_requests import create_tables, \
    get_added_data, get_id_by_url, add_data, get_different, \
    get_similar, get_data_by_id, add_check

app = Flask(__name__)
DATABASE_URL = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def main():

    create_tables()

    data = {'url': ''}
    return render_template('main.html', data=data)


@app.post('/urls')
def add_url():
    url = request.form.to_dict()['url']
    errors = validate(url)

    if not errors:
        url = parse(url)

    elif errors['url'] == 'empty':
        flash('Некорректный URL', 'error')
        flash('URL обязателен', 'error')

    elif errors['url'] == 'invalid':
        flash('Некорректный URL', 'error')

    elif errors['url'] == 'too_long':
        flash('URL превышает 255 символов', 'error')

    messages = get_flashed_messages(with_categories=True)

    if messages:
        data = {'url': request.form.to_dict()['url']}
        return render_template('main.html', data=data, messages=messages), 422

    data = get_added_data()

    for elem in data:
        if elem[1] == url:

            url_id = get_id_by_url(url)

            flash('Страница уже существует', 'warning')
            return redirect(url_for('get_url', url_id=url_id))

    add_data(url)

    url_id = get_id_by_url(url)

    flash('Страница успешно добавлена', 'success_add')
    return redirect(url_for('get_url', url_id=url_id))


@app.route('/urls/<int:url_id>')
def get_url(url_id):
    messages = get_flashed_messages(with_categories=True)

    data, info = get_data_by_id(url_id)

    return render_template('url.html', data=data, info=info, messages=messages)


@app.get('/urls')
def get_urls():
    unadded_data = get_different()
    added_data = get_similar()
    data = unadded_data + added_data

    return render_template(
        'urls.html', data=sorted(data,
                                 key=lambda x: x[0],
                                 reverse=True))


@app.post('/urls/<int:url_id>/checks')
def check_urls(url_id):
    response = make_request(url_id)
    if not response:
        return redirect(url_for('get_url', url_id=url_id))

    add_check(response)

    flash('Страница успешно проверена', 'success_check')
    return redirect(url_for('get_url', url_id=url_id))


@app.errorhandler(404)
def not_found(error):
    return render_template('errors.html', error=error), 404
