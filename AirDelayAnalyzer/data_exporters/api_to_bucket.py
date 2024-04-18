
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data_to_google_cloud_storage(data: str, **kwargs) -> None:
    """
    Export a file to a Google Cloud Storage bucket.

    Args:
        file_path (str): Path to the file to be exported.
        **kwargs: Additional keyword arguments.

    """
    # Specify the configuration settings file path and profile
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    # Specify the bucket name and object key prefix
    bucket_name = 'de-project-0921'  # Update with your bucket name
    object_key_prefix = 'raw_data/'  # Update with your desired folder path

    # Initialize GoogleCloudStorage with the specified configuration
    gcs = GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile))

    # Extract the file name from the file path
    file_name = path.basename(data)

    # Specify the object key
    object_key = f"{object_key_prefix}{file_name}"

    # Upload the file to the Google Cloud Storage bucket
    gcs.export(data, bucket_name, object_key, force=True)


