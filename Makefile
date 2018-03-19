PORT ?= 8000
HOST ?= localhost

run-backend:
	cd backend; pipenv run python manage.py runserver $(HOST):$(PORT)

run-frontend:
	cd frontend; HOST=$(HOST) PORT=$(PORT) npm run dev
