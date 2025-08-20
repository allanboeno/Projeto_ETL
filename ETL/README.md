# ETL - Data Lake TMDB (Game of Thrones)

Esta pasta contém todos os **códigos e scripts relacionados ao processo de ETL** do Data Lake para a série **Game of Thrones**, utilizando dados da API do **TMDB**.  

O objetivo é demonstrar o fluxo completo de **Extração, Transformação e Carga (ETL)** na AWS, preparando os dados para análises e dashboards no **Amazon QuickSight**.

---

## Estrutura da Pasta

```bash
ETL/
 ├── raw/       # Scripts Lambda para extração de dados da API TMDB
 ├── trusted/   # Scripts Glue para transformação e limpeza dos dados
 └── refined/   # Scripts Glue para modelagem dimensional e preparação para 
```

## 🚀 Fluxo do ETL

1. **Raw Zone** (Extração) 🟢  
   - Funções AWS Lambda conectam à API TMDB.  
   - Extraem dados de episódios e atores da série.  
   - Armazenam os dados em JSON na Raw Zone do S3.

2. **Trusted Zone** (Transformação) 🟡  
   - Jobs AWS Glue leem os JSONs da Raw Zone.  
   - Aplicam limpeza e padronização de dados.  
   - Gravam os dados em Parquet particionados por `processing_date`.

3. **Refined Zone** (Refinamento) 🔵  
   - Jobs AWS Glue leem os Parquets da Trusted Zone.  
   - Criam modelo dimensional: **tabela de fatos** e **tabelas de dimensões**.  
   - Gravam as tabelas finalizadas na Refined Zone, prontas para análise.

---

## 🛠 Tecnologias Utilizadas

- **AWS Lambda** – Extração de dados da API TMDB.  
- **AWS Glue (Spark)** – Transformação, limpeza e modelagem dimensional.  
- **AWS S3** – Armazenamento do Data Lake em camadas (Raw, Trusted, Refined).  
- **Amazon Athena** – Consulta SQL sobre os dados processados.  
- **Amazon QuickSight** – Criação de dashboards interativos.

---

## 📝 Observações

- Os scripts já estão comentados, permitindo fácil entendimento do código.  
- Cada camada do ETL possui seu próprio README detalhando **funcionalidades, parâmetros e fluxo de execução**.  
- O projeto segue boas práticas de arquitetura de Data Lake e pode ser reexecutado para atualizar os dados a qualquer momento.
