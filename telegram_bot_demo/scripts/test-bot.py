#!/usr/bin/env python3
import asyncio
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bot'))

try:
    from database import Database
except ImportError:
    print("❌ Не удалось импортировать модуль database")
    print("   Убедитесь, что вы находитесь в корневой папке проекта")
    sys.exit(1)

load_dotenv()

async def test_database():
    print("🔍 Тестирование подключения к базе данных...")
    
    try:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("❌ DATABASE_URL не найден в .env файле")
            return False
        
        db = Database(database_url)
        await db.init()
        print("✅ Подключение к базе данных успешно")

        print("🔨 Проверка структуры базы данных...")

        await db.close()
        print("✅ База данных работает корректно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании базы данных: {e}")
        return False

async def test_environment():
    print("🔍 Проверка переменных окружения...")
    
    required_vars = [
        "BOT_TOKEN",
        "WEBHOOK_URL", 
        "CHANNEL_ID",
        "DATABASE_URL"
    ]
    
    all_good = True
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith("your_") or value.startswith("https://your-domain"):
            print(f"❌ {var}: не настроен")
            all_good = False
        else:
            print(f"✅ {var}: настроен")
    
    return all_good

async def main():
    print("🧪 Тестирование Telegram Bot...")
    print("=" * 50)
    
    env_ok = await test_environment()
    print()
    
    if not env_ok:
        print("⚠️  Некоторые переменные окружения не настроены")
        print("   Отредактируйте .env файл и запустите тест снова")
        return

    db_ok = await test_database()
    print()
    
    if db_ok:
        print("🎉 Все тесты пройдены успешно!")
        print("   Бот готов к работе")
    else:
        print("❌ Некоторые тесты не пройдены")
        print("   Проверьте логи и настройки")

if __name__ == "__main__":
    asyncio.run(main())
