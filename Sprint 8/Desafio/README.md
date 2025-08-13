# Desafio

## Objetivo

Explorar e analisar filmes e séries de drama/romance para extrair insights sobre avaliações, popularidade, tendências temporais e características dos diretores e elenco, utilizando dados do TMDB e IMDB.

## Perguntas

### Sobre os Filmes:

### Avaliações e Popularidade:
Quais são os filmes de drama/romance mais bem avaliados no TMDB e CSV (IMDB)?
Existe uma correlação entre a popularidade dos filmes e suas avaliações nas duas plataformas?

### Diretores:
Quais diretores são responsáveis pelos filmes de drama/romance mais bem avaliados? há algum filme na lista com mais de um diretor?

### Tendências Temporais:
Como a popularidade e a avaliação dos filmes de drama/romance evoluíram ao longo das décadas de acordo com o CSV (IMDB)?
Existem períodos específicos em que filmes de drama/romance receberam avaliações melhores ou piores?

### Personagens e Elenco:
Quais atores/atrizes mais frequentes em filmes de drama/romance tendem a receber melhores avaliações de acordo com o CSV (IMDB)?
Existe uma correlação entre o elenco e a popularidade ou avaliação dos filmes?

### Sobre as Séries:

### Avaliações e Popularidade:
Quais são as séries de drama mais bem avaliadas no TMDB?
Existe uma correlação entre a popularidade das séries e suas avaliações?

### Tendências Temporais:
Como a popularidade e a avaliação das séries de drama/romance mudaram ao longo do tempo de acordo com o CSV (IMDB)?
Existem anos ou períodos específicos em que as séries de drama/romance foram mais populares ou melhor avaliadas?

### Personagens e Elenco:
Quais atores/atrizes mais frequentes em séries de drama/romance tendem a receber melhores avaliações?
Existe uma correlação entre o elenco e a popularidade ou avaliação das séries?

### Análise Comparativa:
Comparação entre Filmes e Séries:

Filmes ou séries de drama/romance tendem a ser mais bem avaliados comparados a outros gêneros no CSV (IMDB)?
Existe uma diferença significativa na popularidade de filmes vs séries de drama/romance?

Discrepância de Avaliações:

Há uma diferença significativa entre as avaliações do TMDB e do IMDB para as mesmas séries de drama? Quais são os casos mais notáveis?

# Passos executados

* Criei o glue do csv, arrumei o nome de algumas colunas, defini o tipo delas e escolhi as colunas que seriam necessárias para responder as perguntas
* Criei 2 crawlers, 1 para séries e 1 para filmes
* Criei o glue do TMDB, criei os schemas para cada arquivo
* Criei 1 crawler para os dados do TMDB

## Código do Glue para o csv

[Código Completo](csv_glue.py)

Esse código foi feito para iterar sobre os ids do csv e buscar as informações no tmdb somente sobre eles, ordenado pelo número de votos

### Importa as bibliotecas e APIs
    import sys
    from awsglue.transforms import *
    from awsglue.utils import getResolvedOptions
    from pyspark.context import SparkContext
    from awsglue.context import GlueContext
    from awsglue.job import Job
    from pyspark.sql.functions import col, cast
    from pyspark.sql.types import IntegerType, DoubleType

### Configura o glue
    args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH_MOVIES', 'S3_INPUT_PATH_SERIES', 'S3_OUTPUT_PATH'])

    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args['JOB_NAME'], args)
    job.commit()

### Caminhos de entrada no S3 para os arquivos CSV de filmes e séries
    input_path_movies = args['S3_INPUT_PATH_MOVIES']
    input_path_series = args['S3_INPUT_PATH_SERIES']

### Ler o arquivo CSV de filmes com a definição de esquema
    df_movies = spark.read.option("header", "true").option("sep", "|").csv(input_path_movies)
    df_movies = df_movies.withColumnRenamed("tituloPincipal", "tituloPrincipal")  # Corrigindo nome da coluna

### Especificar tipos de colunas para filmes
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

### Ler o arquivo CSV de séries com a definição de esquema
    df_series = spark.read.option("header", "true").option("sep", "|").csv(input_path_series)
    df_series = df_series.withColumnRenamed("tituloPincipal", "tituloPrincipal")  # Corrigindo nome da coluna

### Especificar tipos de colunas para séries
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


### Selecionar colunas necessárias para os filmes
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

### Selecionar colunas necessárias para as séries
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

### Caminho de saída no S3 para os dados de filmes e séries
    output_path_movies = f"{args['S3_OUTPUT_PATH']}/movies/movies_filtered"
    output_path_series = f"{args['S3_OUTPUT_PATH']}/series/series_filtered"

### Salvar em formato Parquet
    df_movies_selected.coalesce(1).write.mode("overwrite").parquet(output_path_movies)
    df_series_selected.coalesce(1).write.mode("overwrite").parquet(output_path_series)

    job.commit()


## Código do Glue para o TMDB

[Código Completo](tmdb_glue.py)

### Importa as bibliotecas e APIs

    import sys
    from awsglue.transforms import *
    from awsglue.utils import getResolvedOptions
    from pyspark.context import SparkContext
    from awsglue.context import GlueContext
    from awsglue.job import Job
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, expr, current_date
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, ArrayType

### Configura o glue

    args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_OUTPUT_PATH'])
    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args['JOB_NAME'], args)

### Schema dos diretores

    schema_directors = StructType([
        StructField("Title", StringType(), True),
        StructField("Vote_Average", DoubleType(), True),
        StructField("Directors", ArrayType(
            StructType([
                StructField("Name", StringType(), True)
            ])
        ), True)
    ])

### Schema do tmdb com imdb

    schema_series = StructType([
        StructField("Title", StringType(), True),
        StructField("Overview", StringType(), True),
        StructField("First_Air_Date", StringType(), True),
        StructField("Popularity", DoubleType(), True),
        StructField("Vote_Average", DoubleType(), True),
        StructField("Vote_Count", IntegerType(), True)
    ])

### Schema dos top20 series e movies

    schema_top_movies = StructType([
        StructField("Title", StringType(), True),
        StructField("Popularity", DoubleType(), True),
        StructField("Vote_Average", DoubleType(), True),
        StructField("Vote_Count", IntegerType(), True)
    ])

### Caminho de entrada no S3 para os arquivos JSON

    input_path = args['S3_INPUT_PATH']

### Ler e transformar os arquivos JSON com opção multiline=true

    df_directors = spark.read.option("multiline", "true").schema(schema_directors).json(f"{input_path}/directors_drama_romance_movies.json")
    df_series = spark.read.option("multiline", "true").schema(schema_series).json(f"{input_path}/series_imdb_tmdb.json")
    df_top_movies = spark.read.option("multiline", "true").schema(schema_top_movies).json(f"{input_path}/top_drama_romance_movies.json")
    df_top_tv_shows = spark.read.option("multiline", "true").schema(schema_top_movies).json(f"{input_path}/top_drama_tv_shows.json")

### Adicionar coluna com a data de processamento atual

    current_date_str = current_date().alias("process_date")
    df_directors = df_directors.withColumn("Directors", expr("transform(Directors, x -> regexp_replace(x.Name, '\\\\[|\\\\]', ''))")).withColumn("process_date", current_date_str)
    df_series = df_series.withColumn("process_date", current_date_str)
    df_top_movies = df_top_movies.withColumn("process_date", current_date_str)
    df_top_tv_shows = df_top_tv_shows.withColumn("process_date", current_date_str)

### Remover a coluna Overview do DataFrame df_series

    df_series = df_series.drop("Overview")

### Verificar dados lidos
    print("Data in df_directors:")
    df_directors.show()

    print("Data in df_series:")
    df_series.show()

    print("Data in df_top_movies:")
    df_top_movies.show()

    print("Data in df_top_tv_shows:")
    df_top_tv_shows.show()

### Salvar em formato Parquet particionado pela data de processamento
    output_path = args['S3_OUTPUT_PATH']
    df_directors.write.mode("overwrite").partitionBy("process_date").parquet(f"{output_path}/directors_drama_romance_movies")
    df_series.write.mode("overwrite").partitionBy("process_date").parquet(f"{output_path}/series_imdb_tmdb")
    df_top_movies.write.mode("overwrite").partitionBy("process_date").parquet(f"{output_path}/top_drama_romance_movies")
    df_top_tv_shows.write.mode("overwrite").partitionBy("process_date").parquet(f"{output_path}/top_drama_tv_shows")

### Finaliza o job Glue
    job.commit()
