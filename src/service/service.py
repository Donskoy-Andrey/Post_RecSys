from typing import List
from fastapi import FastAPI, HTTPException
from datetime import datetime
import random
import logging
from src.service.schema import PostGet, Response
from src.data.data_for_launch import default_posts_data, post_data, df_user_data
from src.models.model_loader import get_exp_group
from src.features.construct_user_dataframe import prepare_df_user
from src.models.get_predictions import get_predict

app = FastAPI()


@app.get("/post/recommendations/", response_model=Response)
def recommended_posts(user_id: int, time: datetime, limit: int = 10) -> Response:
    """
    GET {LIMIT} RECOMMENDED POSTS
    EXAMPLE QUERY: http://localhost:8899/post/recommendations/?user_id=200&time=2021-10-2 10:35:54&limit=10
    """
    if user_id not in df_user_data.user_id.values:
        raise HTTPException(status_code=404, detail='User not found. Please, correct your query.')

    start_time = datetime.now()
    df_user = prepare_df_user(user_id, time, df_user_data)
    exp_group = get_exp_group(user_id)
    predict = get_predict(df_user, limit, exp_group)
    logging.info(f'Time: {datetime.now() - start_time}')
    return predict


@app.get("/baseline/", response_model=List[PostGet])
def baseline(user_id: int, time: datetime, limit: int = 10) -> List[PostGet]:
    """
    GET {LIMIT} RANDOM POSTS
    EXAMPLE QUERY: http://localhost:8899/baseline/?user_id=200&time=2021-10-2 10:35:54&limit=10
    """
    nums = random.sample(
        list(post_data.post_id.values),
        limit
    )
    result = default_posts_data[default_posts_data.id.isin(nums)] \
        .to_dict(orient='records')
    return result
