# Slack AI チャットボット with Google Gemini on VertexAI

Slack Bolt for Python と Google の Gemini モデル (VertexAI) を使用した Slack AI チャットボットプロトタイプです。

## 機能

- 🤖 Google Gemini を使った AI 会話機能
- 💬 ダイレクトメッセージ対応
- 📢 チャンネルでのメンション対応
- 🚀 Cloud Run デプロイ対応
- 🛠️ mise と uv を使ったモダンな Python ツール構成
- 🔧 Slack CLI 3.x 統合
- 🎯 Slack Assistant 機能の活用

## アーキテクチャ

- **フレームワーク**: Slack Bolt for Python
- **AI モデル**: Google Gemini on VertexAI
- **デプロイ**: Google Cloud Run
- **ツール管理**: mise
- **パッケージ管理**: uv
- **Slack 管理**: Slack CLI 3.x

## 前提条件

- Python 3.8+
- Google Cloud Platform アカウント
- 管理者権限のある Slack ワークスペース
- mise（オプション、ツール管理用）

## クイックスタート

### 1. 環境セットアップ

```bash
# リポジトリをクローン
git clone <repository-url>
cd slack-bolt-ai-apps-test

# セットアップスクリプトを実行（ツールと依存関係をインストール）
./setup.sh

# または手動セットアップ:
pip install -e ".[dev]"
cp .env.example .env
```

### 2. 環境変数の設定

`.env` ファイルを実際の値で編集:

```bash
# Slack 設定
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_APP_TOKEN=xapp-your-slack-app-token
SLACK_SIGNING_SECRET=your-slack-signing-secret

# Google Cloud 設定
GCP_PROJECT_ID=your-gcp-project-id
GCP_REGION=us-central1

# Vertex AI 設定
VERTEX_AI_LOCATION=us-central1
VERTEX_AI_MODEL=gemini-2.5-flash
```

### 3. Google Cloud セットアップ

```bash
# Google Cloud での認証
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 必要な API を有効化
gcloud services enable aiplatform.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# VertexAI 用のサービスアカウントを作成
gcloud iam service-accounts create slack-ai-chatbot
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:slack-ai-chatbot@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"
```

### 4. Slack アプリセットアップ

Slack CLI 3.x を使用:

```bash
# マニフェストから新しい Slack アプリを作成
slack create app --manifest manifest.json

# アプリをワークスペースにインストール
slack install app
```

### 5. アプリケーションの実行

開発用（Socket Mode）:
```bash
python main.py
```

本番デプロイ用:
```bash
./deploy.sh
```

## 開発

### プロジェクト構造

```
slack-bolt-ai-apps-test/
├── app/
│   ├── __init__.py
│   └── gemini_client.py      # VertexAI Gemini 統合
├── listeners/
│   ├── __init__.py
│   ├── assistant.py          # Slack Assistant リスナー
│   └── message_listener.py   # 従来のメッセージリスナー
├── tests/                    # テストファイル
├── main.py                   # メインアプリケーション
├── manifest.json             # Slack アプリマニフェスト
├── Dockerfile               # コンテナ設定
├── deploy.sh                # Cloud Run デプロイスクリプト
├── setup.sh                 # 開発環境セットアップ
├── pyproject.toml           # Python プロジェクト設定
├── .mise.toml               # ツール設定
└── .env.example             # 環境変数テンプレート
```

### テストの実行

```bash
# 全テストを実行
pytest

# カバレッジ付きで実行
pytest --cov=app --cov=listeners

# 特定のテストファイルを実行
pytest tests/test_gemini_client.py
```

### コード品質

```bash
# コードフォーマット
ruff format .

# コードリント
ruff check .

# 型チェック
mypy .
```

## デプロイ

### Cloud Run デプロイ

1. **ビルドとデプロイ**:
   ```bash
   ./deploy.sh
   ```

2. **環境変数の設定**:
   ```bash
   gcloud run services update slack-ai-chatbot \
     --region=us-central1 \
     --set-env-vars="SLACK_BOT_TOKEN=xoxb-..." \
     --set-env-vars="SLACK_SIGNING_SECRET=..." \
     --set-env-vars="GCP_PROJECT_ID=your-project-id"
   ```

3. **Slack アプリ設定の更新**:
   - リクエスト URL を設定: `https://your-service-url.run.app/slack/events`
   - 本番環境では Socket Mode を無効化

### mise でのツール管理

```bash
# 全ツールをインストール
mise install

# 特定の Slack CLI バージョンを使用
mise use "aqua:slack.com/slack-cli@3.4.0"

# ツールを更新
mise upgrade
```

## 使用方法

### Assistant 機能

このボットは Slack の新しい Assistant 機能を使用しています：

1. **アシスタントスレッドの開始**: ボットとの新しい会話を開始
2. **提案プロンプト**: よく使われる質問の提案
3. **コンテキスト保持**: 会話の文脈を理解した応答

### インタラクションモード

1. **アシスタントスレッド**: Slack の Assistant 機能を使った会話
2. **ダイレクトメッセージ**: ボットに直接メッセージを送信
3. **チャンネルメンション**: チャンネルで `@botname メッセージ` でメンション

### 会話例

```
ユーザー: プログラミングについて教えてください
ボット: プログラミングは、コンピュータに実行させたい処理を...

ユーザー: Pythonの関数について詳しく説明してください
ボット: Pythonの関数は、特定の処理をまとめて名前を付けたもので...
```

## 設定

### 環境変数

| 変数 | 説明 | デフォルト |
|----------|-------------|---------|
| `SLACK_BOT_TOKEN` | ボットユーザーOAuthトークン | 必須 |
| `SLACK_APP_TOKEN` | Socket Mode用アプリレベルトークン | 開発時必須 |
| `SLACK_SIGNING_SECRET` | Slack アプリ署名シークレット | 必須 |
| `GCP_PROJECT_ID` | Google Cloud プロジェクト ID | 必須 |
| `VERTEX_AI_LOCATION` | VertexAI リージョン | `us-central1` |
| `VERTEX_AI_MODEL` | Gemini モデル名 | `gemini-2.5-flash` |
| `PORT` | アプリケーションポート | `3000` |
| `LOG_LEVEL` | ログレベル | `INFO` |

### Slack アプリマニフェスト

`manifest.json` ファイルで以下を設定:
- ボット権限とスコープ
- イベントサブスクリプション
- OAuth 設定
- アプリ表示情報
- Assistant 機能設定

## トラブルシューティング

### よくある問題

1. **Google Cloud のインポートエラー**:
   ```bash
   pip install google-cloud-aiplatform
   ```

2. **認証の問題**:
   ```bash
   gcloud auth application-default login
   ```

3. **Slack トークンの問題**:
   - Slack アプリ設定でトークンを確認
   - トークンの権限とスコープを確認

### ログ

アプリケーションログの確認:
```bash
# ローカル開発
python main.py

# Cloud Run
gcloud logs read --service=slack-ai-chatbot
```

## コントリビューション

1. リポジトリをフォーク
2. フィーチャーブランチを作成
3. テスト付きで変更を作成
4. プルリクエストを送信

## ライセンス

MIT License - 詳細は LICENSE ファイルをご覧ください。
