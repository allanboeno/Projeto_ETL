import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from pyspark.sql import functions as F
from datetime import datetime

# Inicialização do Glue e Spark
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# Parâmetros de entrada
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_OUTPUT_PATH'])
input_path = args['S3_INPUT_PATH']
output_path = args['S3_OUTPUT_PATH']
job_name = args['JOB_NAME']

# Inicialização do trabalho do Glue
job.init(job_name, args)

# Caminhos dos arquivos JSON
episodes_path = f'{input_path}game_of_thrones_episodes_with_season_vote_counts_and_directors.json'
actors_path = f'{input_path}game_of_thrones_actors.json'

# Leitura dos dados de episódios
episodes_df = spark.read.json(episodes_path)

# Leitura dos dados de atores
actors_df = spark.read.json(actors_path)

# Adicionar coluna de data de processamento
current_date = datetime.now().strftime('%Y-%m-%d')
episodes_df = episodes_df.withColumn('processing_date', F.lit(current_date))
actors_df = actors_df.withColumn('processing_date', F.lit(current_date))

# Converter para DynamicFrame
episodes_dyf = DynamicFrame.fromDF(episodes_df, glueContext, 'episodes_dyf')
actors_dyf = DynamicFrame.fromDF(actors_df, glueContext, 'actors_dyf')

# Caminhos de destino no S3
episodes_output_path = f'{output_path}game_of_thrones_episodes/'
actors_output_path = f'{output_path}game_of_thrones_actors/'

# Escrever os dados particionados por data de processamento
glueContext.write_dynamic_frame.from_options(
    frame=episodes_dyf,
    connection_type='s3',
    connection_options={
        'path': episodes_output_path,
        'partitionKeys': ['processing_date']
    },
    format='parquet'
)

glueContext.write_dynamic_frame.from_options(
    frame=actors_dyf,
    connection_type='s3',
    connection_options={
        'path': actors_output_path,
        'partitionKeys': ['processing_date']
    },
    format='parquet'
)

# Commit do trabalho do Glue
job.commit()
