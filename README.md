<div align="center">

<img src="https://sun9-46.userapi.com/impg/exK1Y6d4v8WOvW24WX9JqqjseC9JuVcPfF8y7Q/6ZLsN-UTPBg.jpg?size=512x512&quality=96&sign=b0b04f76053f9d6befa50f9643ea7f24&type=album" alt="logo" width="150" height="auto" />
<h1>Page Analyzer</h1>

[![Actions Status](https://github.com/amahmetov1998/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/amahmetov1998/python-project-83/actions)
[![run test and linter](https://github.com/amahmetov1998/python-project-83/actions/workflows/main.yml/badge.svg)](https://github.com/amahmetov1998/python-project-83/actions/workflows/main.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/8e3581385c30fa25fc6e/maintainability)](https://codeclimate.com/github/amahmetov1998/python-project-83/maintainability)
</div>

## About
The Page Analyzer is an application based on the Flask framework that analyzes the web-pages for SEO suitability.
It uses the basic principles of building modern sites on the MVC architecture: working with routing, forum handlers and templating, interaction with the database.

## Demo
The demo version of the application: https://python-project-83-production-68b1.up.railway.app/

<img src="https://sun21-1.userapi.com/impg/T1FClBJK87OdmiYJL4qAMU41cQo3uexvJEF7hg/V13taWR8Vyw.jpg?size=1280x613&quality=96&sign=08f7c567121eb25b90cfdcefc8b0e099&type=album" width="auto" height="auto" />

---
## Installation

### Python
Make sure you have the Python version 3.8 or higher:
```
python --version
Python 3.8+
```
### Poetry
The project uses Poetry as a dependency manager. [Install](https://python-poetry.org/docs/#installation) Poetry.

### PostgreSQL
The project uses PostgreSQL as a database. [Download](https://www.postgresql.org/download/) the ready-to-use package.

### Application
Clone repository and install dependencies:
```
git clone https://github.com/amahmetov/python-project-83.git
make install
```
Create `.env` file in the root and add the next variables:
```
DATABASE_URL = postgresql://{provider}://{user}:{password}@{host}:{port}/{db}
SECRET_KEY = '{your secret key}'
```

---

## Usage
Start the gunicorn Flask server:
```
make start
```
The server will be available at http://0.0.0.0:8000.

It is possible to start it local in development mode:
```
make dev
```
The dev server will be available at http://127.0.0.1:5000.

To add a new site, enter address into the form on the home page. The address will be validated and then added to the database.