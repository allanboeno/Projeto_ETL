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

* Criei várias funções lambda
* Adicionei a layer com as bibliotecas necessárias
* Dei acesso total ao s3

## Código do TMDB junto com IMDB

[Código Completo](tmdb_imdb_consulta.txt)

[Resultado json](series_imdb_tmdb.json)

Esse código foi feito para iterar sobre os ids do csv e buscar as informações somente sobre eles, ordenado pelo número de votos

### Importa as bibliotecas
    import json
    import pandas as pd
    import boto3
    from tmdbv3api import TMDb, TV, Find
    from io import StringIO
    import datetime

### Configura a API do TMDb
    tmdb = TMDb()
    tmdb.api_key = '1af2f2525262ee4cd8d7926245f782bd'

### Função para buscar detalhes de uma série de TV por IMDb ID usando a API do TMDb
    def get_tv_details(imdb_id):
        find = Find()
        search = find.find(external_id=imdb_id, external_source='imdb_id')
        if search and search.get('tv_results'):
            tmdb_id = search['tv_results'][0]['id']
            tv = TV()
            details = tv.details(tmdb_id)
            return {
                'Title': details.name,
                'Overview': details.overview,
                'First_Air_Date': details.first_air_date,
                'Popularity': details.popularity,
                'Vote_Average': details.vote_average,
                'Vote_Count': details.vote_count,
            }
        return None

### Função para ler um arquivo CSV do S3 e retornar um DataFrame
    def read_csv_from_s3(s3, bucket_name, key):
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        df = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')), sep='|', dtype={'id': str}, low_memory=False)
        print(f"Arquivo CSV lido com sucesso. Total de registros: {len(df)}")
        return df

### Função para filtrar séries de drama e retornar IDs únicos, ordenados pelo número de votos
    def filter_and_sort_drama_series(df):
        df_drama = df[df['genero'] == 'Drama'].drop_duplicates(subset=['id'])
        return df_drama.sort_values(by='numeroVotos', ascending=False)['id'].unique()

### Função para salvar os dados fornecidos em um arquivo JSON no S3
    def save_to_s3(s3, bucket_name, key, data):
        s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(data, indent=4, ensure_ascii=False))
        print(f"Arquivo JSON salvo em: s3://{bucket_name}/{key}")

### Função principal da Lambda
    def lambda_handler(event, context):
        s3 = boto3.client('s3')
        bucket_name = 'data-lake-do-allan'
        csv_key = 'Raw/Local/CSV/Series/2024/06/17/series.csv'

        # Ler e processar o arquivo CSV
        df_series = read_csv_from_s3(s3, bucket_name, csv_key)
        drama_series_ids = filter_and_sort_drama_series(df_series)
        
        # Buscar detalhes no TMDb
        series_info_tmdb = []
        processed_ids = set()
        for imdb_id in drama_series_ids:
            if len(series_info_tmdb) >= 50:
                break
            if imdb_id in processed_ids:
                continue
            details = get_tv_details(imdb_id)
            if details:
                series_info_tmdb.append(details)
                processed_ids.add(imdb_id)
                print(f"Detalhes obtidos para IMDb ID {imdb_id}: {details}")
            else:
                print(f"Detalhes não encontrados para IMDb ID {imdb_id}")
    
    # Salvar resultados no S3
    current_date = datetime.datetime.now().strftime("%Y/%m/%d")
    json_key = f"Raw/TMDB/JSON/{current_date}/series_imdb_tmdb.json"
    save_to_s3(s3, bucket_name, json_key, series_info_tmdb)

    return {
        'statusCode': 200,
        'body': json.dumps(f'Processamento concluído. Total de séries processadas: {len(series_info_tmdb)}')
    }

## Código top20 séries de TV

[Código Completo](top20_séries.txt)

[Resultado json](top_drama_tv_shows.json)

Lambda para obter o top20 séries de TV de Drama no TMDB

### Importa as bibliotecas
    import json
    import boto3
    import requests
    from datetime import datetime

### Configuração básica a chave de API do TMDB
    tmdb_api_key = '1af2f2525262ee4cd8d7926245f782bd'
    
### Função principal da Lambda
    def lambda_handler(event, context):
        # URL da API do TMDB para buscar séries de TV de Drama e Romance
        url = "https://api.themoviedb.org/3/discover/tv"
        
        # Parâmetros da requisição GET
        params = {
            'api_key': tmdb_api_key,
            'include_adult': False,
            'include_video': False,
            'language': 'en-US',
            'sort_by': 'vote_average.desc',
            'with_genres': '18',  # Drama
            'vote_count.gte': 200,  # Pelo menos 200 votos
            'page': 1
        }
        
        # Fazendo a requisição GET para a API do TMDB usando requests
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lança exceção se a requisição falhar
        
        # Convertendo a resposta JSON em um dicionário Python
        response_data = response.json()
        top_tv_shows = response_data.get('results', [])[:20]  # Limitando a 20 séries
        
        top_tv_shows_info = []
        for show in top_tv_shows:
            show_info = {
                'Title': show['name'],
                'Popularity': show['popularity'],
                'Vote_Average': show['vote_average'],
                'Vote_Count': show['vote_count'],
            }
            top_tv_shows_info.append(show_info)
        
        # Timestamp atual para o path de data
        current_date = datetime.now().strftime("%Y/%m/%d")
        
        # Nome do arquivo de saída com o padrão de path especificado
        output_filename = f"Raw/TMDB/JSON/{current_date}/top_drama_tv_shows.json"

### Salvar informações das séries de TV em um arquivo JSON no S3
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket='data-lake-do-allan', Key=output_filename, Body=json.dumps(top_tv_shows_info, indent=4, ensure_ascii=False))
    print(f"Arquivo JSON salvo em: s3://data-lake-do-allan/{output_filename}")
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Processamento concluído. Total de séries processadas: {len(top_tv_shows_info)}')
    }

## Código top20 filmes

[Código Completo](top20_filmes.txt)

[Resultado json](top_drama_romance_movies.json)

Lambda para obter o top20 filmes de Drama e Romance do TMDB

### Importa as bibliotecas
    import json
    import boto3
    import requests
    from datetime import datetime

### Configuração básica a chave de API do TMDB
    tmdb_api_key = '1af2f2525262ee4cd8d7926245f782bd'

### Função principal da Lambda
    # URL da API do TMDB para buscar filmes de Drama e Romance
    url = "https://api.themoviedb.org/3/discover/movie"
    
    # Parâmetros da requisição GET
    params = {
        'api_key': tmdb_api_key,
        'include_adult': False,
        'include_video': False,
        'language': 'en-US',
        'sort_by': 'vote_average.desc',
        'with_genres': '18,10749',  # Drama e Romance
        'vote_count.gte': 200,  # Pelo menos 200 votos
        'page': 1
    }
    
    # Fazendo a requisição GET para a API do TMDB usando requests
    response = requests.get(url, params=params)
    response.raise_for_status()  # Lança exceção se a requisição falhar
    
    # Convertendo a resposta JSON em um dicionário Python
    response_data = response.json()
    top_movies = response_data.get('results', [])[:20]  # Limitando a 20 filmes
    
    top_movies_info = []
    for movie in top_movies:
        movie_info = {
            'Title': movie['title'],
            'Popularity': movie['popularity'],
            'Vote_Average': movie['vote_average'],
            'Vote_Count': movie['vote_count']
        }
        top_movies_info.append(movie_info)
    # Timestamp atual para o path de data
    current_date = datetime.now().strftime("%Y/%m/%d")
    
    # Nome do arquivo de saída com o padrão de path especificado
    output_filename = f"Raw/TMDB/JSON/{current_date}/top_drama_romance_movies.json"

### Salvar informações dos filmes em um arquivo JSON no S3
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket='data-lake-do-allan', Key=output_filename, Body=json.dumps(top_movies_info, indent=4, ensure_ascii=False))
    print(f"Arquivo JSON salvo em: s3://seu-bucket-s3/{output_filename}")
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Processamento concluído. Total de filmes processados: {len(top_movies_info)}')
    }

## Código Diretores dos top20 filmes

[Código Completo](diretores_top20filmes.txt)

[Resultado json](directors_drama_romance_movies.json)

código para obter o nome dos diretores dos filmes de drama e romance do TMDB

### Importa as bibliotecas
    import json
    import boto3
    import requests
    from datetime import datetime

### Configuração básica a chave de API do TMDB
    tmdb_api_key = '1af2f2525262ee4cd8d7926245f782bd'

### Função principal da Lambda
    # URL da API do TMDB para buscar filmes de Drama e Romance
    url = "https://api.themoviedb.org/3/discover/movie"
    
    # Parâmetros da requisição GET
    params = {
        'api_key': tmdb_api_key,
        'include_adult': False,
        'include_video': False,
        'language': 'en-US',
        'sort_by': 'vote_average.desc',
        'with_genres': '18,10749',  # Drama e Romance
        'vote_count.gte': 200,  # Pelo menos 200 votos
        'page': 1
    }
    
    # Fazendo a requisição GET para a API do TMDB usando requests
    response = requests.get(url, params=params)
    response.raise_for_status()  # Lança exceção se a requisição falhar
    
    # Convertendo a resposta JSON em um dicionário Python
    response_data = response.json()
    top_movies = response_data.get('results', [])[:20]  # Limitando a 20 filmes
    
    top_movies_info = []
    for movie in top_movies:
        # URL para buscar os créditos do filme específico
        credits_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/credits"
        credits_params = {
            'api_key': tmdb_api_key,
            'language': 'en-US'
        }
        credits_response = requests.get(credits_url, params=credits_params)
        credits_response.raise_for_status()  # Lança exceção se a requisição falhar
        
        # Convertendo a resposta JSON dos créditos em um dicionário Python
        credits_data = credits_response.json()
        
        # Filtrando os diretores do filme
        directors = [
            {'Name': crew_member['name']}
            for crew_member in credits_data.get('crew', [])
            if crew_member['job'] == 'Director'
        ]
        
        # Construindo o dicionário de informações do filme
        movie_info = {
            'Title': movie['title'],
            'Vote_Average': movie['vote_average'],
            'Directors': directors
        }
        top_movies_info.append(movie_info)
    
    # Timestamp atual para o path de data
    current_date = datetime.now().strftime("%Y/%m/%d")
    
    # Nome do arquivo de saída com o padrão de path especificado
    output_filename = f"Raw/TMDB/JSON/{current_date}/directors_drama_romance_movies.json"
    
### Salvar informações dos filmes em um arquivo JSON no S3
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket='data-lake-do-allan', Key=output_filename, Body=json.dumps(top_movies_info, indent=4, ensure_ascii=False))
    print(f"Arquivo JSON salvo em: s3://data-lake-do-allan/{output_filename}")
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Processamento concluído. Total de filmes processados: {len(top_movies_info)}')
    }