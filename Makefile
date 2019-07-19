
TEST_SUBMISSION_PATH=/media/guillermo/Data/Dropbox/02 Inteligencia Artificial/31_animalai/AnimalAI-Olympics/examples/submission/test_submission

help:
	@echo "test - run tests quickly with the default Python"
	@echo "clean-pyc - remove Python file artifacts"

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

test: clean-pyc
	python setup.py test

env-export:
	conda env export > environment.yml

test-submission:
	docker run -v "$(TEST_SUBMISSION_PATH)":/aaio/test $(DOCKER_IMAGE) python /aaio/test/testDocker.py
