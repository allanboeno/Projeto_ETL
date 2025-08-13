with open('actors.csv', 'r') as arquivo:
    linhas = arquivo.readlines()

contagem_filmes = {}

for linha in linhas[1:]:
    campos = linha.strip().split(',')
    filme = campos[4]
    contagem_filmes[filme] = contagem_filmes.get(filme, 0) + 1

contagem_ordenada = sorted(contagem_filmes.items(), key=lambda x: (-x[1], x[0]))

with open('etapa-4.txt', 'w') as arquivo_saida:
    for filme, quantidade in contagem_ordenada:
        resposta = f'O filme {filme} aparece {quantidade} vez(es) no dataset.\n'
        arquivo_saida.write(resposta)
