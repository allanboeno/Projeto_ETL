def converter_receita_bruta(receita_bruta):
    numero = ''.join(caractere for caractere in receita_bruta if caractere.isdigit() or caractere == '.')
    if numero and numero != '.':
        return float(numero)
    else:
        return 0.0
with open('actors.csv', 'r') as arquivo:
    linhas = arquivo.readlines()

linhas_ordenadas = sorted(linhas[1:], key=lambda linha: converter_receita_bruta(linha.strip().split(',')[1]), reverse=True)

with open('etapa-5.txt', 'w') as arquivo_saida:
    for linha in linhas_ordenadas:
        campos = linha.strip().split(',')
        ator = campos[0]
        receita_bruta = campos[1]
        arquivo_saida.write(f'{ator} ({receita_bruta})\n')