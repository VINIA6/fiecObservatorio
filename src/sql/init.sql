CREATE DATABASE ANTAQ;
GO
-- Criar o banco de dados ANTAQ se não existir
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'ANTAQ')
BEGIN
    CREATE DATABASE ANTAQ;
END
GO

USE ANTAQ;
GO

-- Criar tabela atracacao_fato
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'atracacao_fato')
BEGIN
    CREATE TABLE atracacao_fato (
        IDAtracacao INT PRIMARY KEY,
        TipoNavegacaoAtracacao VARCHAR(100),
        CDTUP VARCHAR(20),
        NacionalidadeArmador VARCHAR(100),
        IDBerco INT,
        FlagMCOperacaoAtracacao BIT,
        Berco VARCHAR(50),
        Terminal VARCHAR(100),
        PortoAtracacao VARCHAR(100),
        Municipio VARCHAR(100),
        ApelidoInstalacaoPortuaria VARCHAR(200),
        UF CHAR(2),
        ComplexoPortuario VARCHAR(100),
        SGUF VARCHAR(10),
        TipoAutoridadePortuaria VARCHAR(100),
        RegiaoGeografica VARCHAR(50),
        DataAtracacao DATETIME,
        DataChegada DATETIME,
        DataDesatracacao DATETIME,
        DataInicioOperacao DATETIME,
        DataTerminoOperacao DATETIME,
        AnoDataInicioOperacao INT,
        MesDataInicioOperacao INT,
        TipoOperacao VARCHAR(100),
        NCapitania VARCHAR(50),
        NIMO VARCHAR(20),
        TEsperaAtracacao DECIMAL(10,2),
        TEsperaInicioOp DECIMAL(10,2),
        TOperacao DECIMAL(10,2),
        TEsperaDesatracacao DECIMAL(10,2),
        TAtracado DECIMAL(10,2),
        TEstadia DECIMAL(10,2),
        created_at DATETIME DEFAULT GETDATE()
    );
END
GO

-- Criar tabela carga_fato
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'carga_fato')
BEGIN
    CREATE TABLE carga_fato (
        IDCarga INT PRIMARY KEY,
        IDAtracacao INT,
        FlagTransporteViaInterioir BIT,
        PercursoTransporteViasInteriores VARCHAR(200),
        OrigemPercursoTransporteInteriores VARCHAR(200),
        Destino VARCHAR(200),
        CDMercadoria VARCHAR(50),
        STSH2 VARCHAR(100),
        TipoOperacaoCarga VARCHAR(50),
        STSH4 VARCHAR(100),
        CargaGeralAcondicionamento VARCHAR(100),
        NaturezaCarga VARCHAR(100),
        ConteinerEstado VARCHAR(50),
        Sentido VARCHAR(50),
        TipoNavegacao VARCHAR(100),
        TEU DECIMAL(10,2),
        FlagAutorizacao BIT,
        QTCarga DECIMAL(15,2),
        FlagCabotagem BIT,
        VLPesoCargaBruta DECIMAL(15,2),
        FlagCabotagemMovimentacao BIT,
        AnoDataInicioOperacao INT,
        MesDataInicioOperacao INT,
        FlagConteinerTamanho VARCHAR(50),
        created_at DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (IDAtracacao) REFERENCES atracacao_fato(IDAtracacao)
    );
END
GO

-- Criar índices para melhor performance
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_atracacao_fato_DataInicioOperacao')
BEGIN
    CREATE INDEX IX_atracacao_fato_DataInicioOperacao 
    ON atracacao_fato(DataInicioOperacao);
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_carga_fato_IDAtracacao')
BEGIN
    CREATE INDEX IX_carga_fato_IDAtracacao 
    ON carga_fato(IDAtracacao);
END
GO

