from mage_ai.data_cleaner.transformer_actions.base import BaseAction
from mage_ai.data_cleaner.transformer_actions.constants import ActionType, Axis
from mage_ai.data_cleaner.transformer_actions.utils import build_transformer_action
from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def execute_transformer_action(df: DataFrame, *args, **kwargs) -> DataFrame:
    
# Assuming df is your DataFrame


    df.columns = df.columns.str.replace(r'(?<!^)(?=[A-Z])', '_').str.replace(' ', '_')

    df.columns = df.columns.str.lower()

    rename_dict = {
    'c_r_s_dep_time_hour': 'crs_dep_time_hour',
    'c_r_s_arr_time_hour': 'crs_arr_time_hour',
    'c_r_s_dep_time_minute': 'crs_dep_time_minute',
    'c_r_s_arr_time_minute': 'crs_arr_time_minute'
    }

    df.rename(columns=rename_dict, inplace=True)
    
    
# Print the modified DataFrame schema
    print(df.dtypes)
    return df
    # return BaseAction(action).execute(df)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'




