CREATE TABLE IF NOT EXISTS message_mapping (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    user_message_id BIGINT NOT NULL,
    channel_message_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, user_message_id, channel_message_id)
);

CREATE INDEX IF NOT EXISTS idx_message_mapping_user_id ON message_mapping(user_id);
CREATE INDEX IF NOT EXISTS idx_message_mapping_channel_message_id ON message_mapping(channel_message_id);
CREATE INDEX IF NOT EXISTS idx_message_mapping_created_at ON message_mapping(created_at);

COMMENT ON TABLE message_mapping IS 'Таблица для хранения соответствия сообщений пользователей и сообщений в канале';
COMMENT ON COLUMN message_mapping.user_id IS 'ID пользователя Telegram';
COMMENT ON COLUMN message_mapping.user_message_id IS 'ID сообщения пользователя';
COMMENT ON COLUMN message_mapping.channel_message_id IS 'ID сообщения в канале';
COMMENT ON COLUMN message_mapping.created_at IS 'Время создания записи';
