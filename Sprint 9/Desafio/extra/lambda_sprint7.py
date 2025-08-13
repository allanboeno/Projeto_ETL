import json
import requests
import boto3
from datetime import datetime

# Chave de API do TMDb
api_key = '1af2f2525262ee4cd8d7926245f782bd'

# Configurar cliente do S3
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # ID do TMDb para Game of Thrones
    tv_id = 1399

    # Função para obter dados de uma série pelo seu ID
    def get_tv_series_data(tv_id, api_key):
        url = f'https://api.themoviedb.org/3/tv/{tv_id}?api_key={api_key}&language=pt-BR'
        response = requests.get(url)
        return response.json()

    # Função para obter dados dos episódios de uma série
    def get_episodes_data(tv_id, season_number, api_key):
        url = f'https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}?api_key={api_key}&language=pt-BR'
        response = requests.get(url)
        return response.json()

    # Função para obter detalhes de um episódio específico
    def get_episode_details(tv_id, season_number, episode_number, api_key):
        url = f'https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}/episode/{episode_number}?api_key={api_key}&language=pt-BR'
        response = requests.get(url)
        return response.json()

    # Obter dados da série
    tv_series_data = get_tv_series_data(tv_id, api_key)

    # Obter dados de todas as temporadas e episódios
    seasons_data = []
    for season in range(1, tv_series_data['number_of_seasons'] + 1):
        season_data = get_episodes_data(tv_id, season, api_key)
        seasons_data.append(season_data)

    # Extrair informações dos episódios, diretores e atores
    episodes = []
    actors = []
    season_vote_counts = {}

    for season in seasons_data:
        total_vote_count = 0
        for episode in season['episodes']:
            episode_details = get_episode_details(tv_id, season['season_number'], episode['episode_number'], api_key)
            
            # Coletar diretores
            directors = [member['name'] for member in episode_details['crew'] if member['job'] == 'Director']
            
            # Coletar atores
            for member in episode_details['guest_stars']:
                actors.append({
                    'season': season['season_number'],
                    'episode_number': episode['episode_number'],
                    'actor': member['name'],
                    'character': member['character']
                })
            
            episodes.append({
                'season': season['season_number'],
                'episode_number': episode['episode_number'],
                'title': episode['name'],
                'vote_average': episode['vote_average'],
                'vote_count': episode['vote_count'],
                'air_date': episode['air_date'],
                'directors': ', '.join(directors)
            })
            total_vote_count += episode['vote_count']
        season_vote_counts[season['season_number']] = total_vote_count

    # Adicionar a contagem total de votos da temporada no DataFrame dos episódios
    for episode in episodes:
        episode['total_season_vote_count'] = season_vote_counts[episode['season']]

    # Obter data atual para estrutura de pastas
    today = datetime.today()
    year = today.strftime('%Y')
    month = today.strftime('%m')
    day = today.strftime('%d')

    # Nome dos arquivos JSON e caminho no S3
    episodes_file_name = 'game_of_thrones_episodes_with_season_vote_counts_and_directors.json'
    actors_file_name = 'game_of_thrones_actors.json'
    s3_bucket = 'data-lake-do-allan'
    episodes_s3_key = f'Raw/TMDB/JSON/{year}/{month}/{day}/{episodes_file_name}'
    actors_s3_key = f'Raw/TMDB/JSON/{year}/{month}/{day}/{actors_file_name}'

    # Salvar JSONs no S3
    s3_client.put_object(
        Bucket=s3_bucket,
        Key=episodes_s3_key,
        Body=json.dumps(episodes, ensure_ascii=False),
        ContentType='application/json'
    )

    s3_client.put_object(
        Bucket=s3_bucket,
        Key=actors_s3_key,
        Body=json.dumps(actors, ensure_ascii=False),
        ContentType='application/json'
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'episodes_s3_key': episodes_s3_key,
            'actors_s3_key': actors_s3_key
        })
    }
