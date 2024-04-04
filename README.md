# ubiquitous-parakeet
Монолитный сервис работающий как контактная книга, реализован на основе архитектуры REST.
## Задание первое
Необходимо разработать RESTful сервис с использованием `Fast API` и `Redis`. Эндпоинты (ручки):  
1. `Write_data` (запись и обновление данных)  
  a.`Phone`  
  b.`Address`  
2. `Check_data` (получение данных)  
  a.`Phone`

Сценарии использования сервиса:
1. Клиент отправляет запрос на ручку вида `https://111.111.111.111/check_data?phone=’89090000000’`. Эндпоинт в свою очередь получает номер телефона и идёт в `redis` по ключу (номер телефона) получает сохраненный адрес и отдаёт его в ответе клиенту.
2. Клиент отправляет запрос на ручку для записи данных в redis вида `https://111.111.111.111/write_data` с телом:  
   - `phone:’89090000000’`,
   - `address:’текстовый адрес’`.
3. Клиент отправляет запрос на ручку изменения адреса вида `https://111.111.111.111/write_data` с телом:
   - `phone:’89090000000’`,
   - `address:’текстовый адрес’`.
  
### Реализация
По итоогу получтлся сервис со следующими конечными точками:
  - GET `/check_data` - принимает в качестве параметра номер телефона `phone_number`, по которому происходит запрос к Redis и возвращается адрес контакта;
  - POST `/write_data` - принимает тело запроса в виде схемы `SContactAdd`, которая содержит поля `phone_number` и `address`. Если были переданы валидные данные, то добавляется новая запись в Redis, в ответ возвразается сообщение об успехе;
  - PATCH `/write_data` - принимает тело запроса в виде схемы `SContactUpdate`, которая содержит поля `phone_number` и `address`. Если были переданы валидные данные, запись в Redis обновляется и получает новое значение, в ответ возвращается сообщение об успехе.
### Сборка и запуск
#### Контейнер
Можно собрать сервис в контейнер используя `Dockerfile` в папке `/task_1` используя следующую команду:  
```shell
docker build . --tag contacts_service && docker run -p 8000:8000 contacts_service
```
И наблюдать следующий результат:
![Сборка контейнера](https://github.com/mementomorri/ubiquitous-parakeet/blob/main/screenshots/Screenshot_docker.png)
Сервис будет иметь следующий адрес: `http://0.0.0.0:8000`, взглянуть на документацию можно по пути `http://0.0.0.0:8000/docs`.  
Либо можно использовать `docker-compose.yml` в папке `/task_1` с помощью команды:
```shell
docker compose -f docker-compose.yml up --build
```
#### venv
Можно запустить сервис используя модуль `venv`, зависимости необходимые для запуска расположены в файле `/task_1/src/deploy_requierents.txt`. Затем можно запустить сервис используя точку входа `/task_1/main.py` имеющую следующее содержание:  
```python
import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "src.contacts:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
```
Сервис будет иметь следующий адрес: `http://0.0.0.0:8000`, взглянуть на документацию можно по пути: `http://0.0.0.0:8000/docs`.  
### Тестирование
Тесты написанные на `pytest` находятся в папке `/task_1/tests/`, запустить их можно командой: `pytest -v tests/` и наблюдать следующий результат:
![Результат тестирования](https://github.com/mementomorri/ubiquitous-parakeet/blob/main/screenshots/Screenshot_tests.png)
### Ручное тестирование
Симитируем работу фронтэнда и отправим несколько запросов имитирующих работу пользователя через встроенную документацию `Swagger`.
![Swagger](https://github.com/mementomorri/ubiquitous-parakeet/blob/main/screenshots/Screenshot_1.png)  
Представим, что пользователь хочет добавить контакт в контактную книгу через конечную точку `/write_data`, он заполняет данные и в ответ получает следующий результат:  
![Добавление контакта](https://github.com/mementomorri/ubiquitous-parakeet/blob/main/screenshots/Screenshot_2.png)  
Проверим, что данные записались корректно и сделаем GET запрос к `/check_data`:  
![Считывание контакта](https://github.com/mementomorri/ubiquitous-parakeet/blob/main/screenshots/Screenshot_3.png)  
Проверим что происходит, если ввести номер несуществующего контакта:  
![Контакт не найден](https://github.com/mementomorri/ubiquitous-parakeet/blob/main/screenshots/Screenshot_4.png)
Теперь представим, что пользователь хочет обновить данные о существующем контакте:  
![Изменение данных](https://github.com/mementomorri/ubiquitous-parakeet/blob/main/screenshots/Screenshot_5.png)
Проверим изменились ли данные:  
![Проверка изменений](https://github.com/mementomorri/ubiquitous-parakeet/blob/main/screenshots/Screenshot_6.png)  
Проверим что происходит, если мы попытаемся изменить данные о несуществующем контакте:  
![Изменение несуществующего контакта](https://github.com/mementomorri/ubiquitous-parakeet/blob/main/screenshots/Screenshot_7.png)  
Именно поэтому был выбран метод PATCH для изменения данных, а не метод PUT.
## Задание второе
Дано две таблицы в СУБД Postgres.
1. short_names
   
| name         | status |
| -------------| ------: |
| nazvanie1    |    1    |
| nazvanie2    |    0    |
| nazvanie5445 |    1    |
2. full_names  

| name             | status |
| -----------------| ------:|
| nazvanie1.mp3    |    1   |
| nazvanie2.mp3    |    0   |
| nazvanie5445.mp3 |    1   |

В одной таблице хранятся имена файлов без расширения. В другой хранятся имена файлов с расширением. Одинаковых названий с разными расширениями быть не может, количество расширений не определено, помимо wav и mp3 может встретиться что угодно. Нам необходимо минимальным количеством запросов к СУБД перенести данные о статусе из таблицы `short_names` в таблицу `full_names`. Необходимо понимать, что на выполнение запросов время работы скрипта нельзя тратить больше 10 минут. Лучшее время выполнения этого тестового задания в 2022 году - 45 секунд на SQL запросе. Необходимо предоставить два и более варианта решения этой задачи.
### Решение
В ходе выполнения задания были собраны таблицы имитирующие хранимые данные, `SQL` скрипт имитирующий случайное распределение данных по таблицам представлен по пути: `/task_2/mock_data.sql` и имеет следующее содердаение:
```sql
CREATE TABLE short_names_mock
(
    name   VARCHAR(64) UNIQUE,
    status BOOLEAN
);

CREATE TABLE full_names_mock
(
    name   VARCHAR(64) UNIQUE,
    status BOOLEAN
);

-- Имитация случайных данных в таблице short_names
INSERT INTO short_names_mock (name, status)
SELECT 'name.dummy' || GENERATE_SERIES(1, 700000), RANDOM() < 0.5;

-- Имитация случайных данных в таблице full_names
INSERT INTO full_names_mock (name)
SELECT 'name.anothername' || GENERATE_SERIES(1, 300000) || CASE WHEN RANDOM() < 0.5 THEN '.mp3' ELSE '.wav' END;

INSERT INTO full_names_mock (name)
SELECT 'name.anothername' || GENERATE_SERIES(300001, 500000) || CASE WHEN RANDOM() < 0.5 THEN '.flac' ELSE '.doc' END;

INSERT INTO full_names_mock (name)
SELECT 'name.anothername' || GENERATE_SERIES(500001, 700000) || CASE WHEN RANDOM() < 0.5 THEN '.jpg' ELSE '.png' END;

-- Копирование тпблиц в случайном порядке
CREATE TABLE short_names AS
SELECT name, status
FROM short_names_mock
ORDER BY RANDOM();

CREATE TABLE full_names AS
SELECT name, status
FROM full_names_mock
ORDER BY RANDOM();
```
После того как данные для проверки решений симитированы взглянем на пару возможных решенией. Решение первое, оно доступно по пути: `/task_2/solution_1.sql` и имеет следующее содержание:
```sql
UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE short_names.name = REGEXP_REPLACE(full_names.name, '\.[^.]*$', '');
```
Здесь используется перенос статуса файла с помощью регулярного выражения `\.[^.]*$`, регулярное выражение урезает расширение файла. Затем сравнивается название файлов из обеих таблиц и на основе этого статус переносится в таблицу `full_names`. Средняя скорость работы полученая в результате использования `pgbench` это 4276 миллисекунд, то есть чуть больше 4 секунд.
Решение второе, оно доступно по пути: `/task_2/solution_2.sql` и имеет следующее содержание:
```sql
UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE split_part(full_names.name, '.', 1) = short_names.name;
```
Здесь используется разделение имени файла на части с помощью функции split_part и сравнение на основе результата. Среднее время работы 10969 миллисекунд.
