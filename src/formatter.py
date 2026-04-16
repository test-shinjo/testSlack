from typing import List, Dict, Any
from datetime import datetime
from src.logger import setup_logger

logger = setup_logger(__name__)

class EventFormatter:
    """イベント情報をSlackメッセージ形式にフォーマット"""
    
    @staticmethod
    def format_event_text(event: Dict[str, Any]) -> str:
        """イベント情報をテキスト形式でフォーマット"""
        title = event.get('title', '(タイトルなし)')
        start = event.get('start', 'N/A')
        end = event.get('end', 'N/A')
        location = event.get('location', '')
        description = event.get('description', '')
        
        text = f"📅 *{title}*\n"
        text += f"⏰ {EventFormatter._format_time(start)} ～ {EventFormatter._format_time(end)}\n"
        
        if location:
            text += f"📍 {location}\n"
        
        if description:
            text += f"📝 {description}\n"
        
        return text
    
    @staticmethod
    def _format_time(time_str: str) -> str:
        """時刻文字列をフォーマット"""
        try:
            if 'T' in time_str:
                dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                return dt.strftime('%H:%M')
            else:
                return time_str
        except:
            return time_str
    
    @staticmethod
    def format_events_text(events: List[Dict[str, Any]]) -> str:
        """複数イベントをテキスト形式でフォーマット"""
        if not events:
            return "📆 本日の予定はありません"
        
        text = f"📆 本日の予定 ({len(events)}件)\n\n"
        for i, event in enumerate(events, 1):
            text += f"{i}. {EventFormatter.format_event_text(event)}\n"
        
        return text
    
    @staticmethod
    def format_events_blocks(events: List[Dict[str, Any]]) -> list:
        """複数イベントをSlack Block Kit 形式でフォーマット"""
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📆 本日の予定 ({len(events)}件)" if events else "📆 本日の予定",
                    "emoji": True
                }
            }
        ]
        
        if not events:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "本日の予定はありません"
                }
            })
        else:
            for event in events:
                blocks.append(EventFormatter._create_event_block(event))
        
        return blocks
    
    @staticmethod
    def _create_event_block(event: Dict[str, Any]) -> Dict[str, Any]:
        """単一イベントのBlockを作成"""
        title = event.get('title', '(タイトルなし)')
        start = EventFormatter._format_time(event.get('start', 'N/A'))
        end = EventFormatter._format_time(event.get('end', 'N/A'))
        location = event.get('location', '')
        
        text = f"*{title}*\n"
        text += f"⏰ {start} ～ {end}"
        if location:
            text += f"\n📍 {location}"
        
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        }
