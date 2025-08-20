# Refinamento - Refined Zone (AWS Glue)

Este módulo contém o **AWS Glue Job** responsável por transformar os dados da **Trusted Zone** em um modelo dimensional, pronto para análise e consumo via **Athena** e **QuickSight**.

## 🔑 Principais Funcionalidades
- Leitura de dados em **Parquet** da Trusted Zone:
  - `game_of_thrones_episodes/`
  - `game_of_thrones_actors/`
- Criação da **tabela de fatos**:
  - `fact_episodes` com informações de cada episódio (nota média, contagem de votos, diretores, etc.).
- Criação das **tabelas de dimensões**:
  - `dim_seasons` – informações de cada temporada.  
  - `dim_episodes` – informações de cada episódio.  
  - `dim_cast` – atores convidados e seus personagens, com IDs únicos.  
  - `dim_directors` – diretores com IDs únicos.  
  - `dim_dates` – informações de datas dos episódios (ano, mês, dia, ID da data).
- Adição de **data de processamento** (`processing_date`) nas tabelas de fato.
- Escrita das tabelas em **Parquet**, particionadas quando aplicável.

## 🖼 Modelo Multidimensional
Abaixo está a representação do modelo dimensional criado na Refined Zone:

![Modelo Multidimensional](evidencias/modelo_multidimensional.png)

## ⚙️ Parâmetros do Script
- **JOB_NAME**: nome do job executado no Glue.  
- **S3_INPUT_PATH**: caminho de entrada (Trusted Zone).  
- **S3_OUTPUT_PATH**: caminho de saída (Refined Zone).  

## 🚀 Fluxo de Execução
1. Leitura dos Parquets da Trusted Zone.  
2. Ajuste de tipos de dados para tabelas de fato e dimensões.  
3. Criação de IDs únicos para atores e diretores.  
4. Construção da tabela de datas (`dim_dates`).  
5. Escrita das tabelas no S3 na Refined Zone.  
