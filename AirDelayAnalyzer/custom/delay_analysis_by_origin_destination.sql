CREATE OR REPLACE TABLE `dtc-de-course-412810.project.delay_by_location_detailed`  -- Replace with your desired table name
PARTITION BY DATE_TRUNC(date_partition_col, YEAR)  -- Partition by date constructed from year and month
CLUSTER BY origin_city, destination_city  -- Cluster by origin and destination city
AS
SELECT
  td.year,
  td.month,
  all_data.day_of_month,  -- Added day_of_month
  dp.origin_city AS origin_city,
  dp.dest_city AS destination_city,
  td.Total_Delay,  -- Removed AVG()
  DATE(td.year, td.month, all_data.day_of_month) AS date_partition_col
FROM `dtc-de-course-412810.project.total_delay` td
INNER JOIN `dtc-de-course-412810.project.place` dp
  ON td.unique_id = dp.unique_id
INNER JOIN `dtc-de-course-412810.project.All` all_data  -- Assuming the table name is 'All'
  ON td.unique_id = all_data.unique_id
WHERE dp.origin_city <> dp.dest_city;  -- Added WHERE clause to exclude same city pairs

