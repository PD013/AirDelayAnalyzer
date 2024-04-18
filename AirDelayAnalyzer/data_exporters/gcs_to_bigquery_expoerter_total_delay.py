from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(df: DataFrame, **kwargs) -> None:
  """
  Export data to a BigQuery warehouse with customized settings.
  Specify your configuration settings in 'io_config.yaml' (optional).

  Args:
      df (DataFrame): The DataFrame containing the data to be exported.
      **kwargs: Additional keyword arguments (unused in this example).
  """
  # Project ID (replace with your actual GCP project ID)
  project_id = "dtc-de-course-412810"

  # Dataset and table names
  dataset_id = "project"
  table_name = "total_delay"

  # Construct the full table ID
  table_id = f"{project_id}.{dataset_id}.{table_name}"

  # Optional: Use a configuration file for BigQuery settings (replace path if needed)
  config_path = path.join(get_repo_path(), "io_config.yaml")
  config_profile = "default"  # Profile name within the configuration file

  # Export the DataFrame to BigQuery
  BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
      df, table_id, if_exists="replace"  # Overwrite existing data
  )


  print(f"Successfully exported data to BigQuery table: {table_id}")




