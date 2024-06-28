# AirDelayAnalyzer

## Project Architecture Diagram

![Project Architecture](https://github.com/PD013/AirDelayAnalyzer/assets/114251906/b1631b99-2202-4ac4-9fa5-7c506afe05b4)

## Problem Statement

Flight delays are a persistent issue in the aviation industry, causing inconvenience and frustration for passengers and financial losses for airlines.
With air travel becoming an essential part of modern life, on-time performance is paramount for both passengers and airlines. Delays disrupt travel itineraries and cause significant inconvenience. This project delves into flight data to shed light on the root causes of delays, pinpoint trends specific to airlines and airports, and ultimately contribute to a more streamlined air travel experience.

Understanding the root causes of these delays is essential for developing strategies to improve on-time performance. While various factors contribute to flight delays, their relative impact and interactions remain unclear.

This project addresses this challenge by leveraging a comprehensive flight delay dataset from Kaggle encompassing domestic flights within the USA. By analyzing this data, we aim to:

- Identify the key cities that contribute to flight delays in the USA.
- Analyze the relationships between these factors, such as origin and destination airports' flight delays.
- Develop insights such as:
  - Airline performance comparison.
  - Delays caused by certain airports more than others.
  - Delays caused in specific time frames.

By delving into this rich dataset, we seek to uncover patterns and relationships that can shed light on the complexities of flight delays and pave the way for a more efficient and reliable air travel experience in the USA.

## About the Dataset: Flight Delay Dataset

This project utilizes a comprehensive dataset ([Flight Delay Dataset](https://www.kaggle.com/datasets/arvindnagaonkar/flight-delay/data)) encompassing real-time data about domestic flights within the USA from 2018 to April 2024.
The data focuses specifically on delays, excluding cancellations and diverted flights.
By analyzing this data, we aim to uncover the key factors contributing to flight delays and gain valuable insights for improving on-time performance in the air travel industry.

## Technologies / Tools

- Containerization: Docker
- Cloud: GCP 
- Infrastructure as code (IaC): Terraform
- Workflow orchestration: Mage-AI
- Data Warehouse: BigQuery
- Batch processing: Spark (with MageAI)
- IDE: VS Code
- Language: Python , SQL 
- Visualization: Google Looker Studio

## Project Architecture

The end-to-end data pipeline includes the following steps:

- Kaggle dataset is downloaded into the Google VM.
- The raw Parquet file is uploaded to the GCS bucket as a data lake.
- Using the Mage+Spark Image on Docker, the data is transformed and cleaned, creating new dataframes through Spark SQL & PySpark. These new dataframes are stored in different folders with partitions. This step is crucial as the dataset contains over 30 million rows.
- The transformed dataframes are uploaded to the GCS bucket and subsequently pushed to BigQuery as tables (data warehouse).
- Tables in BigQuery are queried, partitioned by year, and clustered for optimized performance. These tables will serve as the foundation for creating new tables, which will ultimately be used for visualizations.



## Link to the Dashboard

[Looker Dashboard](https://lookerstudio.google.com/reporting/b2519cc7-0b02-496b-9caa-3e3eaf65916b)

## Setting Up the AirDelayAnalyzer Project

### Project Setup: Google Cloud Platform (GCP)

#### 1. Create a GCP Project:

- If you don't have a GCP project already, head to the [GCP Console](https://console.cloud.google.com/) and create one.
- Note down your project ID, as you'll need it later.

#### 2. Enable Necessary APIs:

- Go to the [GCP APIs & Services Dashboard](https://console.cloud.google.com/apis/dashboard) in the GCP Console.
- Enable the following APIs (if not already enabled):
  - Google Cloud Storage API
  - BigQuery API
  - Cloud Dataflow API (if using Spark for data processing)

#### 3. Create Service Account Credentials:

- In the GCP Console, navigate to the [IAM & Admin](https://console.cloud.google.com/iam-admin) section.
- Create a service account with appropriate permissions for accessing Cloud Storage and BigQuery.
- Download the JSON key file (e.g., keys.json) associated with the service account for authentication later.

### Setting Up the Virtual Machine (VM)

#### 1. Create a Cloud Compute Engine (GCE) VM Instance:

- Use the GCP Console or the `gcloud` command-line tool to create a VM instance.
- Choose a machine type with sufficient resources (e.g., 8 cores recommended for data processing).
- Select a startup script that installs the necessary software packages.

#### 2. Connect to the VM:

- Use an SSH client to connect to your VM instance.

### Installing Dependencies (These are alreadu included in the dockerfile when setting up the MAGE+spark Image)

#### 1. Install Java (Would not need but still can download):

- Follow the official instructions for setting up Java on your specific VM operating system.
- Verify the installation by running `java -version` in your terminal.

#### 2. Install Apache Spark (Would not need but still can download):

- Download the latest stable Spark release from the [Spark website](https://spark.apache.org/downloads.html).
- Extract the downloaded archive to a directory on your VM.
- Set up environment variables in your shell's configuration file to point to the Spark installation.
- Reload the configuration file (`source .bashrc`) and verify the Spark installation.

### Downloading Mage+Spark and Running Docker Image 

#### 1. Obtain Dockerfile:

- Download the [Dockerfile](https://github.com/PD013/AirDelayAnalyzer/blob/main/Dockerfile) provided

#### 2. Build and Run the Docker Image:

- Open a VM terminal in the directory containing the Dockerfile.
- Run the command to build and run the Docker image, mapping port 6789 on the container to port 6789 on your local machine, and mounting your current directory as `/home/src` within the container:
  
-           sudo docker run -it --name spark_de-project -p 6789:6789 -v $(pwd):/home/src mage_spark /app/run_app.sh mage start de-project

- Here you can change the directories according to your need

  
### Configuring Mage (These files would be inside the pipeline folder)

#### 1. Edit Requirements File:

- Open the [`requirements.txt`](https://github.com/PD013/AirDelayAnalyzer/blob/main/requirements.txt) file in your project directory and add the necessary Python libraries using the pip syntax on the mage
-       pip install requirements.txt
  
#### 2. Modify Metadata YAML File:

- Open the [`metadata.yaml`](/metadata.yaml) file and update the `spark_config` section with the required configurations.
- Add or update the `sub_executor_env` list with `JAVA_HOME` and `PYTHONPATH`.
- Add the location of `keys.json` in the `others` section.
  

#### 3. Modify io.config.yaml File:

- Open the [`io.config.yaml`](/io.config.yaml)  file and update the `GOOGLE_SERVICE_ACC_KEY_FILEPATH` with the path to your `keys.json` file.

### Downloading and Running the Pipeline

#### 1. Download the Pipeline:

- Download the .zip file named [flight_delay_de_project_zip](/flight_delay_de_project_zip) from the GitHub repository.
- And just to view the blocks of the pipeline without downloading the ZIP checkout the [AirDelayAnalyzer Folder](/AirDelayAnalyzer)

#### 2. Modify Pipeline Blocks:

- Extract the contents of the .zip file and open the pipeline file.
- Navigate through the blocks and update the details such as bucket names, folder locations, and any other configurations according to your setup.

#### 3. Run the Pipeline:

- Once you've made the necessary changes, you can easily run the pipeline to reproduce the Flight Delay Exploration Project on your setup.


### Visualization
![Delay_by_Airline](https://github.com/PD013/AirDelayAnalyzer/blob/main/images/Delay_by_Airline.png))

![Delay_by_Location](https://github.com/PD013/AirDelayAnalyzer/blob/main/images/Delay_by_Location.png))

![Delay_by_time_period](https://github.com/PD013/AirDelayAnalyzer/assets/114251906/0d41bbb3-94c9-40e2-a19f-175fe5651bc0)


