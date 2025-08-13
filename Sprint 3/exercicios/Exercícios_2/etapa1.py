with open('actors.csv', 'r') as arquivo:
    linhas = arquivo.readlines()

max_filmes = 0
ator_com_max_filmes = ""

for linha in linhas[1:]:
    campos = linha.strip().split(',')
    ator = campos[0]
    num_filmes = int(float(campos[2].strip()))
    
    if num_filmes > max_filmes:
        max_filmes = num_filmes
        ator_com_max_filmes = ator

resposta = f'O ator/atrizes com o maior número de filmes é {ator_com_max_filmes}" com {max_filmes} filmes.'

with open('etapa-1.txt', 'w') as arquivo_saida:
    arquivo_saida.write(resposta)