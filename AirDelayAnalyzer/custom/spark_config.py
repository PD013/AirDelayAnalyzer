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

from mage_ai.data_preparation.repo_manager import RepoConfig, get_repo_path
from mage_ai.services.spark.config import SparkConfig
from pyspark.sql import SparkSession

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):




    # repo_config = RepoConfig(repo_path=get_repo_path())
    # spark_config = SparkConfig.load(config=repo_config.spark_config)
    spark = kwargs.get('spark')
    
    # spark = get_spark_session(spark_config)
    return(print(spark.sql('select 1'))) 



