from flask import Flask, render_template
import psycopq2

app = Flask(__name__)


@app.route('/')
def func():
    return render_template('index.html')
