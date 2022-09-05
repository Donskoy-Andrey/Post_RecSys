# Описание
Проектом является рекомендательная система текстовых постов на основе данных о пользователях, 
публикациях и взаимодействиях между ними.

# Аспекты разработки
В качестве метрики оценки постов для рекомендации была выбрана ROC-AUC на таргете "поставил ли пользователь лайк посту".

Проект включает в себя два блока: применение методов машинного обучения для обработки исходных данных и построения моделей (Stack: sklearn, catboost, nltk, pandas, numpy и др.), а также создание сервиса для взаимодействия с моделями в рамках AB-тестирования (Stack: FastAPI, pydantic, hashlib и др.)

**ЭТАП 1.** Создание базы данных готовых фичей для пользователя и постов производилась в Jupyter Notebook и включала в себя:
1. Подгрузку исходных баз данных с помощью SQL запросов.
2. Первичную обработку данных о постах.
3. Выделение текстовой информации из постов (TF-IDF) и их кластеризация на основе этих фичей.
3. Первичную обработку данных о юзерах.
4. Кодирование категориальной информации - Feature Target Encoding.
5. Сохранение предобработанных датасетов через SQL для последующей загрузки в сервис модели.
6. Формирование полного датасета на > миллион строк на основе публикаций, пользователей и взаимодействий между ними.
7. Обучение моделей, выбор лучших параметров с помощью поиска по сетке параметров.
8. Сохранение моделей в файлы для загрузки на сервис.

**ЭТАП 2.** Реализован сервис взаимодействия с моделями, который включает следующие аспекты:
1. Подгрузка и создание фичей конкретного пользователя.
2. Определение его в одну из двух групп для AB тестирования (выбор между 2-мя моделями).
3. Конкатенация данных о пользователе и всех публикациях (контентный подход к рекомендациям).
4. Предсказание метрики (вероятность лайкнуть тот или иной пост).
5. Сортировка по метрике и выбор необходимого числа лучших.
6. Выдача результата.

![Service Example]()

# Описание репозитория
**service.py** - сервис проекта, написанный на FastAPI\
**schema.py** - валидация выходных данных\
**.env.example** - пример данных для подключения (реальные данные скрыты в .gitignore)\
**project.ipynb** - полная реализация 1 этапа с созданием ML-моделей.
