import logging
from typing import Union
from aiogram import Bot
from aiogram.types import Message, ContentType
from database import Database

logger = logging.getLogger(__name__)


class MessageHandler:
    
    def __init__(self, bot: Bot, database: Database, channel_id: str):
        self.bot = bot
        self.db = database
        self.channel_id = channel_id
    
    async def handle_user_message(self, message: Message):
        try:
            channel_message = await self._forward_to_channel(message)
            
            if channel_message:
                await self.db.save_message_mapping(
                    user_id=message.from_user.id,
                    user_message_id=message.message_id,
                    channel_message_id=channel_message.message_id
                )
                
                await message.answer("✅ Ваше сообщение отправлено в канал!")
                
                logger.info(f"Сообщение от пользователя {message.from_user.id} переслано в канал")
            else:
                await message.answer("❌ Не удалось отправить сообщение в канал")
                
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщения пользователя: {e}")
            await message.answer("❌ Произошла ошибка при обработке вашего сообщения")
    
    async def _forward_to_channel(self, message: Message) -> Union[Message, None]:
        try:
            content_type = message.content_type
            
            if content_type == ContentType.TEXT:
                return await self.bot.send_message(
                    chat_id=self.channel_id,
                    text=f"👤 Сообщение от пользователя {message.from_user.first_name}:\n\n{message.text}"
                )
            
            elif content_type == ContentType.PHOTO:
                caption = f"👤 Фото от пользователя {message.from_user.first_name}"
                if message.caption:
                    caption += f"\n\n{message.caption}"
                
                return await self.bot.send_photo(
                    chat_id=self.channel_id,
                    photo=message.photo[-1].file_id,
                    caption=caption
                )
            
            elif content_type == ContentType.VIDEO:
                caption = f"👤 Видео от пользователя {message.from_user.first_name}"
                if message.caption:
                    caption += f"\n\n{message.caption}"
                
                return await self.bot.send_video(
                    chat_id=self.channel_id,
                    video=message.video.file_id,
                    caption=caption
                )
            
            elif content_type == ContentType.DOCUMENT:
                caption = f"👤 Документ от пользователя {message.from_user.first_name}"
                if message.caption:
                    caption += f"\n\n{message.caption}"
                
                return await self.bot.send_document(
                    chat_id=self.channel_id,
                    document=message.document.file_id,
                    caption=caption
                )
            
            elif content_type == ContentType.VOICE:
                return await self.bot.send_voice(
                    chat_id=self.channel_id,
                    voice=message.voice.file_id,
                    caption=f"👤 Голосовое сообщение от пользователя {message.from_user.first_name}"
                )
            
            elif content_type == ContentType.AUDIO:
                caption = f"👤 Аудио от пользователя {message.from_user.first_name}"
                if message.caption:
                    caption += f"\n\n{message.caption}"
                
                return await self.bot.send_audio(
                    chat_id=self.channel_id,
                    audio=message.audio.file_id,
                    caption=caption
                )
            
            else:
                return await self.bot.send_message(
                    chat_id=self.channel_id,
                    text=f"👤 Неподдерживаемый тип контента от пользователя {message.from_user.first_name}"
                )
                
        except Exception as e:
            logger.error(f"Ошибка при пересылке в канал: {e}")
            return None
    
    async def handle_channel_reply(self, message: Message):
        try:
            if not message.reply_to_message:
                return
            
            replied_message_id = message.reply_to_message.message_id
            
            user_id = await self.db.get_user_by_channel_message(replied_message_id)
            
            if not user_id:
                logger.warning(f"Не найден пользователь для сообщения {replied_message_id}")
                return
            
            await self._forward_reply_to_user(message, user_id)
            
            logger.info(f"Ответ из канала переслан пользователю {user_id}")
            
        except Exception as e:
            logger.error(f"Ошибка при обработке ответа из канала: {e}")
    
    async def _forward_reply_to_user(self, message: Message, user_id: int):
        try:
            content_type = message.content_type
            
            if content_type == ContentType.TEXT:
                await self.bot.send_message(
                    chat_id=user_id,
                    text=f"📢 Ответ из канала:\n\n{message.text}"
                )
            
            elif content_type == ContentType.PHOTO:
                caption = "📢 Ответ из канала"
                if message.caption:
                    caption += f"\n\n{message.caption}"
                
                await self.bot.send_photo(
                    chat_id=user_id,
                    photo=message.photo[-1].file_id,
                    caption=caption
                )
            
            elif content_type == ContentType.VIDEO:
                caption = "📢 Ответ из канала"
                if message.caption:
                    caption += f"\n\n{message.caption}"
                
                await self.bot.send_video(
                    chat_id=user_id,
                    video=message.video.file_id,
                    caption=caption
                )
            
            elif content_type == ContentType.DOCUMENT:
                caption = "📢 Ответ из канала"
                if message.caption:
                    caption += f"\n\n{message.caption}"
                
                await self.bot.send_document(
                    chat_id=user_id,
                    document=message.document.file_id,
                    caption=caption
                )
            
            elif content_type == ContentType.VOICE:
                await self.bot.send_voice(
                    chat_id=user_id,
                    voice=message.voice.file_id,
                    caption="📢 Ответ из канала"
                )
            
            elif content_type == ContentType.AUDIO:
                caption = "📢 Ответ из канала"
                if message.caption:
                    caption += f"\n\n{message.caption}"
                
                await self.bot.send_audio(
                    chat_id=user_id,
                    audio=message.audio.file_id,
                    caption=caption
                )
            
            else:
                await self.bot.send_message(
                    chat_id=user_id,
                    text="📢 Получен ответ из канала (неподдерживаемый тип контента)"
                )
                
        except Exception as e:
            logger.error(f"Ошибка при пересылке ответа пользователю {user_id}: {e}")
