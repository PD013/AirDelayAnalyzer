import subprocess
import os
from zipfile import ZipFile

@data_loader
def load_data_from_api(*args, **kwargs) -> str:
    """
    Load data from Kaggle dataset using Kaggle CLI.

    Returns:
        str: File path of the extracted Flight_Delay.parquet file.
    """
    # Define the command to download the dataset
    command = ['kaggle', 'datasets', 'download', '-d', 'arvindnagaonkar/flight-delay']

    # Run the command to download the dataset
    subprocess.run(command, check=True)

    # Define the target directory
    target_dir = '/home/preet/de-project/mage/de-project/raw_data'

    # Check if the target directory exists, create it if it doesn't
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Extract the contents of the ZIP file
    with ZipFile('flight-delay.zip', 'r') as zip_ref:
        # Delete any existing Flight_Delay.parquet file in the target directory
        existing_parquet_path = os.path.join(target_dir, 'Flight_Delay.parquet')
        if os.path.exists(existing_parquet_path):
            os.remove(existing_parquet_path)

        # Extract only the 'Flight_Delay.parquet' file to the target directory
        for file in zip_ref.namelist():
            if 'Flight_Delay.parquet' in file:
                zip_ref.extract(file, path=target_dir)
            else:
                # Check if the file exists before attempting to remove it
                file_path = os.path.join(target_dir, file)
                if os.path.exists(file_path):
                    os.remove(file_path)

    # Construct the file path of the extracted file
    extracted_file_path = os.path.join(target_dir, 'Flight_Delay.parquet')

    # Return the file path
    return extracted_file_path
