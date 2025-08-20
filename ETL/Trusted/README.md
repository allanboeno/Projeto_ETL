# Transformação - Trusted Zone (AWS Glue)

Este módulo contém o **AWS Glue Job** responsável por processar os dados brutos (Raw Zone) da série **Game of Thrones**, transformá-los em um formato estruturado e armazená-los na **Trusted Zone** do Data Lake (S3) em formato **Parquet**.

## 🔑 Principais Funcionalidades
- Leitura de arquivos **JSON** extraídos da Raw Zone:
  - `game_of_thrones_episodes_with_season_vote_counts_and_directors.json`
  - `game_of_thrones_actors.json`
- Adição de metadado de **data de processamento** (`processing_date`).
- Conversão dos DataFrames para **DynamicFrames** (Glue).
- Escrita em **Parquet** otimizado no S3.
- Particionamento por `processing_date` para consultas mais rápidas no **Athena**.

## ⚙️ Parâmetros do Script
- **JOB_NAME**: nome do job executado no Glue.
- **S3_INPUT_PATH**: caminho de entrada (Raw Zone).
- **S3_OUTPUT_PATH**: caminho de saída (Trusted Zone).

## 🚀 Fluxo de Execução
1. Leitura dos arquivos JSON da Raw Zone.
2. Enriquecimento dos dados com a data de processamento.
3. Conversão para DynamicFrame (Glue).
4. Escrita dos dados no S3 em formato Parquet, particionados por `processing_date`.
5. Commit do job no Glue.
