from connection import CONNECTION
import pandas as pd

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

