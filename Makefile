SYSTEM_PYTHON_313=python3.13

.venv:
	@echo "Setting up a virtual environment..."
	$(SYSTEM_PYTHON_313) -m venv .venv

.PHONY: deps
deps: .venv
	@echo "Installing pip dependencies..."
	@(. .venv/bin/activate; pip install -r requirements.txt)

.PHONY: venv
venv: .venv deps

.PHONY: dev-server
dev-server: .venv
	@echo "Starting development server..."
	@(. .venv/bin/activate; $(SYSTEM_PYTHON_313) -m app.main)

.PHONY: clean
clean:
	rm -rf .venv
