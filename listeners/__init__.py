"""
Package initialization for the listeners module
"""

from .assistant import assistant


def register_listeners(app):
    """アシスタントリスナーを登録する"""
    # アシスタントミドルウェアの使用が推奨方法です
    app.assistant(assistant)