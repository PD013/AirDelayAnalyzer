

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
import os
from typing import List



@data_exporter
def export_data_to_google_cloud_storage(*args, **kwargs) -> List[str]:
    """
    Export data from local folders to Google Cloud Storage with the desired folder structure.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    # Define the folder paths
    folder_paths = ['./final_data/df_airline_names',
                    './final_data/df_all', 
                    './final_data/df_place',
                    './final_data/df_time', 
                    './final_data/df_time_periods',
                    './final_data/df_total_delay',
                    './final_data/total_delay_by_year_airline'] 

    # Load configuration
    config_path = os.path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    # GCS bucket name
    bucket_name = 'de-project-0921'
    # Base folder in GCS
    base_object_key = 'final_data/'

    # List to store successfully uploaded file paths
    uploaded_files = []

    # Export each folder and its contents to GCS
    for folder_path in folder_paths:
        try:
            # Get the folder name from the path
            folder_name = os.path.basename(folder_path)
            # Define the object key for the folder in GCS
            folder_object_key = os.path.join(base_object_key, folder_name) + '/'
            
            # Export files from the folder to GCS
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    # Construct the local file path
                    local_file_path = os.path.join(root, file)
                    # Construct the object key for the file in GCS
                    gcs_object_key = os.path.join(folder_object_key, file)
                    # Export the file to GCS, overwriting any existing file
                    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
                        local_file_path,
                        bucket_name,
                        gcs_object_key,
                        force=True  # Overwrite existing file if present
                    )
                    # Print a message after each file upload
                    print(f"Uploaded {local_file_path} to {gcs_object_key}")
                    # Add the uploaded file path to the list
                    uploaded_files.append(local_file_path)
        except Exception as e:
            print(f"Error uploading files from {folder_path}: {e}")

    return uploaded_files


