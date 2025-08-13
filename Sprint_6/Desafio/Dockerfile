FROM python:3.9

WORKDIR /bucket

RUN pip install boto3 pandas

RUN mkdir csv_files

COPY movies.csv /bucket/csv_files/movies.csv
COPY series.csv /bucket/csv_files/series.csv

COPY Script.py /bucket/Script.py

CMD ["python", "Script.py"]
