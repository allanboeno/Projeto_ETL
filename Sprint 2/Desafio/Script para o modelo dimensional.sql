CREATE VIEW dimensao_cliente AS
SELECT
    idCliente,
    nomeCliente,
    cidadeCliente,
    estadoCliente,
    paisCliente
FROM cliente;

CREATE VIEW dimensao_combustivel AS
SELECT
    idCombustivel,
    tipoCombustivel
FROM combustivel;

CREATE VIEW dimensao_carro AS
SELECT
    idCarro,
    kmCarro,
    classiCarro,
    marcaCarro,
    modeloCarro,
    anoCarro
FROM carro;

CREATE VIEW dimensao_vendedor AS
SELECT
    idVendedor,
    nomeVendedor,
    sexoVendedor,
    estadoVendedor
FROM vendedor;

CREATE VIEW dimensao_tempo AS
SELECT
	idlocacao,
    dataLocacao,
    horaLocacao,
    dataEntrega,
    horaEntrega
FROM locacao;

CREATE VIEW fato_locacao AS
SELECT
    idLocacao,
    idCliente,
    idCarro,
    idCombustivel,
    idVendedor,
    qtdDiaria,
    vlrDiaria
FROM locacao;

