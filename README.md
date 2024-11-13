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

## スタンプ販売プラットフォーム

### プラットフォーム選択ガイド

会員数に応じた最適なプラットフォームを紹介します：

#### 🔸 少人数での販売（〜100人）
👑 **STORES.jp**がおすすめ
- **手数料**: 
  - 月額980円 + 決済手数料3.6%
- **メリット**:
  - 低コストで開始可能
  - サブスク機能が標準搭載
  - 日本語サポート充実
  - 管理が容易
- **収益例（10人の場合）**:
  ```
  売上: 1,000円 × 10人 = 10,000円/月
  手数料: 360円（3.6%）
  月額: 980円
  手取り: 8,660円/月
  ```
- **損益分岐点**: 2人の会員で黒字化

#### 🔸 中規模での販売（100〜1000人）
👑 **BASE**がおすすめ
- **手数料**: 
  - STANDARDプラン：月額4,980円 + 決済手数料3.6%
- **メリット**:
  - 安定した定期購入システム
  - 自動請求・自動配信
  - 充実した管理機能
  - スマホアプリ対応
- **収益例（500人の場合）**:
  ```
  売上: 1,000円 × 500人 = 50万円/月
  手数料: 1.8万円（3.6%）
  月額: 4,980円
  手取り: 約47.7万円/月
  ```

#### 🔸 大規模での販売（1000人〜）
👑 **Shopify**がおすすめ
- **手数料**: 
  - ADVANCEDプラン：月額79,000円 + 決済手数料2.9%
  - サブスク用アプリ：約10,000円/月
- **メリット**:
  - 高いスケーラビリティ
  - 高度な分析ツール
  - API連携が充実
  - 24時間サポート
  - 多言語・多通貨対応
- **収益例（1万人の場合）**:
  ```
  売上: 1,000円 × 10,000人 = 1,000万円/月
  手数料: 29万円（2.9%）
  月額: 8.9万円（プラン+アプリ）
  手取り: 約961万円/月
  ```

### プラットフォーム選択のポイント

1. **初期段階（〜100人）**
   - 低コストで開始できるSTORES.jp
   - 最小限の機能で運用開始
   - 会員数に応じて段階的に移行

2. **成長段階（100〜1000人）**
   - BASEの充実した機能を活用
   - 会員管理の効率化
   - マーケティング機能の活用

3. **大規模段階（1000人〜）**
   - Shopifyの拡張性を活用
   - データ分析による最適化
   - グローバル展開の可能性

### 補足情報

- **必要な準備**:
  - 本人確認書類
  - 振込口座情報
  - 事業者登録（任意）
  - コンテンツ配信の仕組み

- **運用のポイント**:
  - 会員限定コンテンツの定期配信
  - 会員とのコミュニケーション
  - 解約率の管理
  - コンテンツの品質管理

- **リスク対策**:
  - 会員数が少ない初期は赤字
  - 最低3ヶ月は運用資金を確保
  - 解約率を10%以下に抑える工夫

