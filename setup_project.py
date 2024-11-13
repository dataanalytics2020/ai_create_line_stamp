from pathlib import Path
from typing import Dict, List
import os

def create_directory_structure(base_path: Path) -> None:
    """プロジェクトのディレクトリ構造を作成する
    
    Args:
        base_path (Path): プロジェクトのルートパス
    """
    # 作成するディレクトリのリスト
    directories: List[str] = [
        "src",
        "src/config",
        "src/generators",
        "src/processors",
        "src/models",
        "src/utils",
        "data",
        "data/input",
        "data/output"
    ]
    
    # ディレクトリの作成
    for dir_path in directories:
        full_path = base_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        # 各Pythonパッケージに__init__.pyを作成
        if dir_path.startswith('src'):
            init_file = full_path / '__init__.py'
            init_file.touch()

def create_files(base_path: Path) -> None:
    """必要なファイルを作成する
    
    Args:
        base_path (Path): プロジェクトのルートパス
    """
    # ファイルの内容を定義
    file_contents: Dict[str, str] = {
        '.env': '''MIDJOURNEY_API_KEY=your_api_key_here
''',
        'requirements.txt': '''python-dotenv==1.0.0
Pillow==10.2.0
requests==2.31.0
rembg==2.0.50
numpy==1.26.3
''',
        'src/models/stamp.py': '''from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

@dataclass
class StampConfig:
    """スタンプの設定を管理するクラス"""
    width: int = 370  # LINEスタンプの幅
    height: int = 320  # LINEスタンプの高さ
    num_stamps: int = 20  # 生成するスタンプの数
    output_format: str = "PNG"  # 出力フォーマット

@dataclass
class Stamp:
    """スタンプの情報を管理するクラス"""
    image_path: Path
    processed_path: Optional[Path] = None
    prompt: Optional[str] = None
''',
        'src/processors/image_processor.py': '''from pathlib import Path
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
''',
        'src/generators/midjourney.py': '''from pathlib import Path
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
''',
        'src/main.py': '''from pathlib import Path
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
'''
    }
    
    # ファイルの作成
    for file_path, content in file_contents.items():
        full_path = base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)

def main() -> None:
    """メイン処理"""
    # カレントディレクトリにプロジェクトを作成
    base_path = Path.cwd()
    
    # ディレクトリ構造の作成
    create_directory_structure(base_path)
    
    # ファイルの作成
    create_files(base_path)
    
    print("プロジェクト構造の生成が完了しました！")
    print("次のステップ:")
    print("1. venv環境をアクティベートしてください")
    print("2. pip install -r requirements.txt を実行してください")
    print("3. .envファイルにMidjourneyのAPIキーを設定してください")

if __name__ == "__main__":
    main() 