import pytest
from datetime import datetime
from src.formatter import EventFormatter

class TestEventFormatter:
    
    def test_format_event_text(self):
        """イベント情報テキストフォーマットテスト"""
        event = {
            'title': 'Team Meeting',
            'start': '2026-04-16T14:00:00Z',
            'end': '2026-04-16T15:00:00Z',
            'location': 'Conference Room A',
            'description': 'Weekly sync'
        }
        
        text = EventFormatter.format_event_text(event)
        
        assert 'Team Meeting' in text
        assert 'Conference Room A' in text
        assert 'Weekly sync' in text
    
    def test_format_events_text_empty(self):
        """イベント情報テキストフォーマットテスト（空）"""
        text = EventFormatter.format_events_text([])
        
        assert '本日の予定はありません' in text
    
    def test_format_events_text_multiple(self):
        """複数イベントテキストフォーマットテスト"""
        events = [
            {
                'title': 'Event 1',
                'start': '2026-04-16T09:00:00Z',
                'end': '2026-04-16T10:00:00Z',
                'location': '',
                'description': ''
            },
            {
                'title': 'Event 2',
                'start': '2026-04-16T14:00:00Z',
                'end': '2026-04-16T15:00:00Z',
                'location': 'Location A',
                'description': ''
            }
        ]
        
        text = EventFormatter.format_events_text(events)
        
        assert 'Event 1' in text
        assert 'Event 2' in text
        assert '(2件)' in text
    
    def test_format_events_blocks_empty(self):
        """Block Kit形式（空）テスト"""
        blocks = EventFormatter.format_events_blocks([])
        
        assert len(blocks) == 2
        assert blocks[0]['type'] == 'header'
        assert blocks[1]['type'] == 'section'
        assert '予定はありません' in blocks[1]['text']['text']
    
    def test_format_events_blocks_with_events(self):
        """Block Kit形式テスト"""
        events = [
            {
                'title': 'Standup',
                'start': '2026-04-16T10:00:00Z',
                'end': '2026-04-16T10:30:00Z',
                'location': 'Zoom',
                'description': ''
            }
        ]
        
        blocks = EventFormatter.format_events_blocks(events)
        
        assert len(blocks) >= 2
        assert blocks[0]['type'] == 'header'
        assert 'Standup' in str(blocks)
