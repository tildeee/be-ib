# simons-minimal-flask-template

Key assumptions that this scaffolding makes:

- There are two environment variables (accessed in `app/__init__.py`):
    - `SQLALCHEMY_DATABASE_URI`, which holds the connection string for a development database
    - `SQLALCHEMY_TEST_DATABASE_URI`, which holds the connection string for a test database

If a Heroku Procfile existed, with this structure, the best contents would be:

```
web: gunicorn 'app:create_app()'
```
