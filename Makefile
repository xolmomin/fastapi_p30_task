makemigrations:
	alembic revision -m "initial commit"

migrate:
	alembic upgrade heads

down-migrate:
	alembic downgrade
