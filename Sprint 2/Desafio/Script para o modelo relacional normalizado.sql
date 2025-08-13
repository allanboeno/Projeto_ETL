CREATE TABLE cliente (
    idCliente INT PRIMARY KEY,
    nomeCliente VARCHAR(100),
    cidadeCliente VARCHAR(100),
    estadoCliente VARCHAR(100),
    paisCliente VARCHAR(100)
);

CREATE TABLE carro (
    idCarro INT PRIMARY KEY,
    kmCarro INT,
    classiCarro VARCHAR(20),
    marcaCarro VARCHAR(50),
    modeloCarro VARCHAR(50),
    anoCarro YEAR
);

CREATE TABLE vendedor (
    idVendedor INT PRIMARY KEY,
    nomeVendedor VARCHAR(100),
    sexoVendedor BOOLEAN,
    estadoVendedor VARCHAR(100)
);

CREATE TABLE combustivel (
    idCombustivel INT PRIMARY KEY,
    tipoCombustivel VARCHAR(50)
);

CREATE TABLE locacao (
    idLocacao INT PRIMARY KEY,
    idCliente INT,
    idCarro INT,
    idVendedor INT,
    idCombustivel INT,
    dataLocacao DATE,
    horaLocacao TIME,
    qtdDiaria INT,
    vlrDiaria DECIMAL(10, 2),
    dataEntrega DATE,
    horaEntrega TIME,
    FOREIGN KEY (idCliente) REFERENCES cliente(idCliente),
    FOREIGN KEY (idCarro) REFERENCES carro(idCarro),
    FOREIGN KEY (idVendedor) REFERENCES vendedor(idVendedor),
    FOREIGN KEY (idCombustivel) REFERENCES combustivel(idCombustivel)
);

INSERT INTO cliente (idCliente, nomeCliente, cidadeCliente, estadoCliente, paisCliente)
SELECT DISTINCT idCliente, nomeCliente, cidadeCliente, estadoCliente, paisCliente FROM tb_locacao;

INSERT INTO carro (idCarro, kmCarro, classiCarro, marcaCarro, modeloCarro, anoCarro)
SELECT DISTINCT idCarro, kmCarro, classiCarro, marcaCarro, modeloCarro, anoCarro FROM tb_locacao
group by idcarro;

INSERT INTO vendedor (idVendedor, nomeVendedor, sexoVendedor, estadoVendedor)
SELECT DISTINCT idVendedor, nomeVendedor, sexoVendedor, estadoVendedor FROM tb_locacao;

INSERT INTO combustivel (idCombustivel, tipoCombustivel)
SELECT DISTINCT idCombustivel, tipoCombustivel FROM tb_locacao;

INSERT INTO locacao (idLocacao, idCliente, idCarro, idVendedor, idCombustivel, dataLocacao, horaLocacao, qtdDiaria, vlrDiaria, dataEntrega, horaEntrega)
SELECT idLocacao, idCliente, idCarro, idVendedor, idCombustivel, dataLocacao, horaLocacao, qtdDiaria, vlrDiaria, dataEntrega, horaEntrega FROM tb_locacao;

DROP TABLE tb_locacao