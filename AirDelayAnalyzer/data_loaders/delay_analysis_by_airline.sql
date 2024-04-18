CREATE OR REPLACE TABLE `dtc-de-course-412810.project.delay_by_airline_partitioned`  -- Replace with your desired table name
PARTITION BY DATE_TRUNC(date_partition_col, YEAR) -- Partition by date constructed from year and month
AS
SELECT
  *,  -- Select all existing columns
  DATE(year, month, 1) AS date_partition_col  -- Add a new column for partition
FROM `dtc-de-course-412810.project.total_delay_by_airline`;



