## FastAPI Starter

This starter template includes:
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/) for SQLAlchemy + Pydantic models
- [SQLAlchemy](https://www.sqlalchemy.org/) w/ asyncio
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) for migrations
- [ipython](https://ipython.org/)

SQLModel uses Python 3's `typing` by default, so you can consider using it for
the rest of your app as well.

### Installation

This starter template uses sqlite by default for databases. See
[SQLAlchemy Engine Configuration](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls)
to use other databases.

First, create a `.env` file and populate the following variables:

```
DATABASE_URL=<Insert DB String for SQLAlchemy here>
```

Next, install the dependencies and run the initial migration.

```
pip install -r requirements.txt
alembic upgrade head
```

### Running the Tests
Copy the `.env` file to `.test.env` and edit the necessary configuration values
to match your test environment, and then use the following command to run the
tests:

```
make test
```

You will also need to modify the Makefile to match the database you are using.

### Starting the App Server

For development, use the following for autoreloading:

```
uvicorn app:app --reload
```

### Creating a new DB migration

1. Change or add the necessary model definitions in `models/` directory
2. Update the imports in `migrations/env.py` when adding new models or changing model names
3. Run `alembic revision --autogenerate -m "<migration changelog>"`
4. Run `alembic upgrade head`

### License

Copyright 2022 Victor Neo

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.