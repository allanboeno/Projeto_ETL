# Etapa 1
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType
import random

spark = SparkSession \
                .builder \
                .master("local[*]")\
                .appName("Exercicio Intro") \
                .getOrCreate()

# Etapa 2
df_nomes = spark.read.text("/content/drive/MyDrive/Nomes gerados.txt").withColumnRenamed("value", "Nomes")
df_nomes.printSchema()

# Etapa 3
def random_escolaridade():
    escolaridade_opcoes = ["Fundamental", "Médio", "Superior"]
    return random.choice(escolaridade_opcoes)

# Etapa 4
def random_pais():
    pais_opcoes = [
        "Argentina", "Bolívia", "Brasil", "Chile", "Colômbia",
        "Equador", "Guiana", "Paraguai", "Peru",
        "Suriname", "Uruguai", "Venezuela", "Guiana Francesa"
    ]
    return random.choice(pais_opcoes)

# Etapa 5
def random_ano():
    anos = list(range(1945, 2011))
    return random.choice(anos)

random_escolaridade_udf = udf(random_escolaridade, StringType())
random_pais_udf = udf(random_pais, StringType())
random_ano_udf = udf(random_ano, StringType())

df_nomes = df_nomes.withColumn('Escolaridade', random_escolaridade_udf())
df_nomes = df_nomes.withColumn('Pais', random_pais_udf())
df_nomes = df_nomes.withColumn('AnoNascimento', random_ano_udf())

df_nomes.cache()

df_nomes.createOrReplaceTempView("nomes")

# Etapa 7
spark.sql("SELECT Nomes, AnoNascimento FROM nomes WHERE AnoNascimento > 2000").show(10)

# Etapa 9
spark.sql("SELECT COUNT(*) as Quantidade FROM nomes WHERE AnoNascimento > 1980 AND AnoNascimento < 1994").show()

# Etapa 10
spark.sql("""
    SELECT
        Pais,
        CASE
            WHEN AnoNascimento BETWEEN 1944 AND 1964 THEN 'Baby Boomers'
            WHEN AnoNascimento BETWEEN 1965 AND 1979 THEN 'Geração X'
            WHEN AnoNascimento BETWEEN 1980 AND 1994 THEN 'Millennials'
            WHEN AnoNascimento BETWEEN 1995 AND 2015 THEN 'Geração Z'
            ELSE 'Outros'
        END AS Geracao,
        COUNT(*) AS Quantidade
    FROM
        nomes
    GROUP BY
        Pais, Geracao
    ORDER BY
        Pais ASC, Geracao ASC, Quantidade DESC
""").show()
