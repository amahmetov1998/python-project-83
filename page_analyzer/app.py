from flask import Flask

app = Flask(__name__)


@app.route('/')
def func():
    return 'Кира громко перданула'