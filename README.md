# AirDelayAnalyzer
## Problem Statement

Flight delays are a persistent issue in the aviation industry, causing inconvenience and frustration for passengers and financial losses for airlines.
With air travel becoming an essential part of modern life, on-time performance is paramount for both passengers and airlines. Delays disrupt travel itineraries and cause significant inconvenience. This project delves into flight data to shed light on the root causes of delays, pinpoint trends specific to airlines and airports, and ultimately contribute to a more streamlined air travel experience.

Understanding the root causes of these delays is essential for developing strategies to improve on-time performance. While various factors contribute to flight delays, their relative impact and interactions remain unclear.

This project addresses this challenge by leveraging a comprehensive flight delay dataset from Kaggle encompassing domestic flights within the USA. By analyzing this data, we aim to:

* Identify the key Citys that contribute to flight delays in the USA.
* Analyze the relationships between these factors, such as origin and destination airports flights delay.
* Develop insights such as :
  
       * Airline performance Comparison.
       * Delay caused by certian airports more than others.
       * Delays caused in specific time frames. 

By delving into this rich dataset, we seek to uncover patterns and relationships that can shed light on the complexities of flight delays and pave the way for a more efficient and reliable air travel experience in the USA.

## About the Dataset : Flight Delay Dataset

This project utilizes a comprehensive dataset ([Flight Delay Dataset](https://www.kaggle.com/datasets/arvindnagaonkar/flight-delay/data)) encompassing real time data about the domestic flights within the USA from 2018 to April 2024. 

The data focuses specifically on delays, excluding cancellations and diverted flights.

By analyzing this data, we aim to uncover the key factors contributing to flight delays and gain valuable insights for improving on-time performance in the air travel industry.

## Technologies / Tools

* Containerisation : Docker
* Cloud : GCP
* Infrastructure as code (IaC) : Terraform
* Workflow orchestration : Mage-ai
* Data Warehouse : BigQuery
* Batch processing : spark SQL
* IDE : VS Code, Jupyter Notebook
* Language : Python
* Visualisation : Google Looker Studio

## Project Architecture

The end-to-end data pipeline includes the following steps:

- Kaggle dataset is downloaded into the Google VM.
- The raw Parquet file is uploaded to the GCS bucket as a data lake.
- Using the Mage+Spark Image on Docker, the data is transformed and cleaned, creating new dataframes through Spark SQL & PySpark. These new dataframes are stored in different folders with partitions. This step is crucial as the dataset contains over 30 million rows.
- The transformed dataframes are uploaded to the GCS bucket and subsequently pushed to BigQuery as tables (data warehouse).
- Tables in BigQuery are queried, partitioned by year, and clustered for optimized performance. These tables will serve as the foundation for creating new tables, which will ultimately be used for visualizations.



## You can find the detailed Architecture on the diagram below:
![Project Architecture](https://github.com/PD013/AirDelayAnalyzer/assets/114251906/2dbca52d-7c88-4671-80d3-62ac9d6f4f84)



## Link to the Dashboard :- 
  [Looker Dashboard](https://lookerstudio.google.com/reporting/b2519cc7-0b02-496b-9caa-3e3eaf65916b)


