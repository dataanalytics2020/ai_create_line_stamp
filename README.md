# AI LINE Stamp Generator

LINEスタンプを自動生成するPythonプロジェクトです。Midjourneyを使用して、人物画像とドレス画像から新しいスタンプ画像を生成します。

## 必要要件

- Python 3.8以上
- M1 Mac
- MidjourneyのAPIキー
- zsh

## セットアップ手順

1. Pythonのインストール:
```
brew install python@3.9
```
2. 仮想環境の作成と有効化:
```
python3.9 -m venv venv
source venv/bin/activate
```
3. 必要なパッケージのインストール:
```
pip install -r requirements.txt
```
4. プロジェクトの構造を作成:
```
mkdir -p src/{config,generators,processors,models,utils}
mkdir -p data/{input,output}
touch .env
```
5. 環境変数の設定:
.envファイルを編集し、以下の内容を設定:
```
MIDJOURNEY_API_KEY=your_api_key_here
```
## プロジェクト構造
```
ai_create_line_stamp/
├── .env                    # API keyなどの環境変数
├── requirements.txt        # 必要なパッケージリスト
├── src/                   # ソースコードディレクトリ
│   ├── __init__.py
│   ├── config/           # 設定ファイル
│   │   └── config.py
│   ├── generators/       # Midjourney API関連
│   │   ├── __init__.py
│   │   └── midjourney.py
│   ├── processors/       # 画像処理関連
│   │   ├── __init__.py
│   │   └── image_processor.py
│   ├── models/          # スタンプモデル
│   │   ├── __init__.py
│   │   └── stamp.py
│   └── utils/           # ユーティリティ関数
│       ├── __init__.py
│       └── helpers.py
└── data/                # データディレクトリ
    ├── input/          # 入力画像保存用
    │   ├── person.jpg
    │   └── dress.jpg
    └── output/         # 生成された画像保存用
        └── stamps/
```
## 使用方法と処理手順

### 基本的な使い方

1. **Discord Botのセットアップ**
   - Discordアプリケーションを作成し、Botトークンを取得
   - MidjourneyボットのあるサーバーにBotを招待
   - .envファイルに以下の内容を設定:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   DISCORD_CHANNEL_ID=your_channel_id
   ```

2. **画像の準備と配置**
   - `data/input/person.jpg` に自分の全身写真を配置
   - `data/input/dress.jpg` に参考にしたいドレス画像を配置

3. **プログラムの実行**
   ```
   python src/main.py
   ```

4. **AIによる画像生成プロセス**
   - Discord APIを使用してMidjourneyと連携
   - 各スタンプのテキストごとに以下の処理を実行:
     1. テキストの感情分析
     2. 感情に合わせたプロンプト生成
     3. Discordチャンネルに画像とプロンプトを送信
     4. Midjourneyからの応答を待機（30-60秒）
     5. 生成された画像をダウンロード
   - 例：
     - 「ありがとう」→ "elegant hostess with a warm grateful smile"
     - 「待ってます」→ "charming hostess with a slightly lonely expression"
     - 「嬉しい」→ "beautiful hostess with a bright cheerful smile"

5. **自動画像処理**
   - 生成された画像の背景が自動で削除されます
   - LINEスタンプサイズ（370x320px）に自動調整されます
   - テキストが画像に追加されます
   - 処理済み画像は `data/output/stamps/` に保存されます

### 画像生成の技術詳細

```
[Discord Bot] ─→ [Midjourneyチャンネル]
      ↓                    ↓
  感情分析            画像生成開始
      ↓                    ↓
プロンプト生成    ←→    生成処理
      ↓                    ↓
  画像ダウンロード  ←─  生成完了通知
      ↓
  画像後処理
```

- **プロンプト生成**: テキストの感情に基づいて最適なプロンプトを自動生成
- **画像生成監視**: Discord WebSocketを使用して生成状態をリアルタイム監視
- **エラーハンドリング**: タイムアウトや生成失敗時の再試行機能
- **非同期処理**: asyncioを使用した効率的な画像生成と処理

### 入力画像の要件

- フォーマット: JPG, PNG
- 推奨解像度: 1024x1024px以上
- ファイルサイズ: 5MB以下
- 画質: 高品質、ノイズの少ないもの

### 処理の流れ
```
[入力画像] → [感情分析] → [AI生成] → [背景除去] → [サイズ調整] → [テキスト追加] → [完成]
person.jpg     ↓            ↓          ↓           ↓            ↓             ↓
dress.jpg → テキスト解析 → 1枚生成 → 透過処理 → 370x320px → メッセージ追加 → stamps/
```

生成された画像は以下のコマンドで確認できます：
```
open data/output/stamps/
```

## トラブルシューティング

1. Python 3.9のインストールエラー:
- Homebrewの更新
- brew update
- brew upgrade
- 再インストール
- brew reinstall python@3.9

2. パッケージのインストールエラー:
- pipの更新
- pip install --upgrade pip
- キャッシュクリア
- pip cache purge

3. venv作成エラー:
- 既存のvenvを削除
- rm -rf venv
- 再作成
- python3.9 -m venv venv

