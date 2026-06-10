from api_client.client import NewsAPIClient


def run_example():
    client = NewsAPIClient('http://127.0.0.1:8000')

    # Регистрация нового пользователя
    registration = client.register('apiuser', 'apiuser@example.com', 'password123')
    print('Register:', registration)

    # Получение токена
    token_response = client.login('apiuser', 'password123')
    print('Login:', token_response)

    # Создание новости
    news = client.create_news(
        title='API: Новость для тестирования',
        content='Это тестовая новость, созданная через API-клиент. ' * 3,
        summary='Тестовый API-клиент'
    )
    print('Created news:', news)

    # Получение списка новостей
    all_news = client.get_news()
    print('News list:', all_news)

    # Обновление новости
    if news.get('id'):
        updated = client.update_news(news['id'], title='Обновлённая API-новость')
        print('Updated news:', updated)

    # Удаление новости
    if news.get('id'):
        delete_status = client.delete_news(news['id'])
        print('Delete status:', delete_status)


if __name__ == '__main__':
    run_example()
