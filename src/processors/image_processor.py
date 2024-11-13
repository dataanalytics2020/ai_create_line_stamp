from pathlib import Path
from typing import List, Optional
from PIL import Image, ImageDraw, ImageFont
from rembg import remove

class ImageProcessor:
    """画像処理を行うクラス"""
    
    def __init__(self, config: 'StampConfig'):
        """
        Args:
            config (StampConfig): スタンプの設定
        """
        self.config = config
        # フォントの設定（M1 Macのデフォルトフォント）
        self.font_path = '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc'
        self.font_size = 24

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

    def add_text_to_image(
        self, 
        image: Image.Image, 
        text: str,
        position: str = 'bottom'
    ) -> Image.Image:
        """画像にテキストを追加する
        
        Args:
            image (Image.Image): 入力画像
            text (str): 追加するテキスト
            position (str): テキストの位置 ('bottom', 'top', 'center')
            
        Returns:
            Image.Image: テキストが追加された画像
        """
        # 作業用のコピーを作成
        img = image.copy()
        draw = ImageDraw.Draw(img)
        
        # フォントの設定
        font = ImageFont.truetype(self.font_path, self.font_size)
        
        # テキストのサイズを取得
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # テキストの位置を計算
        x = (self.config.width - text_width) // 2
        if position == 'bottom':
            y = self.config.height - text_height - 10
        elif position == 'top':
            y = 10
        else:  # center
            y = (self.config.height - text_height) // 2
            
        # 縁取り付きでテキストを描画
        outline_color = 'black'
        text_color = 'white'
        outline_width = 2
        
        # 縁取りを描画
        for adj in range(-outline_width, outline_width+1):
            for adj2 in range(-outline_width, outline_width+1):
                draw.text((x+adj, y+adj2), text, font=font, fill=outline_color)
                
        # メインのテキストを描画
        draw.text((x, y), text, font=font, fill=text_color)
        
        return img
