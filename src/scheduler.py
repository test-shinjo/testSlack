import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from src.logger import setup_logger
from src.calendar_client import CalendarClient
from src.slack_client import SlackClient
from src.formatter import EventFormatter

logger = setup_logger(__name__)

class Scheduler:
    """スケジューラー管理"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.calendar_client = None
        self.slack_client = None
    
    def initialize(self):
        """スケジューラーの初期化"""
        try:
            self.calendar_client = CalendarClient()
            self.slack_client = SlackClient()
            logger.info("スケジューラー初期化成功")
        except Exception as e:
            logger.error(f"スケジューラー初期化エラー: {e}")
            raise
    
    def schedule_daily_task(self):
        """毎日のタスクをスケジュール"""
        schedule_time = os.getenv('SCHEDULE_TIME', '09:00')
        hour, minute = map(int, schedule_time.split(':'))
        
        self.scheduler.add_job(
            self.execute_task,
            CronTrigger(hour=hour, minute=minute),
            id='daily_calendar_task',
            name='Daily Calendar to Slack',
            replace_existing=True
        )
        
        logger.info(f"毎日 {schedule_time} に実行するタスクをスケジュール")
    
    def execute_task(self):
        """タスク実行"""
        try:
            logger.info("タスク実行開始")
            
            # カレンダーイベント取得
            events = self.calendar_client.get_today_events()
            
            # イベント情報を抽出
            formatted_events = [
                self.calendar_client.get_event_details(event)
                for event in events
            ]
            
            # Slack メッセージ作成
            blocks = EventFormatter.format_events_blocks(formatted_events)
            
            # Slack送信
            self.slack_client.send_formatted_message(blocks)
            
            logger.info("タスク実行完了")
        
        except Exception as e:
            logger.error(f"タスク実行エラー: {e}")
            # エラー通知もSlackに送信
            try:
                self.slack_client.send_to_myself(f"❌ エラーが発生しました:\n{str(e)}")
            except:
                pass
    
    def start(self):
        """スケジューラーを開始"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("スケジューラー開始")
    
    def stop(self):
        """スケジューラーを停止"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("スケジューラー停止")
