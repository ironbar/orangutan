
TEST_SUBMISSION_PATH=/media/guillermo/Data/Dropbox/02 Inteligencia Artificial/31_animalai/orangutan/scripts/test_submission
SAVED_GAMES_PATH=/media/guillermo/Data/Kaggle/animalai/gameplay

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

test: clean-pyc ## run tests quickly with the default Python
	python setup.py test

env-export: ## export conda environment to file
	conda env export > environment.yml

test-submission: ## test that submission works. DOCKER_IMAGE=animalai:001_simple_food_SL make test-submission
	docker run -v "$(TEST_SUBMISSION_PATH)":/aaio/test $(DOCKER_IMAGE) python /aaio/test/testDocker.py

push-submission: ## push submission to evalai. DOCKER_IMAGE=animalai:001_simple_food_SL make push-submission
	evalai push $(DOCKER_IMAGE) --phase animalai-main-396

record-games: ## play games with keyboard and saved them to file. CONFIG_FILEPATH=data/env_configs/1-Food_multi.yaml make record-games |   ENV_SEED=1 CONFIG_FILEPATH=data/env_configs/1-Food_multi.yaml make record-games
	python scripts/record_games/record_games.py "$(CONFIG_FILEPATH)" $(SAVED_GAMES_PATH)

