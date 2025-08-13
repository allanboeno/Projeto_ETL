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

# Etapa 6
df_select = df_nomes.select('Nomes', 'AnoNascimento').filter(col('AnoNascimento') > 2000)

# Etapa 8
df_count = df_nomes.filter(col('AnoNascimento').between(1980, 1994)).count()

df_nomes.show(10)
df_select.show(10)
print (f'Essa é quantidade de pessoas da geração millennials: {df_count}')