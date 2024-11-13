import asyncio
from pathlib import Path
import os
from dotenv import load_dotenv
from src.config.messages import STAMP_MESSAGES
from src.models.stamp import StampConfig
from src.processors.image_processor import ImageProcessor
from src.generators.midjourney import MidjourneyGenerator

async def generate_stamps():
    """スタンプ生成のメイン処理"""
    # 環境変数の読み込み
    load_dotenv()
    
    # 設定の初期化
    config = StampConfig()
    
    # 各クラスのインスタンス化
    processor = ImageProcessor(config)
    generator = MidjourneyGenerator(
        discord_token=os.getenv("DISCORD_TOKEN"),
        channel_id=int(os.getenv("DISCORD_CHANNEL_ID"))
    )
    
    # 入力画像のパス
    base_image = Path("data/input/person.jpg")
    dress_image = Path("data/input/dress.jpg")
    
    # 出力ディレクトリの作成
    output_dir = Path("data/output/stamps")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # メッセージごとに画像を生成して処理
    for i, message in enumerate(STAMP_MESSAGES):
        print(f"スタンプ {i+1}/{len(STAMP_MESSAGES)} を生成中...")
        
        # 画像生成
        generated_image = await generator.generate_image(
            base_image,
            dress_image,
            message=message
        )
        
        if generated_image:
            # 背景除去
            processed_image = processor.remove_background(generated_image)
            
            # サイズ調整
            resized_image = processor.resize_image(processed_image)
            
            # テキスト追加
            final_image = processor.add_text_to_image(resized_image, message)
            
            # 保存
            output_path = output_dir / f"stamp_{i+1:02d}.png"
            final_image.save(output_path, "PNG")
            
            print(f"スタンプ {i+1} を保存しました: {output_path}")
        else:
            print(f"スタンプ {i+1} の生成に失敗しました")

def main():
    """エントリーポイント"""
    asyncio.run(generate_stamps())

if __name__ == "__main__":
    main()
