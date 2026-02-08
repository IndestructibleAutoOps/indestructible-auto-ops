.PHONY: setup lint test run example clean

setup:
	python3 -m pip install -U pip
	python3 -m pip install -e .[dev]

lint:
	python3 -m ruff check src tests
	python3 -m ruff format --check src tests

test:
	python3 -m pytest -q

run:
	python3 -m indestructibleautoops run --config configs/indestructibleautoops.pipeline.yaml --project .

example:
	bash examples/run.sh

clean:
	rm -rf .indestructibleautoops .pytest_cache .ruff_cache dist build *.egg-info