import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from src.calendar_client import CalendarClient

class TestCalendarClient:
    
    @patch('src.calendar_client.os.path.exists')
    @patch('src.calendar_client.service_account.Credentials.from_service_account_file')
    @patch('src.calendar_client.build')
    def test_authentication_success(self, mock_build, mock_creds, mock_exists):
        """認証成功のテスト"""
        mock_exists.return_value = True
        mock_creds.return_value = MagicMock()
        mock_build.return_value = MagicMock()
        
        client = CalendarClient()
        
        assert client.service is not None
        mock_creds.assert_called_once()
    
    @patch('src.calendar_client.os.path.exists')
    @patch('src.calendar_client.service_account.Credentials.from_service_account_file')
    def test_authentication_failure_missing_file(self, mock_creds, mock_exists):
        """認証失敗のテスト（ファイルが見つからない）"""
        mock_exists.return_value = False
        
        with pytest.raises(FileNotFoundError):
            CalendarClient()
    
    @patch('src.calendar_client.os.path.exists')
    @patch('src.calendar_client.service_account.Credentials.from_service_account_file')
    @patch('src.calendar_client.build')
    def test_get_today_events(self, mock_build, mock_creds, mock_exists):
        """本日のイベント取得テスト"""
        mock_exists.return_value = True
        mock_creds.return_value = MagicMock()
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        mock_events = {
            'items': [
                {
                    'summary': 'Test Event 1',
                    'start': {'dateTime': datetime.now().isoformat()},
                    'end': {'dateTime': (datetime.now() + timedelta(hours=1)).isoformat()}
                },
                {
                    'summary': 'Test Event 2',
                    'start': {'dateTime': datetime.now().isoformat()},
                    'end': {'dateTime': (datetime.now() + timedelta(hours=1)).isoformat()}
                }
            ]
        }
        
        mock_service.events().list().execute.return_value = mock_events
        
        client = CalendarClient()
        events = client.get_today_events()
        
        assert len(events) == 2
        assert events[0]['summary'] == 'Test Event 1'
    
    @patch('src.calendar_client.os.path.exists')
    @patch('src.calendar_client.service_account.Credentials.from_service_account_file')
    @patch('src.calendar_client.build')
    def test_get_event_details(self, mock_build, mock_creds, mock_exists):
        """イベント情報抽出テスト"""
        mock_exists.return_value = True
        mock_creds.return_value = MagicMock()
        mock_build.return_value = MagicMock()
        
        event = {
            'summary': 'Meeting',
            'start': {'dateTime': '2026-04-16T09:00:00Z'},
            'end': {'dateTime': '2026-04-16T10:00:00Z'},
            'description': 'Test meeting',
            'location': 'Zoom',
            'attendees': [{'email': 'user1@example.com'}, {'email': 'user2@example.com'}]
        }
        
        client = CalendarClient()
        details = client.get_event_details(event)
        
        assert details['title'] == 'Meeting'
        assert details['description'] == 'Test meeting'
        assert details['location'] == 'Zoom'
        assert details['attendees'] == 2
