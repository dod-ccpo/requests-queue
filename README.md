# requests-queue

## Installation

    script/setup

The setup script installs pipenv, which is what this application uses to manage its dependences and virtualenv. Instead of the classic `requirements.txt` file, pipenv uses a Pipfile and Pipfile.lock, making it more similar to other modern package managers like yarn or mix.

To enter the virtualenv manually (a la `source .venv/bin/activate`):

    pipenv shell

If you want to automatically load the virtual environment whenever you enter the project directory, take a look at [direnv](https://direnv.net/).  An `.envrc` file is included in this repository.  direnv will activate and deactivate virtualenvs for you when you enter and leave the directory.

### Database Setup

The app assumes that you have a local postgres 9.4+ instance running on the default port (5432), with credentials atat/password and database `requests_queue`. If you've installed postgres with `brew install postgres`, run the following:

```
createuser -s atat
psql -c 'create database requests_queue;' -U atat
pipenv run alembic upgrade head
```

## Running (development)

To start the app and watch for changes:

    DEBUG=1 script/server

## Testing

To run unit tests:

    script/test

or

    python -m pytest

## Configuration

The file config/dev.ini can contain a config file that will be
read during testing.  If `FLASK_ENV` is set to something other
than "dev", the `$FLASK_ENV.ini` will be used.  Here is a sample
config file:

    [default]
    DEBUG=true
    AUTORELOAD=true
    REDIS_URL=redis://localhost:6379
    PORT=8889
