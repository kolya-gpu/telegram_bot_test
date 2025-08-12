# 🚀 Быстрый старт Telegram Bot

## 📋 Что нужно для запуска

1. **Docker и Docker Compose** - установлены и работают
2. **Telegram Bot Token** - получить у @BotFather
3. **Канал в Telegram** - создать или использовать существующий
4. **Домен с SSL** - для webhook (можно использовать ngrok для тестирования)

## ⚡ Быстрый запуск

### 1. Клонирование и настройка

```bash
git clone <repository-url>
cd telegram_bot
```

### 2. Настройка переменных окружения

```bash
# Linux/Mac
cp env.example .env

# Windows PowerShell
Copy-Item env.example .env
```

Отредактируйте `.env` файл:
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
WEBHOOK_URL=https://your-domain.com/webhook
CHANNEL_ID=@your_channel_username
```

### 3. Генерация SSL сертификатов (для тестирования)

```bash
# Linux/Mac
chmod +x scripts/generate-ssl.sh
./scripts/generate-ssl.sh

# Windows PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\scripts\generate-ssl.ps1
```

### 4. Запуск сервисов

```bash
# Linux/Mac
chmod +x scripts/setup.sh
./scripts/setup.sh

# Windows PowerShell
.\scripts\setup.ps1
```

## 🔧 Ручной запуск

Если скрипты не работают:

```bash
# Создание директорий
mkdir -p logs/nginx nginx/ssl

# Запуск сервисов
docker-compose up -d --build

# Проверка статуса
docker-compose ps
```

## 📱 Тестирование

1. **Отправьте сообщение боту** - любое текстовое сообщение
2. **Проверьте канал** - сообщение должно появиться с пометкой от пользователя
3. **Ответьте в канале** - используйте функцию "Ответить" на сообщение
4. **Проверьте бота** - ответ должен прийти пользователю

## 🚨 Частые проблемы

### Бот не отвечает
```bash
docker-compose logs bot
```

### Ошибки базы данных
```bash
docker-compose logs postgres
```

### Проблемы с SSL
```bash
docker-compose logs nginx
```

## 🛠️ Полезные команды

```bash
# Просмотр логов в реальном времени
docker-compose logs -f bot

# Перезапуск бота
docker-compose restart bot

# Остановка всех сервисов
docker-compose down

# Обновление и пересборка
docker-compose up -d --build
```

## 📚 Дополнительная документация

- [Полная документация](README.md)
- [Конфигурация Nginx](nginx/nginx.conf)
- [Схема базы данных](init.sql)

## 🆘 Поддержка

При возникновении проблем:
1. Проверьте логи: `docker-compose logs`
2. Убедитесь, что все переменные окружения настроены
3. Проверьте SSL сертификаты
4. Создайте Issue в репозитории
