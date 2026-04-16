import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from src.logger import setup_logger
from src.calendar_client import CalendarClient
from src.slack_client import SlackClient
from src.formatter import EventFormatter
from src.scheduler import Scheduler

logger = setup_logger(__name__)

def load_environment():
    """環境変数を読み込む"""
    env_file = '.env'
    if not os.path.exists(env_file):
        logger.error(f"{env_file} ファイルが見つかりません")
        logger.info(f"{env_file}.example を参考に {env_file} ファイルを作成してください")
        sys.exit(1)
    
    load_dotenv(env_file)
    logger.info("環境変数読み込み完了")

def run_once():
    """1回のみ実行"""
    try:
        logger.info("=" * 50)
        logger.info("Google Calendar → Slack 送信開始")
        logger.info("=" * 50)
        
        # クライアント初期化
        calendar_client = CalendarClient()
        slack_client = SlackClient()
        
        # カレンダーイベント取得
        events = calendar_client.get_today_events()
        
        # イベント情報を抽出
        formatted_events = [
            calendar_client.get_event_details(event)
            for event in events
        ]
        
        # Slack メッセージ作成
        blocks = EventFormatter.format_events_blocks(formatted_events)
        
        # Slack送信
        slack_client.send_formatted_message(blocks)
        
        logger.info("=" * 50)
        logger.info("実行完了")
        logger.info("=" * 50)
    
    except Exception as e:
        logger.error(f"実行エラー: {e}", exc_info=True)
        sys.exit(1)

def run_scheduler():
    """スケジューラーモードで実行"""
    try:
        logger.info("=" * 50)
        logger.info("スケジューラーモード開始")
        logger.info("=" * 50)
        
        scheduler = Scheduler()
        scheduler.initialize()
        scheduler.schedule_daily_task()
        scheduler.execute_task()  # 起動時に1回実行
        scheduler.start()
        
        logger.info("スケジューラーで待機中... (Ctrl+C で停止)")
        
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("スケジューラー停止")
            scheduler.stop()
    
    except Exception as e:
        logger.error(f"スケジューラーエラー: {e}", exc_info=True)
        sys.exit(1)

def main():
    """メイン処理"""
    load_environment()
    
    # コマンドライン引数をチェック
    if len(sys.argv) > 1 and sys.argv[1] == '--scheduler':
        run_scheduler()
    else:
        run_once()

if __name__ == '__main__':
    main()
