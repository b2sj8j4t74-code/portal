# API Documentation

## Аутентификация

- POST `/api/token/`
  - body: `{ "username": "...", "password": "..." }`
  - response: `{ "token": "..." }`

## Пользователи

- GET `/api/users/`
- POST `/api/users/`
- GET `/api/users/<id>/`
- PUT `/api/users/<id>/`
- PATCH `/api/users/<id>/`
- DELETE `/api/users/<id>/`

### Регистрация пользователя

POST `/api/users/`

Пример тела:

```json
{
  "username": "apiuser",
  "email": "user@example.com",
  "password": "password123"
}
```

## Новости

- GET `/api/news/`
- POST `/api/news/`
- GET `/api/news/<id>/`
- PUT `/api/news/<id>/`
- PATCH `/api/news/<id>/`
- DELETE `/api/news/<id>/`

### Фильтрация

- `/api/news/?author=<id>` — вывод новостей выбранного автора.

### Пример создания новости

POST `/api/news/`

```json
{
  "title": "Заголовок новости",
  "summary": "Краткое описание",
  "content": "Полный текст новости должен содержать минимум 50 символов..."
}
```

### Ответы с ошибками

Если данные не прошли валидацию, API возвращает JSON с полями ошибок:

```json
{
  "title": ["Это поле обязательно."],
  "content": ["Минимум 50 символов."]
}
```
