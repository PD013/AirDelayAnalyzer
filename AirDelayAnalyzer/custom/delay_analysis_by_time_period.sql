CREATE OR REPLACE TABLE `dtc-de-course-412810.project.delay_by_time_period_partitioned_clustered`
PARTITION BY DATE_TRUNC(date_partition_col, YEAR)   
CLUSTER BY year, month  
AS
SELECT 
  td.year,
  td.month,
  -- Add a new column for partition
  tp.crs_dep_time_hour_dis AS departure_period,
  td.total_delay AS total_delay,
  DATE(year, month, 1) AS date_partition_col
FROM `dtc-de-course-412810.project.total_delay` td
INNER JOIN `dtc-de-course-412810.project.time_periods` tp
  ON tp.unique_id = td.unique_id;


-- THESE Queries would create a new table which will be used for visualizations