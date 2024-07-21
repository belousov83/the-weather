# 

Прогноз погоды

Приложение показывает прогноз погоды введенного или выбранного из истории поиска города.

Для создания этого сайта я использовал API Яндекс.Погоды и JavaScript API и HTTP Геокодер, также от Яндекса.
Автодополнение реализовано с помощью сервиса dadata.ru

1. Прогноз можно получить на любой интервал времени от 1 до 7 дней
2. Регистрация возможна как через API, так и через стандартные формы
3. Личный кабинет сделан через Django REST framework
4. Подключен drf-spectacular для генерации Swagger схем
4. Собирается и выводится информация по истории всех запросов пользователя
5. Вывод данных в удобном локализованном виде с указанием дней недели
6. Погоду можно посмотреть в уже запрашиваемых городах
7. Все помещено в докер контейнер
8. Сделал парочку простых тестов на регистрацию и авторизацию.



Запуск проекта


1. Клонируйте репозиторий:

```
git clone https://github.com/belousov83/the-weather.git
```

2. Установите виртуальное окружение:

```
python -m venv your_venv
``` 

3. Активируйте виртуальное окружение:
```
venv/Scripts/activate
```

4. Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

5. Сделайте миграции:
```
python manage.py migrate
```

6. Запустите сервер, выполнив команду:
```
python manage.py runserver
```