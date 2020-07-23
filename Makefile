.PHONY: deploy

migrate:
	alembic upgrade head

generate-migration:
    alembic revision --autogenerate -m $(msg)