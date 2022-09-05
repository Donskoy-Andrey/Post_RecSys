from sklearn.preprocessing import StandardScaler
from data_for_launch import df_time_data, post_data
import pandas as pd
import logging
from datetime import datetime


def prepare_df_user(id: int, time: datetime, df_user) -> pd.DataFrame:
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

