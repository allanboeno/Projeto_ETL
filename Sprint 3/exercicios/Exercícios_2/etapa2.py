with open('actors.csv', 'r') as arquivo:
    linhas = arquivo.readlines()

total_bruto = 0
num_filmes = 0

for linha in linhas[1:]:
    campos = linha.strip().split(',')
    
    try:
        bruto = float(campos[5].strip())
    except ValueError:
        continue
    
    total_bruto += bruto
    num_filmes += 1

media_bruta = total_bruto / num_filmes

resposta = f'A média de receita bruta dos principais filmes é de ${media_bruta:.2f}.'

with open('etapa-2.txt', 'w') as arquivo_saida:
    arquivo_saida.write(resposta)