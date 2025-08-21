# Projeto de ETL com AWS e TMDB 🎬⚡

## 📌 Descrição
Este projeto consiste em um **pipeline ETL completo** construído na **AWS**, utilizando a **API do TMDB** como fonte de dados.  
Foi escolhida a série **Game of Thrones** 🐉 como caso de estudo, e a partir dela foram extraídos, transformados e carregados dados em um **Data Lake**.  
Por fim, as informações foram disponibilizadas em um **dashboard no Amazon QuickSight** para análise e visualização interativa.  

## 🚀 Fluxo do Projeto
1. **Extração**: Coleta de dados da API do TMDB com funções Lambda em Python.  
2. **Armazenamento**: Dados brutos armazenados no **Amazon S3 (Raw Zone)**.  
3. **Transformação**: Limpeza e normalização realizadas com **AWS Glue (Spark)**, estruturando os dados em formato **Parquet**.  
4. **Trusted/Refined Zone**: Organização dos dados no Data Lake para governança e consultas.  
5. **Consulta**: Exploração dos dados via **AWS Athena**.  
6. **Visualização**: Construção de **dashboards interativos** no **Amazon QuickSight**, permitindo insights sobre a série.  

## 🛠️ Tecnologias Utilizadas
- **Python**  
- **Apache Spark** (AWS Glue)  
- **Amazon S3** (Data Lake)  
- **AWS Lambda**  
- **AWS Glue**  
- **AWS Athena**  
- **Amazon QuickSight**  
- **TMDB API**  

## 📂 Estrutura do Projeto
```
├── ETL/ # Parte de Engenharia de Dados
│ ├── Raw/ # 📥 Funções para extração de dados da API TMDB
│ ├── Trusted/ # 🔄 Scripts Spark para transformação e limpeza dos dados
│ ├── Refined/ # 📊 Scripts para criação de datasets prontos para análise
│ ├── Evidencias/ # Pasta com as evidências do projeto
│ └── README.md # Documentação do projeto

├── BI/ # Parte de Business Intelligence
│ ├── Evidencias/ # Pasta com as evidências do projeto
│ └── README.md # Documentação do projeto


└── README.md # Documentação do projeto
```

## 📊 Principais Análises no Dashboard
- Variação da avaliação (média, mínimo e máximo) dos episódios ao longo das temporadas.
- Relação entre votos recebidos e notas atribuídas aos episódios.
- Ranking de diretores, com quantidade de episódios dirigidos e notas médias por temporada.
- Tabela interativa com principais dados (notas e votos) para explorar temporadas e episódios em detalhe.  

## 👤 Autor
Projeto desenvolvido por **Allan Gabriel** como estudo prático de **Engenharia de Dados e Cloud Computing**.  
