# Conteúdo

Aqui estão os códigos sql utilizados no desafio

# Explicação breve

Para normalizar, identifiquei as entidades da tabela, como Cliente, Carro, Combustível, Vendedor e Locação, e seus atributos, como nome, cidade, modelo do carro, etc. Depois criei uma tabela para cada entidade, finalizando ligando as tabelas por chaves estrangeiras

Para fazer a mudança para o modelo dimensional, defini a tabela locacao como fato e as outras como dimensões, adicionando mais uma mudança, tirando tudo relacionado a data e hora da tabela fato, colocando numa nova tabela "dimensao_tempo"
