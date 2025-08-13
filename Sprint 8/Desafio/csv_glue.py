import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, cast
from pyspark.sql.types import IntegerType, DoubleType

## @params: [JOB_NAME, S3_INPUT_PATH_MOVIES, S3_INPUT_PATH_SERIES, S3_OUTPUT_PATH]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH_MOVIES', 'S3_INPUT_PATH_SERIES', 'S3_OUTPUT_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
job.commit()

# Caminhos de entrada no S3 para os arquivos CSV de filmes e séries
input_path_movies = args['S3_INPUT_PATH_MOVIES']
input_path_series = args['S3_INPUT_PATH_SERIES']

# Ler o arquivo CSV de filmes com a definição de esquema
df_movies = spark.read.option("header", "true").option("sep", "|").csv(input_path_movies)
df_movies = df_movies.withColumnRenamed("tituloPincipal", "tituloPrincipal")  # Corrigindo nome da coluna, se necessário

# Especificar tipos de colunas para filmes
df_movies = df_movies.select(
    col("id"),
    col("tituloPrincipal"),
    col("anoLancamento").cast(IntegerType()).alias("anoLancamento"),
    col("genero"),
    col("notaMedia").cast(DoubleType()).alias("notaMedia"),
    col("numeroVotos").cast(IntegerType()).alias("numeroVotos"),
    col("nomeArtista"),
    col("profissao")
)

# Ler o arquivo CSV de séries com a definição de esquema
df_series = spark.read.option("header", "true").option("sep", "|").csv(input_path_series)
df_series = df_series.withColumnRenamed("tituloPincipal", "tituloPrincipal")  # Corrigindo nome da coluna, se necessário

# Especificar tipos de colunas para séries
df_series = df_series.select(
    col("id"),
    col("tituloPrincipal"),
    col("anoLancamento").cast(IntegerType()).alias("anoLancamento"),
    col("anoTermino").cast(IntegerType()).alias("anoTermino"),
    col("genero"),
    col("notaMedia").cast(DoubleType()).alias("notaMedia"),
    col("numeroVotos").cast(IntegerType()).alias("numeroVotos"),
    col("nomeArtista"),
    col("profissao"),
    col("titulosMaisConhecidos")
)


# Selecionar colunas necessárias para os filmes
df_movies_selected = df_movies.select(
    "id",
    "tituloPrincipal",
    "anoLancamento",
    "genero",
    "notaMedia",
    "numeroVotos",
    "nomeArtista",
    "profissao"
)

# Selecionar colunas necessárias para as séries
df_series_selected = df_series.select(
    "id",
    "tituloPrincipal",
    "anoLancamento",
    "anoTermino",
    "genero",
    "notaMedia",
    "numeroVotos",
    "nomeArtista",
    "profissao",
    "titulosMaisConhecidos"
)

# Caminho de saída no S3 para os dados de filmes e séries
output_path_movies = f"{args['S3_OUTPUT_PATH']}/movies/movies_filtered"
output_path_series = f"{args['S3_OUTPUT_PATH']}/series/series_filtered"

# Salvar em formato Parquet
df_movies_selected.coalesce(1).write.mode("overwrite").parquet(output_path_movies)
df_series_selected.coalesce(1).write.mode("overwrite").parquet(output_path_series)

job.commit()