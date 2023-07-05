<div align="center">

<img src="https://sun9-46.userapi.com/impg/exK1Y6d4v8WOvW24WX9JqqjseC9JuVcPfF8y7Q/6ZLsN-UTPBg.jpg?size=512x512&quality=96&sign=b0b04f76053f9d6befa50f9643ea7f24&type=album" alt="logo" width="150" height="auto" />
<h1>Page Analyzer</h1>

[![Actions Status](https://github.com/amahmetov1998/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/amahmetov1998/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/8e3581385c30fa25fc6e/maintainability)](https://codeclimate.com/github/amahmetov1998/python-project-83/maintainability)
</div>

## About
The page analyzer is an application based on the Flask framework. 
It uses the basic principles of building modern sites on the MVC architecture: working with routing, forum handlers and templating, interaction with the database.

## Demo
The demo version of the application: https://python-project-83-production-68b1.up.railway.app/

<img src="https://sun21-1.userapi.com/impg/T1FClBJK87OdmiYJL4qAMU41cQo3uexvJEF7hg/V13taWR8Vyw.jpg?size=1280x613&quality=96&sign=08f7c567121eb25b90cfdcefc8b0e099&type=album" width="auto" height="auto" />

## Installation

### Python
Make sure you have the Python version 3.8 or higher:
```
>> python --version
Python 3.8+
```

### Poetry
[Install] Poetry.

### PostgreSQL
The project uses PostgreSQL as a database. [Download] the ready-to-use package.

### Application
```
>> git clone https://github.com/amahmetov/python-project-83.git
make install
```
Create .env file in the root and add the next variables:
```
DATABASE_URL = postgresql://{provider}://{user}:{password}@{host}:{port}/{db}
SECRET_KEY = '{your secret key}'
```
Run commands from `database.sql` to create tables.

---