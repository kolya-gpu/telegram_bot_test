import asyncpg
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class Database:
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool: Optional[asyncpg.Pool] = None
    
    async def init(self):
        try:
            self.pool = await asyncpg.create_pool(self.database_url)
            await self._create_tables()
            logger.info("База данных инициализирована")
        except Exception as e:
            logger.error(f"Ошибка инициализации базы данных: {e}")
            raise
    
    async def _create_tables(self):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS message_mapping (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    user_message_id BIGINT NOT NULL,
                    channel_message_id BIGINT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, user_message_id, channel_message_id)
                )
            """)
            logger.info("Таблицы созданы")
    
    async def save_message_mapping(
        self, 
        user_id: int, 
        user_message_id: int, 
        channel_message_id: int
    ) -> bool:
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO message_mapping (user_id, user_message_id, channel_message_id)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (user_id, user_message_id, channel_message_id) 
                    DO NOTHING
                """, user_id, user_message_id, channel_message_id)
                logger.info(f"Маппинг сохранен: user_id={user_id}, channel_message_id={channel_message_id}")
                return True
        except Exception as e:
            logger.error(f"Ошибка сохранения маппинга: {e}")
            return False
    
    async def get_user_by_channel_message(self, channel_message_id: int) -> Optional[int]:
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT user_id FROM message_mapping 
                    WHERE channel_message_id = $1
                    ORDER BY created_at DESC
                    LIMIT 1
                """, channel_message_id)
                return row['user_id'] if row else None
        except Exception as e:
            logger.error(f"Ошибка получения пользователя: {e}")
            return None
    
    async def get_user_message_id(self, user_id: int, channel_message_id: int) -> Optional[int]:
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT user_message_id FROM message_mapping 
                    WHERE user_id = $1 AND channel_message_id = $2
                    ORDER BY created_at DESC
                    LIMIT 1
                """, user_id, channel_message_id)
                return row['user_message_id'] if row else None
        except Exception as e:
            logger.error(f"Ошибка получения user_message_id: {e}")
            return None
    
    async def close(self):
        if self.pool:
            await self.pool.close()
            logger.info("Соединения с базой данных закрыты")
