import boto3
import os
import pandas as pd
from datetime import datetime

session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN')
)

def upload_file(file_path, bucket_name, s3_path):
    s3 = session.client('s3')
    try:
        s3.upload_file(file_path, bucket_name, s3_path)
        print(f'Upload feito com sucesso {file_path} para o s3://{bucket_name}/{s3_path}')
    except Exception as e:
        print(f'Falha no upload {file_path} para o s3://{bucket_name}/{s3_path}: {e}')

def main():
    bucket_name = 'data-lake-do-allan'
    date = datetime.now().strftime('%Y/%m/%d')

    s3_movies = f'Raw/Local/CSV/Movies/{date}/movies.csv'
    s3_series = f'Raw/Local/CSV/Series/{date}/series.csv'

    print (pd.read_csv("/bucket/csv_files/movies.csv", delimiter='|'))
    print (pd.read_csv("/bucket/csv_files/series.csv", delimiter='|'))
    
    upload_file("/bucket/csv_files/movies.csv", bucket_name, s3_movies)
    upload_file("/bucket/csv_files/series.csv", bucket_name, s3_series)

if __name__ == '__main__':
    main()
