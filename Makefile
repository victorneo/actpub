all:
	uvicorn app:app --reload

test:
	TEST=1 alembic upgrade head
	pytest tests/ --envfile .test.env
	rm testdb.sqlite
