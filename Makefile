.PHONY: migrate generate-migration

migrate:
	alembic upgrade head

generate-migration:
	alembic revision --autogenerate -m $(msg)