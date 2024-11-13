from pathlib import Path
from typing import List, Optional
import requests

class MidjourneyGenerator:
    """Midjourneyを使用して画像を生成するクラス"""
    
    def __init__(self, api_key: str):
        """
        Args:
            api_key (str): Midjourney API key
        """
        self.api_key = api_key

    def generate_images(
        self, 
        base_image: Path, 
        dress_image: Path, 
        num_images: int = 20
    ) -> List[Path]:
        """画像を生成する
        
        Args:
            base_image (Path): 元となる人物画像
            dress_image (Path): ドレス画像
            num_images (int): 生成する画像数
            
        Returns:
            List[Path]: 生成された画像のパスリスト
        """
        # TODO: Midjourney APIの実装
        pass
