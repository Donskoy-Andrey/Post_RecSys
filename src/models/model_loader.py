import os
import logging
import joblib
import hashlib

path_to_control_model = '../../models/model_control.pkl'
path_to_test_model = '../../models/model_test.pkl'
SALT = 'pepper'
TEST_PERCENTAGE = 50


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
    elif margin > (100 - TEST_PERCENTAGE):
        exp_group = 'control'
    logging.info(f"User group = {exp_group}!")
    return exp_group


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
            MODEL_PATH = path_to_control_model
        elif exp_group == 'test':
            MODEL_PATH = path_to_test_model
        else:
            raise ValueError('unknown group')
    return MODEL_PATH


def load_model(exp_group: str):
    """
    LOAD ONE OF TWO MODELS
    """
    logging.info('Loading model')
    model_path = get_model_path(exp_group)
    model = joblib.load(model_path)
    logging.info(model)
    return model

