# Описание
Проектом является рекомендательная система текстовых постов на основе данных о пользователях, 
публикациях и взаимодействиях между ними.

# Запуск кода
1. Необходимо скопировать репозиторий себе локально:
```
git clone https://github.com/Donskoy-Andrey/Post_RecSys.git
```

2. Создаем образ Docker – контейнера:
```
docker build . -t TAG
```
где TAG – его имя.

3. Создаем Docker – контейнер:
```
docker run -p 8899:8899 TAG
```
где TAG – имя с предыдущего шага. 

4. Спустя некоторое время, отведенное на запуск сервиса (загрузка исходных баз данных), он станет доступен.
Проверка работы возможна по локальному адресу, который начинается с: 
```
http://127.0.0.1:8899/
```
или
```
http://localhost:8899/
```
5. Например, запрос 2 (limit) рекомендаций для пользователя 2021 (id) 
в момент времени 2020-11-11 (time) выглядит следующим образом:
```
http://127.0.0.1:8899/post/recommendations/?id=2021&time=2020-11-11%2010:35:54&limit=2
```
или
```
http://localhost:8899/post/recommendations/?id=2021&time=2020-11-11%2010:35:54&limit=2
```
\
![Service Example](https://github.com/Donskoy-Andrey/Post_RecSys/blob/master/images/example.gif)

# Стадии разработки
В качестве метрики оценки постов для рекомендации была выбрана ROC – AUC на таргете "поставил ли пользователь лайк посту".

Проект включает в себя два блока: применение методов машинного обучения для обработки исходных данных и построения моделей (Stack: sklearn, catboost, nltk, pandas, numpy и др.), а также создание сервиса для взаимодействия с моделями в рамках AB-тестирования (Stack: FastAPI, pydantic, hashlib и др.)

**ЭТАП 1.** Создание базы данных готовых фичей для пользователя и постов производилась в Jupyter Notebook и включала в себя:
1. Подгрузку исходных баз данных с помощью SQL запросов.
2. Первичную обработку данных о постах.
3. Выделение текстовой информации из постов (TF–IDF) и их кластеризация на основе этих фичей.
3. Первичную обработку данных о юзерах.
4. Кодирование категориальной информации – Feature Target Encoding.
5. Сохранение предобработанных датасетов через SQL для последующей загрузки в сервис модели.
6. Формирование полного датасета на > миллион строк на основе публикаций, пользователей и взаимодействий между ними.
7. Обучение моделей, выбор лучших параметров с помощью поиска по сетке параметров.
8. Сохранение моделей в файлы для загрузки на сервис.

**ЭТАП 2.** Реализован сервис взаимодействия с моделями, который включает следующие аспекты:
1. Подгрузка и создание фичей конкретного пользователя.
2. Определение его в одну из двух групп для AB – тестирования (выбор между 2-мя моделями).
3. Конкатенация данных о пользователе и всех публикациях (контентный подход к рекомендациям).
4. Предсказание метрики (вероятность лайкнуть тот или иной пост).
5. Сортировка по метрике и выбор необходимого числа лучших.
6. Выдача результата.
