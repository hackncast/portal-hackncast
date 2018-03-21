RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

clean_silk:
	@echo -e $(BLUE)Cleaning SILK log tables...$(NC)
	pipenv run ./manage.py silk_clear_request_log

lint:
	@echo -e $(BLUE)Linting project...$(NC)
	@-flake8 || true
