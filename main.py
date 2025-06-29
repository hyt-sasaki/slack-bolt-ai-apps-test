"""
Slack AI Chatbot using Gemini on VertexAI

Google Gemini と VertexAI を使用した Slack AI チャットボットのメインアプリケーションファイルです。
"""

import os
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

from app.gemini_client import GeminiClient
from listeners import register_listeners

# 環境変数を読み込み
load_dotenv()

# ロギング設定
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Slack Bolt アプリを初期化
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Gemini クライアントを初期化
gemini_client = GeminiClient(
    project_id=os.environ.get("GCP_PROJECT_ID"),
    location=os.environ.get("VERTEX_AI_LOCATION", "us-central1"),
    model_name=os.environ.get("VERTEX_AI_MODEL", "gemini-2.5-flash")
)

# Gemini クライアントをアプリコンテキストに保存してリスナーでアクセス可能にする
app.client.gemini = gemini_client

# リスナーを登録
register_listeners(app)

@app.route("/health")
def health_check():
    """Cloud Run 用のヘルスチェックエンドポイント"""
    return {"status": "healthy", "gemini_available": gemini_client.is_available()}

def main():
    """Slack アプリを開始するメイン関数"""
    try:
        # Gemini クライアントが利用可能かチェック
        if not gemini_client.is_available():
            logger.warning("Gemini クライアントが利用できません。Google Cloud の設定を確認してください。")
        
        # 開発用に Socket Mode でアプリを開始
        if os.environ.get("SLACK_APP_TOKEN"):
            handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
            logger.info("Socket Mode で Slack アプリを開始しています...")
            handler.start()
        else:
            # 本番デプロイ用 (例: Cloud Run)
            port = int(os.environ.get("PORT", 3000))
            logger.info(f"ポート {port} で Slack アプリを開始しています...")
            app.start(port=port)
            
    except KeyboardInterrupt:
        logger.info("ユーザーによってアプリが停止されました")
    except Exception as e:
        logger.error(f"アプリ開始エラー: {e}")
        raise

if __name__ == "__main__":
    main()