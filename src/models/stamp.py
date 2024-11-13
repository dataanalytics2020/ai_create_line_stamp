from dataclasses import dataclass
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
