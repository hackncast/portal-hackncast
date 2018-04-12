ifdef PORT
	BE_PORT ?= $(PORT)
	FE_PORT ?= $(PORT)
else
	BE_PORT ?= 8000
	FE_PORT ?= 8080
endif
HOST ?= localhost

run-backend:
	cd backend; pipenv run python manage.py runserver $(HOST):$(BE_PORT)

run-frontend:
	cd frontend; HOST=$(HOST) PORT=$(FE_PORT) npm run dev
