import os
import pandas as pd
import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import types
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.functions import col, substring ,concat, lit, to_date

from pyspark.sql.functions import split
from pyspark.sql.functions import when
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):
    spark = kwargs.get('spark')

    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    flight_schema = types.StructType(
        [
            types.StructField("year", types.LongType(), True),
            types.StructField("Month", types.LongType(), True),
            types.StructField("DayofMonth", types.LongType(), True),
            types.StructField("FlightDate", types.DateType(), True),
            types.StructField("Marketing_Airline_Network", types.StringType(), True),
            types.StructField("OriginCityName", types.StringType(), True),
            types.StructField("DestCityName", types.StringType(), True),
            types.StructField("CRSDepTime", types.LongType(), True),
            types.StructField("DepTime", types.DoubleType(), True),
            types.StructField("DepDelay", types.DoubleType(), True),
            types.StructField("DepDelayMinutes", types.DoubleType(), True),
            types.StructField("TaxiOut", types.DoubleType(), True),
            types.StructField("WheelsOff", types.DoubleType(), True),
            types.StructField("WheelsOn", types.DoubleType(), True),
            types.StructField("TaxiIn", types.DoubleType(), True),
            types.StructField("CRSArrTime", types.LongType(), True),
            types.StructField("ArrTime", types.DoubleType(), True),
            types.StructField("ArrDelay", types.DoubleType(), True),
            types.StructField("ArrDelayMinutes", types.DoubleType(), True),
            types.StructField("CRSElapsedTime", types.DoubleType(), True),
            types.StructField("ActualElapsedTime", types.DoubleType(), True),
            types.StructField("AirTime", types.DoubleType(), True),
            types.StructField("Distance", types.DoubleType(), True),
            types.StructField("DistanceGroup", types.LongType(), True),
            types.StructField("CarrierDelay", types.DoubleType(), True),
            types.StructField("WeatherDelay", types.DoubleType(), True),
            types.StructField("NASDelay", types.DoubleType(), True),
            types.StructField("SecurityDelay", types.DoubleType(), True),
            types.StructField("LateAircraftDelay", types.DoubleType(), True)
        ]
    )
    filepath = 'gs://de-project-0921/raw_data/Flight_Delay.parquet'
    # Specify your custom logic here
    df_all = spark.read \
        .option("header", "true") \
        .schema(flight_schema) \
        .parquet('./raw_data/Flight_Delay.parquet')

    # Here Adding A unique key


    #######
    df_all = df_all.withColumn("unique_id", monotonically_increasing_id().cast("double"))
    
    #######


    column_names = ["CRSDepTime", "WheelsOff", "CRSArrTime", "WheelsOn"]

    for col_name in column_names:
        # Extract hour and minute substrings
        df_all = df_all.withColumn(f"{col_name}Hour", substring(col(col_name), 1, 2).cast("integer"))
        df_all = df_all.withColumn(f"{col_name}Minute", substring(col(col_name), 3, 2).cast("integer"))

    columns_to_add= ["unique_id","CRSDepTimeHour", "WheelsOffHour", "CRSArrTimeHour", "WheelsOnHour",
                     "CRSDepTimeMinute", "WheelsOffMinute", "CRSArrTimeMinute", "WheelsOnMinute"]

    # Create a new DataFrame to store the columns to be removed
    df_time = df_all.select(columns_to_add)


    #########

    column_name = ["CRSDepTimeHour"]

    def time_dis(hour):
        return (when((hour > 3) & (hour <= 5), "EarlyMorning")
                .when((hour >= 6) & (hour <= 11), "Morning")
                .when((hour >= 12) & (hour <= 16), "Afternoon")
                .when((hour >= 17) & (hour < 21), "Evening")
                .otherwise("Night"))

    for column  in column_name:
        new_col = column  + "Dis"
        df_all = df_all.withColumn(new_col, time_dis(df_all[column]))
    
    df_time_periods = df_all.select("unique_id", "CRSDepTimeHourDis")

    #############


    places_of_add = ["unique_id", "OriginCity", "OriginState", "DestCity", "DestState"]

    df_all = df_all.withColumn("OriginCity", split(df_all["OriginCityName"], ", ").getItem(0))
    df_all = df_all.withColumn("OriginState", split(df_all["OriginCityName"], ", ").getItem(1))
    df_all = df_all.withColumn("DestCity", split(df_all["DestCityName"], ", ").getItem(0))
    df_all = df_all.withColumn("DestState", split(df_all["DestCityName"], ", ").getItem(1))

    df_place = df_all.select(places_of_add)


    ########







    df_all = df_all.withColumn("Total_Delay", col("DepDelay") + col("ArrDelay") + col("TaxiOut"))


    df_all = df_all.withColumn("Delay_Category", when(col("Total_Delay") <= 15, "Short Delay")
                             .when((col("Total_Delay") > 15) & (col("Total_Delay") <= 30), "Moderate Delay")
                             .otherwise("Long Delay"))


    df_total_delay = df_all.select("unique_id","year","Month","Total_Delay","Delay_Category")


    data = [("UA", "United Airlines"),
        ("DL", "Delta Airlines"),
        ("F9", "Frontier Airlines"),
        ("NK", "Spirit Airlines"),
        ("AA", "American Airlines"),
        ("WN", "Southwest Airlines"),
        ("AS", "Alaska Airlines"),
        ("HA", "Hawaiian Airlines"),
        ("VX", "Virgin America"),
        ("B6", "JetBlue Airways"),
        ("G4", "Allegiant Air")]
    
    df_airline_names = spark.createDataFrame(data)



    #####

    df_all.createOrReplaceTempView("flights")
    df_total_delay.createOrReplaceTempView("total_delay")
    df_airline_names.createOrReplaceTempView("airline_names")

    total_delay_by_year_airline = spark.sql("""
    SELECT 
    flights.year, flights.Month,
    airline_names._2 AS airline_name,
    AVG(total_delay.Total_Delay) AS avg_delay
    
    FROM flights
    
    JOIN total_delay ON flights.unique_id = total_delay.unique_id
    JOIN airline_names ON flights.Marketing_Airline_Network = airline_names._1
    
    GROUP BY flights.year, flights.Month, airline_names._2
    ORDER BY flights.year, flights.Month, avg_delay DESC

    """)

    columns_to_remove= ["CRSDepTimeHour", "WheelsOffHour", "CRSArrTimeHour", "WheelsOnHour",
                     "CRSDepTimeMinute", "WheelsOffMinute", "CRSArrTimeMinute",
                    "WheelsOnMinute","CRSDepTimeHourDis","CRSDepTime", "WheelsOff",
                    "CRSArrTime", "WheelsOn","OriginCityName", "DestCityName",
                    "FlightDate","Total_Delay"]


    df_all = df_all.drop(*columns_to_remove)



    output_base_dir = "./final_data/"

    # SAVING FILES IN THE LOCAL STORAGE
    # df_all.repartition(30).write.mode('overwrite').parquet(output_base_dir + "df_all")

    df_time.repartition(30).write.mode('overwrite').parquet(output_base_dir + "df_time")

    # Write df_time_periods
    df_time_periods.repartition(30).write.mode('overwrite').parquet(output_base_dir + "df_time_periods")

    # Write df_place
    df_place.repartition(30).write.mode('overwrite').parquet(output_base_dir + "df_place")

    # Write df_total_delay
    df_total_delay.repartition(30).write.mode('overwrite').parquet(output_base_dir + "df_total_delay")

    # Write df_airline_names
    df_airline_names.write.mode('overwrite').parquet(output_base_dir + "df_airline_names")

    # Write total_delay_by_year_airline
    total_delay_by_year_airline.repartition(30).write.mode('overwrite').parquet(output_base_dir + "total_delay_by_year_airline")




    print(df_all.printSchema())

    print(df_time.printSchema())

    print(df_time_periods.printSchema())

    print(df_place.printSchema())

    print(df_total_delay.printSchema())

    print(df_airline_names.printSchema())

    print(total_delay_by_year_airline.printSchema())

    folder_paths = []

# Iterate over folders in the directory
    # directory = '/home/preet/de-project/mage/final_data'
    directory = './final_data/'
    for folder_name in os.listdir(directory):
    # Construct full path for each folder
        folder_path = os.path.join(directory, folder_name)
    # Check if it's a directory
        if os.path.isdir(folder_path):
        # Add to the list of paths
             folder_paths.append(folder_path)


    # spark.stop()
    return folder_paths

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
