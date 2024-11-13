from pathlib import Path
from typing import List
from src.models.stamp import StampConfig, Stamp
from src.processors.image_processor import ImageProcessor
from src.generators.midjourney import MidjourneyGenerator
import os
from dotenv import load_dotenv

def main():
    """メイン処理"""
    # 環境変数の読み込み
    load_dotenv()
    
    # 設定の初期化
    config = StampConfig()
    
    # 各クラスのインスタンス化
    processor = ImageProcessor(config)
    generator = MidjourneyGenerator(os.getenv("MIDJOURNEY_API_KEY"))
    
    # 入力画像のパス
    base_image = Path("data/input/person.jpg")
    dress_image = Path("data/input/dress.jpg")
    
    # 画像生成
    generated_images = generator.generate_images(base_image, dress_image)
    
    # 画像処理
    for image_path in generated_images:
        processed_image = processor.remove_background(image_path)
        resized_image = processor.resize_image(processed_image)
        # 保存処理など

if __name__ == "__main__":
    main()
