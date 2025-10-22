APP=docker compose exec app

migration:
	$(APP) python manage.py makemigrations

migrate:
	$(APP) python manage.py migrate

superuser:
	$(APP) python manage.py createsuperuser

root: 
	docker compose exec -u 0 app

bash:
	$(APP) bash

fmt:
	$(APP) black . 

logs:
	docker compose logs app

test:
	$(APP) python manage.py test

build:
	docker compose build app --no-cache

flushtokens:
	$(APP) python manage.py flushexpiredtokens