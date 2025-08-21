# Extração - Raw Zone (AWS Lambda)

Este módulo contém a função **AWS Lambda** responsável por extrair os dados da série **Game of Thrones** diretamente da **API do TMDB** e armazená-los na **Raw Zone** do Data Lake (S3) em formato **JSON**.

## 🔑 Principais Funcionalidades
- Conexão com a API do TMDB usando `requests`.
- Extração de:
  - **Episódios** (nome, número, data, média de votos, diretores, total de votos da temporada).
  - **Atores convidados** (nome e personagem).
- Organização dos dados em dois arquivos JSON:
  - `game_of_thrones_episodes_with_season_vote_counts_and_directors.json`
  - `game_of_thrones_actors.json`
- Estrutura de particionamento no S3 por data (ano/mês/dia).
- Armazenamento no bucket: `s3://data-lake-do-allan/Raw/TMDB/JSON/{ano}/{mês}/{dia}/`

⚙️ Parâmetros do Script
-----------------------

* **API Key do TMDB**: já definida dentro do código (`api_key`).
* **tv_id**: ID da série no TMDB (Game of Thrones = `1399`).
* **Bucket S3**: `data-lake-do-allan`.

🚀 Fluxo de Execução
--------------------

1. Lambda é executado.
2. Faz chamadas à API do TMDB:
   * Dados gerais da série.
   * Temporadas e episódios.
   * Detalhes de cada episódio (diretores e atores).
3. Monta os objetos JSON de episódios e atores.
4. Salva no S3 dentro da pasta **Raw/TMDB/JSON/{ano}/{mês}/{dia}**.