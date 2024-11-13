from pathlib import Path
from typing import List, Optional
from PIL import Image
from rembg import remove

class ImageProcessor:
    """画像処理を行うクラス"""
    
    def __init__(self, config: 'StampConfig'):
        """
        Args:
            config (StampConfig): スタンプの設定
        """
        self.config = config

    def remove_background(self, image_path: Path) -> Image.Image:
        """背景除去を行う
        
        Args:
            image_path (Path): 入力画像のパス
            
        Returns:
            Image.Image: 背景除去された画像
        """
        input_image = Image.open(image_path)
        return remove(input_image)

    def resize_image(self, image: Image.Image) -> Image.Image:
        """画像をLINEスタンプサイズにリサイズ
        
        Args:
            image (Image.Image): 入力画像
            
        Returns:
            Image.Image: リサイズされた画像
        """
        return image.resize((self.config.width, self.config.height))
