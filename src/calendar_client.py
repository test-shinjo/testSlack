import os
from typing import List, Dict, Any
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from google_auth_httplib2 import AuthorizedHttp
from googleapiclient.discovery import build
from src.logger import setup_logger

logger = setup_logger(__name__)

class CalendarClient:
    """Google Calendar API ラッパー"""
    
    def __init__(self):
        self.service = None
        self.calendar_id = os.getenv('GOOGLE_CALENDAR_ID', 'primary')
        self._authenticate()
    
    def _authenticate(self):
        """Google Calendar API の認証"""
        try:
            creds_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
            
            if not os.path.exists(creds_file):
                raise FileNotFoundError(f"認証ファイルが見つかりません: {creds_file}")
            
            # サービスアカウント認証
            credentials = service_account.Credentials.from_service_account_file(
                creds_file,
                scopes=['https://www.googleapis.com/auth/calendar.readonly']
            )
            
            self.service = build('calendar', 'v3', credentials=credentials)
            logger.info("Google Calendar API 認証成功")
        
        except FileNotFoundError as e:
            logger.error(f"認証ファイルエラー: {e}")
            raise
        except Exception as e:
            logger.error(f"Google Calendar API 認証エラー: {e}")
            raise
    
    def get_today_events(self) -> List[Dict[str, Any]]:
        """本日のイベント一覧を取得"""
        try:
            now = datetime.utcnow()
            today_start = datetime(now.year, now.month, now.day)
            today_end = today_start + timedelta(days=1)
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=today_start.isoformat() + 'Z',
                timeMax=today_end.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            logger.info(f"本日のイベント取得: {len(events)} 件")
            return events
        
        except Exception as e:
            logger.error(f"イベント取得エラー: {e}")
            raise
    
    def get_event_details(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """イベント情報を抽出"""
        details = {
            'title': event.get('summary', '(タイトルなし)'),
            'start': event.get('start', {}).get('dateTime', event.get('start', {}).get('date')),
            'end': event.get('end', {}).get('dateTime', event.get('end', {}).get('date')),
            'description': event.get('description', ''),
            'location': event.get('location', ''),
            'attendees': len(event.get('attendees', [])),
        }
        return details
