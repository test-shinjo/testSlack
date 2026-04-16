import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from slack_sdk.errors import SlackApiError
from src.slack_client import SlackClient

class TestSlackClient:
    
    @patch.dict('os.environ', {'SLACK_BOT_TOKEN': 'xoxb-test-token'})
    @patch('src.slack_client.WebClient')
    def test_initialization(self, mock_webclient):
        """初期化テスト"""
        client = SlackClient()
        assert client.client is not None
    
    @patch.dict('os.environ', {})
    def test_initialization_missing_token(self):
        """初期化失敗テスト（トークンなし）"""
        with pytest.raises(ValueError):
            SlackClient()
    
    @patch.dict('os.environ', {'SLACK_BOT_TOKEN': 'xoxb-test-token'})
    @patch('src.slack_client.WebClient')
    def test_send_dm_success(self, mock_webclient):
        """DM送信成功テスト"""
        mock_client = MagicMock()
        mock_webclient.return_value = mock_client
        mock_client.conversations_open.return_value = {'channel': {'id': 'C123'}}
        mock_client.chat_postMessage.return_value = {'ok': True}
        
        client = SlackClient()
        result = client.send_dm('U123', 'Test message')
        
        assert result is True
        mock_client.conversations_open.assert_called_once_with(users=['U123'])
        mock_client.chat_postMessage.assert_called_once()
    
    @patch.dict('os.environ', {'SLACK_BOT_TOKEN': 'xoxb-test-token'})
    @patch('src.slack_client.WebClient')
    def test_send_dm_failure(self, mock_webclient):
        """DM送信失敗テスト"""
        mock_client = MagicMock()
        mock_webclient.return_value = mock_client
        
        error_response = {'error': 'invalid_user_id'}
        mock_client.conversations_open.side_effect = SlackApiError(
            'Invalid user_id', response={'ok': False, 'error': 'invalid_user_id'}
        )
        
        client = SlackClient()
        
        with pytest.raises(SlackApiError):
            client.send_dm('U999', 'Test message')
    
    @patch.dict('os.environ', {'SLACK_BOT_TOKEN': 'xoxb-test-token', 'SLACK_USER_ID': 'U123'})
    @patch('src.slack_client.WebClient')
    def test_send_to_myself(self, mock_webclient):
        """自分にメッセージ送信テスト"""
        mock_client = MagicMock()
        mock_webclient.return_value = mock_client
        mock_client.conversations_open.return_value = {'channel': {'id': 'D123'}}
        mock_client.chat_postMessage.return_value = {'ok': True}
        
        client = SlackClient()
        result = client.send_to_myself('Test message')
        
        assert result is True
