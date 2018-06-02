RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

run:
	pipenv run ./manage.py runserver

clean_silk:
	@echo -e $(BLUE)Cleaning SILK log tables...$(NC)
	pipenv run ./manage.py silk_clear_request_log

lint:
	@echo -e $(BLUE)Linting project...$(NC)
	@-flake8 || true

test:
	@echo -e $(BLUE)Testing project...$(NC)
	@pipenv run pytest

coverage:
	@echo -e $(BLUE)Testing project coverage...$(NC)
	@pipenv run pytest --cov . -n 2
