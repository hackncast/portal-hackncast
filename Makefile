ifdef PORT
	BE_PORT ?= $(PORT)
	FE_PORT ?= $(PORT)
else
	BE_PORT ?= 8000
	FE_PORT ?= 8080
endif
HOST ?= localhost

export_api:
	cd backend; pipenv run python manage.py export_api --file ../frontend/src/apiUrls.js

run-backend:
	cd backend; pipenv run python manage.py runserver $(HOST):$(BE_PORT)

run-frontend:
	cd frontend; HOST=$(HOST) PORT=$(FE_PORT) npm run dev
