# api_yamdb
api_yamdb

## Что я сделал
### Кастомизация модели User
 - Создал приложение Users
 - Создал собственную модель User, унаследовав её от AbstractUser c новыми полями
 - файле settings AUTH_USER_MODEL = 'users.User'
 - зарегистрировал в админке admin.site.register(User)
 - выполнил миграции

### работа с токеном
 - Аутентификация по JWT-токену
 - Подключил Фреймворк DRF pip install djangorestframework
 - добавил приложение rest_framework в INSTALLED_APPS
 - подключил две библиотеки Djoser и Simple JWT pip install djoser djangorestframework-simplejwt==4.7.2
 - Обновил файл settings.py
 - В settings.py в настройках  REST_FRAMEWORK объявил новый способ аутентификации TokenAuthentication

