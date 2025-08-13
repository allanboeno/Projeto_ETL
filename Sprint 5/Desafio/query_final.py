import boto3

session = boto3.Session(profile_name='allan1')
s3 = session.client('s3')

bucket_name = 'sprint5-allan'
file_key = 'agenda-de-veiculos-demandas-normais-e-de-campov4.csv'

sql_expression = """SELECT
    MAX(CAST("N DE PASSAGEIROS" AS INT)),
    SUM(CHAR_LENGTH("N DE PASSAGEIROS")),
    CASE WHEN MAX(CAST("N DE PASSAGEIROS" AS INT)) > 40 THEN 'Muito' ELSE 'Pouco' END,
    UTCNOW()
    FROM s3object
    WHERE ORIGEM = 'REITORIA' OR ORIGEM = 'CRES' OR ORIGEM = 'LEM'
    """

response = s3.select_object_content(
    Bucket=bucket_name,
    Key=file_key,
    ExpressionType='SQL',
    Expression=sql_expression,
    InputSerialization={
        'CSV': {
            "FileHeaderInfo": "Use", 
            "AllowQuotedRecordDelimiter": True
        },
    },
    OutputSerialization={'CSV': {}},
)

for event in response['Payload']:
    if 'Records' in event:
        print(event['Records']['Payload'].decode('utf-8'))
