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

1. **画像の準備と配置**
   - `data/input/person.jpg` に自分の全身写真を配置
   - `data/input/dress.jpg` に参考にしたいドレス画像を配置

2. **プログラムの実行**
   ```
   python src/main.py
   ```

3. **AIによる画像生成**
   - Midjourneyが人物画像とドレス画像を組み合わせて新しい画像を生成
   - 20枚の異なるバリエーションが自動生成されます
   - 生成には1枚あたり約30-60秒かかります

4. **自動画像処理**
   - 生成された画像の背景が自動で削除されます
   - LINEスタンプサイズ（370x320px）に自動調整されます
   - 処理済み画像は `data/output/stamps/` に保存されます

### 入力画像の要件

- フォーマット: JPG, PNG
- 推奨解像度: 1024x1024px以上
- ファイルサイズ: 5MB以下
- 画質: 高品質、ノイズの少ないもの

### 処理の流れ
```
[入力画像] → [AI生成] → [背景除去] → [サイズ調整] → [完成]
person.jpg     ↓          ↓           ↓            ↓
dress.jpg → 20枚生成 → 透過処理 → 370x320px → stamps/
```

生成された画像は以下のコマンドで確認できます：
```
open data/output/stamps/
```

## 注意事項

- Midjourneyの利用規約に従って使用してください
- 生成される画像の品質は入力画像の品質に依存します
- LINEスタンプの審査基準に合致するよう、適切な画像を生成してください
- M1 Macでの動作を前提としています

## トラブルシューティング
```
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
```

