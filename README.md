# Чат-боты (Telegram и VK) для распознавания речи

## Установка чат-ботов (Telegram и VK)

- Скачайте код.
- Установите актуальную версию poetry в `UNIX`-подобных дистрибутивах с помощью команды:
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
```
или в `Windows Powershell`:
```
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```
- Добавьте к переменной окружения `$PATH` команду poetry:
```
source $HOME/.poetry/bin
```
- Установите виртуальное окружение в директории с проектом командой:
```
poetry config virtualenvs.in-project true
```
- Установите все зависимости (для установки без dev зависимостей можно добавить аргумент `--no-dev`):
```
poetry install
```
- Активируйте виртуальное окружение командой: 
```
source .venv/bin/activate
```

## Настройка переменных окружения

- Cоздайте файл `.env` в директории проекта, на основе файла `.env.example` командой 
(при необходимости скорректируйте значения переменных окружения):
```
cp .env.example .env
```
<details>
  <summary>Переменные окружения</summary>
  <pre>
    TG_BOT_TOKEN=
    PROJECT_ID=
    GOOGLE_APPLICATION_CREDENTIALS=
    LOGGING_LEVEL=ERROR
  </pre>
</details>

*** Для работы telegram чат-бота необходимо заполнить переменную окружения `TG_BOT_TOKEN`. ***

*** Для интеграции с DialogFlow необходимо сначала создать новый проект и агента (затем указать переменную окружения `PROJECT_ID`). Далее создать и заполнить свою группу `intents`.
[Подробнее, как создать проект и настроить агента](https://cloud.google.com/dialogflow/es/docs/quick/build-agent) ***

*** Для подключения к своей группе с `intents` необходимо сгенерировать JSON ключ для подключения и в переменной окружения `GOOGLE_APPLICATION_CREDENTIALS` указать путь до файла. [Подробнее, как сгенерировать JSON ключ](https://habr.com/ru/post/502688/) ***

## Запуск линтеров

```
isort . && flake8 . && mypy .
```

## Запуск чат-бота для распознавания речи в Telegram и VK

- Для запуска telegram чат-бота вводим команду:
```
python3 tg_bot.py
```

## Цели проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Devman](https://dvmn.org).
