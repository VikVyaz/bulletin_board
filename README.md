# Доска объявлений

## О проекте
Backend API для сервиса с объявлениями, отзывами, аутентификацией, 
email-уведомлениями и автоматическим деплоем Docker + GitHub Actions.

## ✨ Основной функционал

🔐 Аутентификация и пользователи
* JWT-аутентификация (Bearer)
* Роли: user, admin
* Сброс пароля по email (uid + token)

📢 Объявления (Ad)
* CRUD для объявлений.
* Сортировка по дате (новые выше).
* Поиск по полям: title, price, description.
* Пагинация (≤ 4 на страницу).

💬 Отзывы (Feedback)
* Пользователи могут оставлять отзывы под объявлениями.
* CRUD для своих отзывов.
* Админ может управлять всеми отзывами.

👮 Permissions
* Аноним: только просмотр списка объявлений.
* User: свои объявления/отзывы.
* Admin: управление всем.

🚀 Extra фичи
* Celery уведомления по email о новых отзывах
* Celery-beat: периодический трекер количества новых отзывов
* Деплой на ВМ Yandex Cloud (Docker + Actions) http://130.193.57.240

## 🛠 Технологии и стек
* Python 3.12+
* Django, Django REST Framework
* PostgreSQL
* CORS-конфигурация
* Nginx
* JWT (SimpleJWT)
* Celery + Celery-beat + Redis
* Docker, Docker Compose, Docker Hub
* GitHub Actions (CI/CD), GitHub Secrets
* Swagger / Redoc
* pytest

## 📚 API Документация
* Swagger UI: http://130.193.57.240/swagger/
* Redoc: http://130.193.57.240/redoc/

## ☁️ Деплой
Подробная инструкция:
➡️ [DEPLOY.md](./DEPLOY.md)

## 📝 Планы
* Интеграция Telegram как альтернатива email-рассылке
* Избранные объявления
* Простенький фронт

## 👤 Автор

Кузнецов Виктор
https://github.com/VikVyaz