# Google Calendar → Slack 連携ツール

GoogleカレンダーのイベントをSlackのダイレクトメッセージに自動送信するPythonツール

## 概要

このツールは以下を実現します：
- 毎日指定時間（デフォルト: 9:00）に実行
- Google Calendar の本日のイベント情報を取得
- Slack のダイレクトメッセージに整形して送信

## アーキテクチャ

### 設計方針
- **言語**: Python 3.8+
- **実行方式**: 手動実行 + スケジューラー対応
- **認証**: 環境変数（.env）で管理
- **ロギング**: ファイル＋コンソール出力

### モジュール構成
```
src/
├── main.py          # メインエントリーポイント
├── calendar_client.py   # Google Calendar API ラッパー
├── slack_client.py      # Slack API ラッパー
├── formatter.py         # イベント情報フォーマッター
├── scheduler.py         # スケジューラー処理
└── logger.py            # ロギング設定
```

## 使用技術

### 主要ライブラリ
- **google-api-python-client**: Google Calendar API
- **slack-sdk**: Slack API
- **apscheduler**: ジョブスケジューリング
- **python-dotenv**: 環境変数管理

### 外部API
- Google Calendar API (OAuth 2.0)
- Slack Web API (ボットトークン認証)

## セットアップ

### 1. 環境構築

```bash
# Python 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

### 2. Google Calendar API 設定

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成
3. Google Calendar API を有効化
4. サービスアカウントを作成
5. JSON キーファイルをダウンロード → `credentials.json` として保存

### 3. Slack アプリ設定

1. [Slack App Directory](https://api.slack.com/apps) にアクセス
2. 新しいアプリを作成
3. Bot Token Scopes に以下を追加：
   - `chat:write`
   - `conversations:open`
4. ユーザースコープに `chat:write` を追加
5. ボットトークン（`xoxb-...`）をコピー

### 4. 環境変数の設定

`.env.example` をコピーして `.env` を作成：

```bash
cp .env.example .env
```

`.env` ファイルを編集：

```env
# Google Calendar
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_CALENDAR_ID=primary

# Slack
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_USER_ID=U0123456789  # 自分のユーザーID

# スケジューラー
SCHEDULE_TIME=09:00

# ロギング
LOG_LEVEL=INFO
```

## 使用方法

### 手動実行（1回のみ実行）

```bash
python src/main.py
```

### スケジューラーモード（毎日自動実行）

```bash
python src/main.py --scheduler
```

## ログ

ログは `logs/app.log` に保存されます

## トラブルシューティング

### 認証エラー
- `credentials.json` が正しく配置されているか確認
- `SLACK_BOT_TOKEN` の値が正しいか確認
- `SLACK_USER_ID` が正しいか確認

### イベント取得エラー
- `GOOGLE_CALENDAR_ID` が正しいか確認
- Google Calendar API が有効化されているか確認

### メッセージ送信エラー
- Slack ボットの権限を確認
- DMチャンネルの作成権限があるか確認

## 今後の拡張

- [ ] 複数カレンダーの対応
- [ ] イベントフィルター（特定の予定のみ送信）
- [ ] 複数ユーザーへの送信対応
- [ ] Web UI ダッシュボード
- [ ] メール通知機能
- [ ] Docker 対応

## ライセンス

MIT

## 作成者

GitHub Copilot
