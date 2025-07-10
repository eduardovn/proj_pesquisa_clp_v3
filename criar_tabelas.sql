CREATE SCHEMA banco_proj;
USE banco_proj;

CREATE TABLE peca_metalica_1 (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_contagem BIGINT NOT NULL,
    data_fabricacao DATE NOT NULL,
	tipo VARCHAR(40) NOT NULL,
	descricao VARCHAR(40) NOT NULL,
	tempo_ciclo TIME NOT NULL,
    peca1_status BOOL DEFAULT 1
);

CREATE TABLE peca_metalica_2 (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_contagem BIGINT NOT NULL,
    data_fabricacao DATE NOT NULL,
	tipo VARCHAR(40) NOT NULL,
	descricao VARCHAR(40) NOT NULL,
	tempo_ciclo TIME NOT NULL,
    peca2_status BOOL DEFAULT 1
);

CREATE TABLE peca_metalica_3 (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_contagem BIGINT NOT NULL,
    data_fabricacao DATE NOT NULL,
	tipo VARCHAR(40) NOT NULL,
	descricao VARCHAR(40) NOT NULL,
	tempo_ciclo TIME NOT NULL,
    peca3_status BOOL DEFAULT 1
);

CREATE TABLE peca_nao_metalica (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_contagem BIGINT NOT NULL,
    data_fabricacao DATE NOT NULL,
	tipo VARCHAR(40) NOT NULL,
	descricao VARCHAR(40) NOT NULL,
	tempo_ciclo TIME NOT NULL,
    peca_status BOOL DEFAULT 1
);