.venv:
	@echo "Setting up a virtual environment..."
	@python -m venv .venv

.PHONY: deps
deps: .venv
	@echo "Installing pip dependencies..."
	@(. .venv/bin/activate; pip install -r requirements.txt)

.PHONY: venv
venv: .venv deps

.PHONY: dev-server
dev-server: .venv
	@echo "Starting development server..."
	@(. .venv/bin/activate; python -m app.main)

.PHONY: clean
clean:
	rm -rf .venv
