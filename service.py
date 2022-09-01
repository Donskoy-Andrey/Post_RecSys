import os
from typing import List
from fastapi import FastAPI
from schema import PostGet, Response
from datetime import datetime
import pandas as pd
import random
import logging
import joblib
from sklearn.preprocessing import StandardScaler
import warnings
import hashlib
from dotenv import load_dotenv


"""
INSTALL LIBRARIES:
    pip install -r requirements.txt    

START SERVICE:
    python -m uvicorn service:app --reload --port 8899    
"""

load_dotenv()
database = os.environ.get('DATABASE')
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')
host = os.environ.get('HOST')
port = os.environ.get('PORT')
PATH1 = os.environ.get('PATH1')  # CONTROL MODEL
PATH2 = os.environ.get('PATH2')  # TEST MODEL


logging.basicConfig(level=logging.DEBUG)
warnings.filterwarnings("ignore")

CONNECTION = f"postgresql://{user}:{password}@{host}:{port}/{database}"
SALT = 'pepper'
TEST_PERCENTAGE = 50

app = FastAPI()


default_posts_data = pd.read_sql(
    """
    SELECT * FROM public.post_text_df
    """,
    con=CONNECTION
).rename({'post_id': 'id'}, axis=1)

post_data = pd.read_sql(
    """
    SELECT * FROM public.my_post_data
    """,
    con=CONNECTION
)

df_user_data = pd.read_sql(
    """
    SELECT * FROM public.my_user_data
    """,
    con=CONNECTION
)

df_time_data = pd.read_sql(
    f"""
    SELECT * FROM public.my_time_data
    ORDER BY RANDOM()
    LIMIT 100000;
    """,
    con=CONNECTION
)


def get_model_path(exp_group: str) -> str:
    """
    CHOOSE MODEL PATH IN A/B TESTING
    """
    if os.environ.get("IS_LMS") == "1":
        if exp_group == 'control':
            MODEL_PATH = '/workdir/user_input/model_control'
        elif exp_group == 'test':
            MODEL_PATH = '/workdir/user_input/model_test'
        else:
            raise ValueError('unknown group')
    else:
        if exp_group == 'control':
            MODEL_PATH = PATH1
        elif exp_group == 'test':
            MODEL_PATH = PATH2
        else:
            raise ValueError('unknown group')
    return MODEL_PATH


def load_models(exp_group):
    """
    LOAD ONE OF TWO MODELS
    """
    logging.info('Loading model')
    model_path = get_model_path(exp_group)
    model = joblib.load(model_path)
    logging.info(model)
    return model


def prepare_df_user(id: int, time: datetime, df_user):
    """
    PREPARE USER DATAFRAME WITH ALL POSTS
    FOR FEEDING THE MODEL
    """
    logging.info('Creating DataFrame for User')
    df_user = df_user[df_user.user_id == id]
    df_user = df_user.drop('user_id', axis=1)

    post_data['month'] = time.month
    post_data['weekday'] = time.weekday()
    post_data['hour'] = time.hour
    post_data['minute'] = time.minute

    for col in df_user.columns:
        post_data[col] = df_user[col].item()

    df_user = post_data.reset_index().drop('index', axis=1)
    df_user = df_user.set_index('post_id')

    df_user = df_user[['gender', 'age', 'country', 'city',
                       'exp_group', 'month', 'weekday',
                       'hour', 'minute', 'topic', 'text_len',
                       'cluster_0', 'cluster_1', 'cluster_2',
                       'cluster_3', 'cluster_4', 'cluster_5',
                       'cluster_6', 'os_iOS', 'source_organic'
                       ]]

    logging.info('Time Processing')

    user_time = pd.DataFrame.from_dict(
        {'index': [len(df_time_data)],
         'month': [time.month],
         'weekday': [time.weekday()],
         'hour': [time.hour],
         'minute': [time.minute]}
    )

    df_time = pd.concat((df_time_data, user_time), axis=0)
    df_time = StandardScaler().fit_transform(df_time.iloc[:, 1:])

    df_user[['month', 'weekday', 'hour', 'minute']] = df_time[-1]

    return df_user


def get_predict(df_user, limit, exp_group):
    """
    CHOOSE {LIMIT} POSTS WITH THE HIGHEST METRIC VALUE
    """
    logging.info('Get Predict')
    model = load_models(exp_group)
    preds = model.predict_proba(df_user)[:, 1]
    top_of_preds = pd.DataFrame(preds, df_user.index, columns=['value']).sort_values(by='value', ascending=False)
    result = top_of_preds[:limit].index.values

    all_result = []

    for i in result:
        all_result.append(default_posts_data[default_posts_data.id == i] \
                          .iloc[0, :].to_dict()
                           )

    return {'exp_group': exp_group, 'recommendations': all_result}


def get_exp_group(user_id: int) -> str:
    """
    ASSIGN USER TO EXP_GROUP (TEST AND CONTROL)
    FOR A/B MODEL TESTING
    """
    text = str(user_id) + SALT
    value = int(hashlib.md5(text.encode()).hexdigest(), 16)
    margin = value % 100
    if margin < TEST_PERCENTAGE:
        exp_group = 'test'
    elif margin > (100-TEST_PERCENTAGE):
        exp_group = 'control'
    logging.info(f"User group = {exp_group}!")
    return exp_group


@app.get("/post/recommendations/", response_model=Response)
def recommended_posts(id: int, time: datetime, limit: int = 10) -> Response:
    """
    GET {LIMIT} RECOMMENDED POSTS
    EXAMPLE QUERY: http://localhost:8899/post/recommendations/?id=5&time=2021-10-2 10:35:54&limit=10
    """
    start_time = datetime.now()
    df_user = prepare_df_user(id, time, df_user_data)
    exp_group = get_exp_group(id)
    predict = get_predict(df_user, limit, exp_group)
    logging.info(f'Time: {datetime.now() - start_time}')
    return predict


@app.get("/baseline/", response_model=List[PostGet])
def baseline(id: int, time: datetime, limit: int = 10) -> List[PostGet]:
    """
    GET {LIMIT} RANDOM POSTS
    EXAMPLE QUERY: http://localhost:8899/baseline/?id=5&time=2021-10-2 10:35:54&limit=10
    """
    nums = random.sample(
        list(post_data.post_id.values),
        limit
    )
    result = default_posts_data[default_posts_data.id.isin(nums)]\
        .to_dict(orient='records')
    return result
