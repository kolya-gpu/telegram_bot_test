# Telegram Bot - Пересылка сообщений

Telegram-бот на Python (aiogram) для перенаправления сообщений от пользователей в канал и пересылки ответов обратно пользователям. Бот работает через webhook и разворачивается в Docker-окружении.

## 🚀 Основной функционал

- ✅ Приём сообщений от пользователя (текст, фото, видео, документы, аудио, голосовые)
- ✅ Пересылка сообщений в указанный канал
- ✅ Хранение маппинга user_id ↔ сообщение в канале для идентификации ответов
- ✅ Обратная пересылка ответов из канала конкретному пользователю
- ✅ Поддержка всех типов контента Telegram

## 🏗️ Архитектура

- **Сервис bot** (Python 3.11 + aiogram) — принимает webhook-запросы от Telegram API
- **PostgreSQL** — хранит соответствие user ↔ сообщение в канале
- **Nginx** — принимает HTTPS, проксирует на бота
- **Docker Compose** — для локального запуска и тестов

## 📋 Требования

- Docker и Docker Compose
- Telegram Bot Token (получить у @BotFather)
- Домен с SSL-сертификатом (для webhook)
- Канал в Telegram

## 🛠️ Установка и настройка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd telegram_bot
```

### 2. Настройка переменных окружения

Скопируйте файл `env.example` в `.env` и заполните необходимые значения:

```bash
cp env.example .env
```

Отредактируйте `.env` файл:

```env
# Telegram Bot Configuration
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
WEBHOOK_URL=https://your-domain.com/webhook
CHANNEL_ID=@your_channel_username

# Database Configuration
DATABASE_URL=postgresql://bot_user:bot_password@localhost:5432/telegram_bot
```

### 3. Настройка SSL-сертификатов

Создайте папку `nginx/ssl/` и поместите туда ваши SSL-сертификаты:

```bash
mkdir -p nginx/ssl
# Скопируйте cert.pem и key.pem в nginx/ssl/
```

### 4. Запуск сервисов

```bash
docker-compose up -d
```

### 5. Проверка работы

```bash
# Проверка статуса сервисов
docker-compose ps

# Просмотр логов бота
docker-compose logs bot

# Проверка доступности webhook
curl -k https://your-domain.com/health
```

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | Пример |
|------------|----------|---------|
| `BOT_TOKEN` | Токен бота от @BotFather | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `WEBHOOK_URL` | URL для webhook | `https://your-domain.com/webhook` |
| `CHANNEL_ID` | ID или username канала | `@your_channel` или `-1001234567890` |
| `DATABASE_URL` | Строка подключения к PostgreSQL | `postgresql://user:pass@host:port/db` |

### Структура базы данных

```sql
CREATE TABLE message_mapping (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    user_message_id BIGINT NOT NULL,
    channel_message_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, user_message_id, channel_message_id)
);
```

## 📱 Использование

### 1. Отправка сообщения боту

Пользователь отправляет любое сообщение боту:
- Текст
- Фото
- Видео
- Документы
- Аудио
- Голосовые сообщения

### 2. Пересылка в канал

Бот автоматически пересылает сообщение в указанный канал с пометкой от какого пользователя оно пришло.

### 3. Ответ администратора

Администратор в канале отвечает на сообщение (используя функцию "Ответить").

### 4. Пересылка ответа пользователю

Бот автоматически определяет, кому отправить ответ, и пересылает его пользователю.

## 🔍 Логирование

Логи сохраняются в папку `logs/`:

- `logs/` - логи бота
- `logs/nginx/` - логи Nginx

## 🐳 Docker команды

```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Перезапуск конкретного сервиса
docker-compose restart bot

# Просмотр логов
docker-compose logs -f bot

# Обновление и пересборка
docker-compose up -d --build
```

## 🚨 Устранение неполадок

### Бот не отвечает

1. Проверьте токен бота в `.env`
2. Убедитесь, что webhook установлен корректно
3. Проверьте логи: `docker-compose logs bot`

### Ошибки базы данных

1. Проверьте подключение к PostgreSQL
2. Убедитесь, что база данных запущена: `docker-compose ps postgres`
3. Проверьте логи PostgreSQL: `docker-compose logs postgres`

### Проблемы с SSL

1. Убедитесь, что сертификаты находятся в `nginx/ssl/`
2. Проверьте права доступа к файлам сертификатов
3. Проверьте логи Nginx: `docker-compose logs nginx`

## 📚 API Endpoints

- `POST /webhook` - webhook для Telegram API
- `GET /health` - проверка статуса сервиса

## 🔒 Безопасность

- Бот работает только через HTTPS
- Используется безопасная конфигурация SSL
- База данных изолирована в Docker-сети
- Бот работает под непривилегированным пользователем

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License

## 📞 Поддержка

При возникновении проблем создайте Issue в репозитории проекта.
