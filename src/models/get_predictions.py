import pandas as pd

from ..service.schema import Response
import logging
from src.models.model_loader import load_model
from src.data.data_for_launch import default_posts_data


def get_predict(df_user: pd.DataFrame, limit: int, exp_group: str) -> Response:
    """
    CHOOSE {LIMIT} POSTS WITH THE HIGHEST METRIC VALUE
    """
    logging.info('Get Predict')
    model = load_model(exp_group)
    preds = model.predict_proba(df_user)[:, 1]
    top_of_preds = pd.DataFrame(
        preds, df_user.index, columns=['value']
    ).sort_values(by='value', ascending=False)

    result = top_of_preds[:limit].index.values

    all_result = []

    for i in result:
        all_result.append(
            default_posts_data[default_posts_data.id == i].iloc[0, :].to_dict()
        )

    return Response(
        **{'exp_group': exp_group,
           'recommendations': all_result}
    )