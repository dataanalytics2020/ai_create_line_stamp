# AI LINE Stamp Generator

LINEスタンプを自動生成するPythonプロジェクトです。Midjourneyを使用して、人物画像とドレス画像から新しいスタンプ画像を生成します。

## 必要要件

- Python 3.8以上
- M1 Mac
- MidjourneyのAPIキー
- zsh

## セットアップ手順

1. Pythonのインストール:

brew install python@3.9

2. 仮想環境の作成と有効化:

python3.9 -m venv venv
source venv/bin/activate

3. 必要なパッケージのインストール:

pip install -r requirements.txt

4. プロジェクトの構造を作成:

mkdir -p src/{config,generators,processors,models,utils}
mkdir -p data/{input,output}
touch .env

5. 環境変数の設定:
.envファイルを編集し、以下の内容を設定:

MIDJOURNEY_API_KEY=your_api_key_here

## プロジェクト構造

ai_create_line_stamp/
├── .env                    # API keyなどの環境変数
├── requirements.txt        # 必要なパッケージリスト
├── src/
│   ├── config/            # 設定ファイル
│   ├── generators/        # Midjourney API関連
│   ├── processors/        # 画像処理関連
│   ├── models/           # スタンプモデル
│   └── utils/            # ユーティリティ関数
└── data/
    ├── input/            # 入力画像保存用
    └── output/           # 生成された画像保存用

## 使用方法

1. 入力画像の配置:
   - data/input/person.jpg - スタンプにしたい人物の画像を配置
   - data/input/dress.jpg - 参考にしたいドレス画像を配置

入力画像の要件：
- フォーマット: JPG, PNG
- 推奨解像度: 1024x1024px以上
- ファイルサイズ: 5MB以下
- 画像品質: 高品質、ノイズの少ないもの

2. プログラムの実行:

python src/main.py

3. 生成された画像の確認:

open data/output/

## 注意事項

- Midjourneyの利用規約に従って使用してください
- 生成される画像の品質は入力画像の品質に依存します
- LINEスタンプの審査基準に合致するよう、適切な画像を生成してください
- M1 Macでの動作を前提としています

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


