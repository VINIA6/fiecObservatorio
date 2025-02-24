-- Criação da tabela Atracacao
CREATE TABLE Atracacao (
    IDAtracacao BIGINT PRIMARY KEY,
    CDTUP VARCHAR(20),
    IDBerco VARCHAR(20),
    Berco VARCHAR(50),
    Porto_Atracacao VARCHAR(100),
    Apelido_Instalacao_Portuaria VARCHAR(100),
    Complexo_Portuario VARCHAR(100),
    Tipo_Autoridade_Portuaria VARCHAR(50),
    Data_Atracacao DATETIME,
    Data_Chegada DATETIME,
    Data_Desatracacao DATETIME,
    Data_Inicio_Operacao DATETIME,
    Data_Termino_Operacao DATETIME,
    Ano VARCHAR(4),
    Mes VARCHAR(2),
    Tipo_Operacao VARCHAR(50),
    Tipo_Navegacao_Atracacao VARCHAR(50),
    Nacionalidade_Armador VARCHAR(50),
    FlagMCOperacaoAtracacao VARCHAR(10),
    Terminal VARCHAR(150),
    Municipio VARCHAR(100),
    UF VARCHAR(2),
    SGUF VARCHAR(2),
    Regiao_Geografica VARCHAR(20),
    Nº_Capitania VARCHAR(20),
    Nº_IMO VARCHAR(20),
    TEsperaAtracacao FLOAT,
    TEsperaInicioPeriodo FLOAT,
    TOperacao FLOAT,
    TEsperaDesatracacao FLOAT,
    TAtracado FLOAT,
    TEstadia FLOAT
);

-- Criação da tabela Carga
CREATE TABLE Carga (
    IDCarga BIGINT PRIMARY KEY,
    IDAtracacao BIGINT,
    Origem NVARCHAR(100),
    Destino NVARCHAR(100),
    CDMercadoria NVARCHAR(50),
    NaturezaCarga NVARCHAR(50),
    TipoOperacao NVARCHAR(50),
    Carga_Geral FLOAT,
    Granel_Solido FLOAT,
    Granel_Liquido FLOAT,
    Conteiner FLOAT,
    Peso_Carga_Bruta FLOAT,
    QTCarga FLOAT,
    Tipo_Navegacao NVARCHAR(50)
);

-- Criação da tabela Carga_Conteinerizada
CREATE TABLE Carga_Conteinerizada (
    IDCarga BIGINT PRIMARY KEY,
    IDAtracacao BIGINT,
    Tamanho NVARCHAR(10),
    Tipo NVARCHAR(50),
    Estado NVARCHAR(20),
    Quantidade FLOAT
);

-- Índices para melhorar a performance
CREATE INDEX idx_data_atracacao ON Atracacao(Data_Atracacao);
CREATE INDEX idx_porto ON Atracacao(Porto_Atracacao);
CREATE INDEX idx_berco ON Atracacao(Berco);
CREATE INDEX idx_ano_mes ON Atracacao(Ano, Mes);

CREATE INDEX idx_carga_atracacao ON Carga(IDAtracacao);
CREATE INDEX idx_carga_mercadoria ON Carga(CDMercadoria);
CREATE INDEX idx_carga_natureza ON Carga(NaturezaCarga);

CREATE INDEX idx_conteiner_atracacao ON Carga_Conteinerizada(IDAtracacao);
CREATE INDEX idx_conteiner_tipo ON Carga_Conteinerizada(Tipo); 