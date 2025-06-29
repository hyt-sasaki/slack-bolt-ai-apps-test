.PHONY: setup install test lint format clean deploy run

# Development setup
setup:
	@echo "🔧 開発環境をセットアップ中..."
	./setup.sh

# Install dependencies
install:
	@echo "📦 依存関係をインストール中..."
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

install-uv:
	@echo "📦 uv で依存関係をインストール中..."
	uv sync

# Run tests
test:
	@echo "🧪 テストを実行中..."
	pytest tests/ -v

test-coverage:
	@echo "🧪 カバレッジ付きテストを実行中..."
	pytest tests/ --cov=app --cov=listeners --cov-report=html

# Linting and formatting
lint:
	@echo "🔍 コードをリント中..."
	ruff check app/ listeners/ main.py
	mypy app/ listeners/ main.py

format:
	@echo "✨ コードをフォーマット中..."
	ruff format app/ listeners/ main.py tests/

format-check:
	@echo "🔍 コードフォーマットをチェック中..."
	ruff format --check app/ listeners/ main.py tests/

# Run the application
run:
	@echo "🚀 Slack AI チャットボットを起動中..."
	python main.py

# Deploy to Cloud Run
deploy:
	@echo "☁️  Cloud Run にデプロイ中..."
	./deploy.sh

# Clean up
clean:
	@echo "🧹 クリーンアップ中..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

# Development with hot reload (requires additional setup)
dev:
	@echo "🔥 ホットリロード付き開発サーバーを起動中..."
	@echo "注意: watchdog が必要です (pip install watchdog)"
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
	@echo "利用可能なコマンド:"
	@echo "  setup          - 開発環境のセットアップ"
	@echo "  install        - pip で依存関係をインストール"
	@echo "  install-uv     - uv で依存関係をインストール"
	@echo "  test          - テストを実行"
	@echo "  test-coverage - カバレッジ付きテストを実行"
	@echo "  lint          - コードリント"
	@echo "  format        - コードフォーマット"
	@echo "  format-check  - コードフォーマットをチェック"
	@echo "  run           - アプリケーションを起動"
	@echo "  dev           - ホットリロード付き開発サーバーを起動"
	@echo "  deploy        - Cloud Run にデプロイ"
	@echo "  clean         - ビルド成果物をクリーンアップ"
	@echo "  help          - このヘルプメッセージを表示"