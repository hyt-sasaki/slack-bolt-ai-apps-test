import logging
from typing import List, Dict
from slack_bolt import Assistant, BoltContext, Say, SetSuggestedPrompts, SetStatus
from slack_bolt.context.get_thread_context import GetThreadContext
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from app.gemini_client import GeminiClient

# Refer to https://tools.slack.dev/bolt-python/concepts/assistant/ for more details
assistant = Assistant()


def call_gemini(
    messages_in_thread: List[Dict[str, str]],
    gemini_client: GeminiClient,
    system_content: str = "あなたはSlackワークスペースのアシスタントです。ユーザーの質問に対して、プロフェッショナルで役立つ回答を日本語で提供してください。"
) -> str:
    """Gemini を使って応答を生成する"""
    try:
        # 最新のユーザーメッセージを取得
        if messages_in_thread:
            latest_message = messages_in_thread[-1]
            if latest_message.get("role") == "user":
                user_message = latest_message.get("content", "")
                return gemini_client.generate_response(user_message)
        
        return "申し訳ございませんが、メッセージを処理できませんでした。"
    except Exception as e:
        logging.error(f"Gemini 応答生成エラー: {e}")
        return "申し訳ございませんが、AI応答の生成中にエラーが発生しました。"


# This listener is invoked when a human user opened an assistant thread
@assistant.thread_started
def start_assistant_thread(
    say: Say,
    get_thread_context: GetThreadContext,
    set_suggested_prompts: SetSuggestedPrompts,
    logger: logging.Logger,
):
    try:
        say("こんにちは！何かお手伝いできることはありますか？")

        prompts: List[Dict[str, str]] = [
            {
                "title": "技術的な質問をする",
                "message": "プログラミングや技術について教えてください",
            },
            {
                "title": "文書の作成を手伝ってもらう",
                "message": "新機能のアナウンス文書を作成したいのですが、手伝ってもらえますか？",
            },
            {
                "title": "アイデアを整理してもらう",
                "message": "プロジェクトのアイデアを整理して、優先順位を付けるのを手伝ってください",
            },
        ]

        thread_context = get_thread_context()
        if thread_context is not None and thread_context.channel_id is not None:
            summarize_channel = {
                "title": "参照チャンネルを要約する",
                "message": "参照されたチャンネルの会話を要約してもらえますか？",
            }
            prompts.append(summarize_channel)

        set_suggested_prompts(prompts=prompts)
    except Exception as e:
        logger.exception(f"アシスタントスレッド開始の処理に失敗しました: {e}", e)
        say(f":warning: エラーが発生しました！ ({e})")


# This listener is invoked when the human user sends a reply in the assistant thread
@assistant.user_message
def respond_in_assistant_thread(
    payload: dict,
    logger: logging.Logger,
    context: BoltContext,
    set_status: SetStatus,
    get_thread_context: GetThreadContext,
    client: WebClient,
    say: Say,
):
    try:
        user_message = payload["text"]
        set_status("入力中...")
        
        # Gemini クライアントを取得
        gemini_client = getattr(client, 'gemini', None)
        if not gemini_client:
            say("申し訳ございませんが、AI サービスが利用できません。")
            return

        if user_message == "参照されたチャンネルの会話を要約してもらえますか？":
            # チャンネル履歴を取得して要約する機能
            thread_context = get_thread_context()
            referred_channel_id = thread_context.get("channel_id")
            try:
                channel_history = client.conversations_history(channel=referred_channel_id, limit=50)
            except SlackApiError as e:
                if e.response["error"] == "not_in_channel":
                    # ボットがパブリックチャンネルにいない場合、チャンネルに参加を試行
                    client.conversations_join(channel=referred_channel_id)
                    channel_history = client.conversations_history(channel=referred_channel_id, limit=50)
                else:
                    raise e

            prompt = f"Slackチャンネル <#{referred_channel_id}> のメッセージを簡潔に要約してください:\n\n"
            for message in reversed(channel_history.get("messages")):
                if message.get("user") is not None:
                    prompt += f"\n<@{message['user']}> の発言: {message['text']}\n"
            
            messages_in_thread = [{"role": "user", "content": prompt}]
            returned_message = call_gemini(messages_in_thread, gemini_client)
            say(returned_message)
            return

        # 通常のスレッド会話を処理
        replies = client.conversations_replies(
            channel=context.channel_id,
            ts=context.thread_ts,
            oldest=context.thread_ts,
            limit=10,
        )
        messages_in_thread: List[Dict[str, str]] = []
        for message in replies["messages"]:
            role = "user" if message.get("bot_id") is None else "assistant"
            messages_in_thread.append({"role": role, "content": message["text"]})
        
        returned_message = call_gemini(messages_in_thread, gemini_client)
        say(returned_message)

    except Exception as e:
        logger.exception(f"ユーザーメッセージの処理に失敗しました: {e}")
        say(f":warning: エラーが発生しました！ ({e})")