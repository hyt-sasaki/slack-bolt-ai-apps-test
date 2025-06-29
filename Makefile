.PHONY: setup install test lint format clean deploy run

# Development setup
setup:
	@echo "🔧 Setting up development environment..."
	./setup.sh

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

install-uv:
	@echo "📦 Installing dependencies with uv..."
	uv sync

# Run tests
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v

test-coverage:
	@echo "🧪 Running tests with coverage..."
	pytest tests/ --cov=app --cov=listeners --cov-report=html

# Linting and formatting
lint:
	@echo "🔍 Linting code..."
	flake8 app/ listeners/ main.py
	mypy app/ listeners/ main.py

format:
	@echo "✨ Formatting code..."
	black app/ listeners/ main.py tests/

format-check:
	@echo "🔍 Checking code formatting..."
	black --check app/ listeners/ main.py tests/

# Run the application
run:
	@echo "🚀 Starting Slack AI Chatbot..."
	python main.py

# Deploy to Cloud Run
deploy:
	@echo "☁️  Deploying to Cloud Run..."
	./deploy.sh

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

# Development with hot reload (requires additional setup)
dev:
	@echo "🔥 Starting development server with hot reload..."
	@echo "Note: This requires watchdog (pip install watchdog)"
	python -c "from watchdog.observers import Observer; from watchdog.events import FileSystemEventHandler; import subprocess; import time; import os; \
	class RestartHandler(FileSystemEventHandler): \
		def __init__(self): self.process = None; self.restart() \
		def on_modified(self, event): \
			if event.src_path.endswith('.py'): self.restart() \
		def restart(self): \
			if self.process: self.process.terminate() \
			self.process = subprocess.Popen(['python', 'main.py']) \
	handler = RestartHandler(); observer = Observer(); observer.schedule(handler, '.', recursive=True); observer.start(); \
	try: \
		while True: time.sleep(1) \
	except KeyboardInterrupt: \
		observer.stop(); handler.process.terminate() \
	observer.join()"

# Help
help:
	@echo "Available commands:"
	@echo "  setup          - Set up development environment"
	@echo "  install        - Install dependencies with pip"
	@echo "  install-uv     - Install dependencies with uv"
	@echo "  test          - Run tests"
	@echo "  test-coverage - Run tests with coverage"
	@echo "  lint          - Lint code"
	@echo "  format        - Format code"
	@echo "  format-check  - Check code formatting"
	@echo "  run           - Start the application"
	@echo "  dev           - Start development server with hot reload"
	@echo "  deploy        - Deploy to Cloud Run"
	@echo "  clean         - Clean up build artifacts"
	@echo "  help          - Show this help message"