.PHONY: check
check:
	black .
	ruff check .
	mypy .
	flake8 .


.PHONY: clean
clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -exec rm -rf {} +
	find . -type d -name '.mypy_cache' -exec rm -rf {} +
	find . -type d -name '.ruff_cache' -exec rm -rf {} +
