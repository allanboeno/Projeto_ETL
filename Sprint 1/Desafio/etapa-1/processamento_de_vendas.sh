#!/bin/bash

data=$(date +"%Y%m%d")
data2=$(date +"%Y/%m/%d %H:%M")

# criando a pasta vendas e copiando o arquivo dos dados dentro dela
mkdir vendas
cp ecommerce/dados_de_vendas.csv vendas/dados_de_vendas.csv

# criando a pasta backup e copiando o arquivo dados dentro dela e renomeando
mkdir vendas/backup
cp ecommerce/dados_de_vendas.csv vendas/backup/dados-$data.csv 
mv vendas/backup/dados-$data.csv vendas/backup/backup-dados-$data.csv

# criando o arquivo de relatório
touch vendas/backup/relatorio$data.txt

echo "$data2" >> vendas/backup/relatorio$data.txt
echo "Data do primeiro registro de vendas: $(awk -F',' 'NR>1 {print $5}' ecommerce/dados_de_vendas.csv | sort -t '/' -k3,3 -k2,2 -k1,1 | head -n 1)" >> vendas/backup/relatorio$data.txt
echo "Data do ultimo registro de vendas: $(awk -F',' 'NR>1 {print $5}' ecommerce/dados_de_vendas.csv | sort -r -t '/' -k3,3 -k2,2 -k1,1 | head -n 1)" >> vendas/backup/relatorio$data.txt
echo "Quantidade total de itens diferentes vendidos: $(awk -F ',' 'NR>1 {print $1}' ecommerce/dados_de_vendas.csv | wc -l)" >> vendas/backup/relatorio$data.txt
echo "As 10 primeiras linhas do arquivo dados_de_vendas.csv: \n$(head -n 10 vendas/backup/backup-dados-$data.csv)" >> vendas/backup/relatorio$data.txt

# zipando os arquivos de backup e removendo o arquivo de dados de vendas
zip -j vendas/backup/backup-dados-$data.zip vendas/backup/backup-dados-$data.csv
rm vendas/backup/backup-dados-$data.csv vendas/dados_de_vendas.csv

