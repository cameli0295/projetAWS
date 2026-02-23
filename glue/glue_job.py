import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

input_path = "s3://data-project-m2-master/raw/sales_raw.csv"
output_path = "s3://data-project-m2-master/processed/sales_cleaned/"

# 1) Read raw CSV
raw_df = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)

# 2) Rename columns to normalized snake_case
renamed_df = (
    raw_df.withColumnRenamed("buyerId", "buyerid")
    .withColumnRenamed("eventId", "eventid")
    .withColumnRenamed("qtySold", "qtysold")
    .withColumnRenamed("pricePaid", "pricepaid")
)

# 3) Remove rows with null values on required columns
required_columns = ["buyerid", "eventid", "qtysold", "pricepaid"]
non_null_df = renamed_df.dropna(subset=required_columns)

# 4) Cast types
typed_df = (
    non_null_df.withColumn("buyerid", F.col("buyerid").cast("int"))
    .withColumn("eventid", F.col("eventid").cast("int"))
    .withColumn("qtysold", F.col("qtysold").cast("int"))
    .withColumn("pricepaid", F.col("pricepaid").cast("decimal(10,2)"))
)

# Remove rows where casting failed
typed_non_null_df = typed_df.dropna(subset=required_columns)

# 5) Remove duplicates
dedup_df = typed_non_null_df.dropDuplicates()

# 6) Add computed column total_price
final_df = dedup_df.withColumn(
    "total_price", (F.col("qtysold") * F.col("pricepaid")).cast("decimal(10,2)")
)

# 7) Write cleaned dataset as Parquet for Redshift COPY
final_df.write.mode("overwrite").parquet(output_path)

job.commit()
