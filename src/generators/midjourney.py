import discord
from discord.ext import commands
import asyncio
from pathlib import Path
import aiohttp
import os
from typing import Optional
import logging

class MidjourneyGenerator:
    def __init__(self, discord_token: str, channel_id: int):
        """Midjourneyジェネレーターの初期化
        
        Args:
            discord_token (str): Discordボットのトークン
            channel_id (int): MidjourneyボットのあるチャンネルID
        """
        self.token = discord_token
        self.channel_id = channel_id
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.setup_logging()

    def setup_logging(self) -> None:
        """ロギングの設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('MidjourneyGenerator')

    async def wait_for_midjourney_response(self, channel, timeout: int = 120) -> Optional[str]:
        """Midjourneyの応答を待機
        
        Args:
            channel: Discordチャンネル
            timeout (int): タイムアウト時間（秒）
            
        Returns:
            Optional[str]: 生成された画像のURL
        """
        def check(message):
            # Midjourneyからの完了メッセージをチェック
            return (message.channel.id == channel.id and 
                   message.author.id == 936929561302675456 and  # Midjourney Bot ID
                   len(message.attachments) > 0)

        try:
            message = await self.bot.wait_for('message', check=check, timeout=timeout)
            return message.attachments[0].url
        except asyncio.TimeoutError:
            self.logger.error(f"画像生成がタイムアウトしました（{timeout}秒）")
            return None

    async def generate_image(
        self,
        base_image: Path,
        dress_image: Path,
        message: str = ""
    ) -> Optional[Path]:
        """画像を生成
        
        Args:
            base_image (Path): 元となる人物画像
            dress_image (Path): ドレス画像
            message (str): スタンプのメッセージ
            
        Returns:
            Optional[Path]: 生成された画像のパス
        """
        try:
            # Discordにログイン
            await self.bot.start(self.token)
            channel = self.bot.get_channel(self.channel_id)
            
            if not channel:
                self.logger.error(f"チャンネルが見つかりません: {self.channel_id}")
                return None

            # 画像をアップロード
            base_file = discord.File(str(base_image))
            dress_file = discord.File(str(dress_image))
            
            # 参照画像を送信
            await channel.send(files=[base_file, dress_file])
            
            # プロンプトを構築して送信
            emotion = self._analyze_message_emotion(message)
            prompt = self._create_prompt(emotion)
            await channel.send(f"/imagine {prompt}")
            
            # 画像生成の完了を待機
            image_url = await self.wait_for_midjourney_response(channel)
            
            if image_url:
                # 画像をダウンロード
                output_path = Path(f"data/output/temp/midjourney_{message[:10]}.png")
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as resp:
                        if resp.status == 200:
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                            with open(output_path, 'wb') as fd:
                                fd.write(await resp.read())
                            self.logger.info(f"画像を保存しました: {output_path}")
                            return output_path
            
            return None

        except Exception as e:
            self.logger.error(f"画像生成中にエラーが発生しました: {str(e)}")
            return None
        
        finally:
            # Botを終了
            await self.bot.close()

    def _analyze_message_emotion(self, message: str) -> str:
        """メッセージから感情を分析する
        
        Args:
            message (str): 分析するメッセージ
            
        Returns:
            str: 感情カテゴリ（happy, grateful, expectant など）
        """
        # 簡単な感情分析ロジック
        if "ありがとう" in message:
            return "grateful"
        elif "待ってます" in message:
            return "expectant"
        elif "嬉しい" in message:
            return "happy"
        else:
            return "neutral"

    def _create_prompt(
        self, 
        emotion: str
    ) -> str:
        """感情に基づいてプロンプトを生成する
        
        Args:
            emotion (str): 感情カテゴリ
            
        Returns:
            str: 生成用プロンプト
        """
        # 感情に基づくポーズや表情の指定
        emotion_prompts = {
            "grateful": "with a warm grateful smile",
            "expectant": "with a slightly lonely but hopeful expression",
            "happy": "with a bright cheerful smile",
            "neutral": "with a professional elegant pose"
        }
        
        # 基本プロンプトに感情表現を追加
        prompt = f"professional hostess photo, {emotion_prompts.get(emotion, '')}"
        return prompt
