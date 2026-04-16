import os
from typing import Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from src.logger import setup_logger

logger = setup_logger(__name__)

class SlackClient:
    """Slack API ラッパー"""
    
    def __init__(self):
        token = os.getenv('SLACK_BOT_TOKEN')
        if not token:
            raise ValueError("SLACK_BOT_TOKEN 環境変数が設定されていません")
        
        self.client = WebClient(token=token)
        self.user_id = os.getenv('SLACK_USER_ID')
    
    def send_dm(self, user_id: str, message: str) -> bool:
        """ダイレクトメッセージを送信"""
        try:
            # DMチャンネルを開く
            response = self.client.conversations_open(users=[user_id])
            channel_id = response['channel']['id']
            
            # メッセージを送信
            self.client.chat_postMessage(
                channel=channel_id,
                text=message
            )
            logger.info(f"Slack メッセージ送信成功 (ユーザー: {user_id})")
            return True
        
        except SlackApiError as e:
            logger.error(f"Slack API エラー: {e.response['error']}")
            raise
        except Exception as e:
            logger.error(f"メッセージ送信エラー: {e}")
            raise
    
    def send_to_myself(self, message: str) -> bool:
        """自分自身にメッセージを送信"""
        if not self.user_id:
            raise ValueError("SLACK_USER_ID 環境変数が設定されていません")
        return self.send_dm(self.user_id, message)
    
    def send_formatted_message(self, blocks: list) -> bool:
        """フォーマット済みメッセージ（ブロック形式）を送信"""
        try:
            if not self.user_id:
                raise ValueError("SLACK_USER_ID 環境変数が設定されていません")
            
            response = self.client.conversations_open(users=[self.user_id])
            channel_id = response['channel']['id']
            
            self.client.chat_postMessage(
                channel=channel_id,
                blocks=blocks
            )
            logger.info("Slack フォーマット済みメッセージ送信成功")
            return True
        
        except SlackApiError as e:
            logger.error(f"Slack API エラー: {e.response['error']}")
            raise
        except Exception as e:
            logger.error(f"メッセージ送信エラー: {e}")
            raise
