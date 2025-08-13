with open('actors.csv', 'r') as arquivo:
    linhas = arquivo.readlines()

maior_media = 0
ator_maior_media = ""

for linha in linhas[1:]:
    campos = linha.strip().split(',')
    
    ator = campos[0]
    media = float(campos[3].strip())
    
    if media > maior_media:
        maior_media = media
        ator_maior_media = ator

resposta = f'O ator/atriz com a maior média de receita por filme é "{ator_maior_media}" com uma média de ${maior_media:.2f}.'

with open('etapa-3.txt', 'w') as arquivo_saida:
    arquivo_saida.write(resposta)