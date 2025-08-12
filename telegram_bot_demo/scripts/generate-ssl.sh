#!/bin/bash
echo "🔐 Генерация самоподписанных SSL-сертификатов..."

mkdir -p nginx/ssl

openssl req -x509 -newkey rsa:4096 -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem -days 365 -nodes -subj "/C=RU/ST=State/L=City/O=Organization/CN=localhost"

chmod 600 nginx/ssl/key.pem
chmod 644 nginx/ssl/cert.pem

echo "✅ SSL сертификаты созданы:"
echo "   - Сертификат: nginx/ssl/cert.pem"
echo "   - Приватный ключ: nginx/ssl/key.pem"
echo ""
echo "⚠️  ВНИМАНИЕ: Это самоподписанные сертификаты для тестирования!"
echo "   Для продакшена используйте настоящие SSL сертификаты от Let's Encrypt или другого CA."
echo ""
echo "🔒 Права доступа установлены:"
echo "   - Сертификат: 644 (чтение для всех, запись для владельца)"
echo "   - Приватный ключ: 600 (только для владельца)"
