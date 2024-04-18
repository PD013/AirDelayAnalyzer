import pandas as pd
import pyarrow.parquet as pq
from io import BytesIO
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from google.cloud import storage
from os import path
from typing import List

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_from_google_cloud_storage(*args, **kwargs) -> pd.DataFrame:
    """
    Load data from a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Args:
        args: Additional positional arguments.
        kwargs: Additional keyword arguments.

    Returns:
        pd.DataFrame: Merged DataFrame containing data from all files in the specified folder.
    """
    # Define configuration settings
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    bucket_name = 'de-project-0921'
    folder_path = 'final_data/df_all/' # Adjust to the desired folder path in the bucket

    # Initialize Google Cloud Storage client
    client = storage.Client()

    # List all blobs (files) in the specified folder
    blobs = client.list_blobs(bucket_name, prefix=folder_path)

    # List to store individual DataFrames
    dfs = []

    # Iterate over each blob and load its data into a DataFrame
    for blob in blobs:
        try:
            # Load Parquet file from GCS
            parquet_file = blob.download_as_string()
            # Read Parquet file into a DataFrame
            df = pq.ParquetFile(BytesIO(parquet_file)).read().to_pandas()
            # Append the DataFrame to the list
            dfs.append(df)
        except Exception as e:
            print(f"Error loading file {blob.name}: {e}")

    # Merge all DataFrames into a single DataFrame
    merged_df = pd.concat(dfs, ignore_index=True)
    print(merged_df.head(4))

    num_rows = len(merged_df)
    print("Number of rows:", num_rows)

    return merged_df

@test
def test_output(output: pd.DataFrame, *args) -> None:
    """
    Template code for testing the output of the block.

    Args:
        output (pd.DataFrame): Output DataFrame.
        args: Additional positional arguments.
    """
    assert output is not None, 'The output is undefined'
    assert isinstance(output, pd.DataFrame), 'Output is not a DataFrame'
    assert not output.empty, 'Output DataFrame is empty'