import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, current_date
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, ArrayType

# Inicialização e configuração do job Glue
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_OUTPUT_PATH'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Esquemas dos arquivos JSON
schema_directors = StructType([
    StructField("Title", StringType(), True),
    StructField("Vote_Average", DoubleType(), True),
    StructField("Directors", ArrayType(
        StructType([
            StructField("Name", StringType(), True)
        ])
    ), True)
])

schema_series = StructType([
    StructField("Title", StringType(), True),
    StructField("Overview", StringType(), True),
    StructField("First_Air_Date", StringType(), True),
    StructField("Popularity", DoubleType(), True),
    StructField("Vote_Average", DoubleType(), True),
    StructField("Vote_Count", IntegerType(), True)
])

schema_top_movies = StructType([
    StructField("Title", StringType(), True),
    StructField("Popularity", DoubleType(), True),
    StructField("Vote_Average", DoubleType(), True),
    StructField("Vote_Count", IntegerType(), True)
])

# Caminho de entrada no S3 para os arquivos JSON
input_path = args['S3_INPUT_PATH']
# Ler e transformar os arquivos JSON com opção multiline=true
df_directors = spark.read.option("multiline", "true").schema(schema_directors).json(f"{input_path}/directors_drama_romance_movies.json")
df_series = spark.read.option("multiline", "true").schema(schema_series).json(f"{input_path}/series_imdb_tmdb.json")
df_top_movies = spark.read.option("multiline", "true").schema(schema_top_movies).json(f"{input_path}/top_drama_romance_movies.json")
df_top_tv_shows = spark.read.option("multiline", "true").schema(schema_top_movies).json(f"{input_path}/top_drama_tv_shows.json")

# Adicionar coluna com a data de processamento atual
current_date_str = current_date().alias("process_date")
df_directors = df_directors.withColumn("Directors", expr("transform(Directors, x -> regexp_replace(x.Name, '\\\\[|\\\\]', ''))")).withColumn("process_date", current_date_str)
df_series = df_series.withColumn("process_date", current_date_str)
df_top_movies = df_top_movies.withColumn("process_date", current_date_str)
df_top_tv_shows = df_top_tv_shows.withColumn("process_date", current_date_str)

# Remover a coluna Overview do DataFrame df_series
df_series = df_series.drop("Overview")

# Verificar dados lidos
print("Data in df_directors:")
df_directors.show()

print("Data in df_series:")
df_series.show()

print("Data in df_top_movies:")
df_top_movies.show()

print("Data in df_top_tv_shows:")
df_top_tv_shows.show()

# Salvar em formato Parquet particionado pela data de processamento
output_path = args['S3_OUTPUT_PATH']
df_directors.write.mode("overwrite").partitionBy("process_date").parquet(f"{output_path}/directors_drama_romance_movies")
df_series.write.mode("overwrite").partitionBy("process_date").parquet(f"{output_path}/series_imdb_tmdb")
df_top_movies.write.mode("overwrite").partitionBy("process_date").parquet(f"{output_path}/top_drama_romance_movies")
df_top_tv_shows.write.mode("overwrite").partitionBy("process_date").parquet(f"{output_path}/top_drama_tv_shows")

# Finaliza o job Glue
job.commit()
