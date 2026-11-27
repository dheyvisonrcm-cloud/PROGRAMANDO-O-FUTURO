
-- SCRIPT DE CRIAÇÃO DO BANCO DE DADOS (MVP - Programando o Futuro)
-- Autor: Dheyvison Raylan
-- Baseado no Modelo Lógico (BRModelo)

CREATE DATABASE IF NOT EXISTS programando_futuro;
USE programando_futuro;


CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    pontos_totais INT NOT NULL DEFAULT 0
);


CREATE TABLE monumentos (
    id_monumento INT AUTO_INCREMENT PRIMARY KEY,
    nome_monumento VARCHAR(255) NOT NULL,
    descricao_monumento VARCHAR(255),
    qrcode_hash VARCHAR(255) NOT NULL UNIQUE,
    pontos INT NOT NULL DEFAULT 10
);


CREATE TABLE brindes (
    brinde_id INT AUTO_INCREMENT PRIMARY KEY,
    id_monumento INT,
    imagem_url VARCHAR(255),
    nome_brinde VARCHAR(255) NOT NULL,
    CONSTRAINT fk_brindes_monumentos FOREIGN KEY (id_monumento)
        REFERENCES monumentos(id_monumento) ON DELETE SET NULL ON UPDATE CASCADE
);


-- O UNIQUE KEY abaixo garante a regra de "conquista inédita" (MVP RF04).
CREATE TABLE usuario_conquista (
    id_conquista INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_monumento INT NOT NULL,
    data_conquista DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_usuario_monumento (id_usuario, id_monumento),
    CONSTRAINT fk_conquista_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_conquista_monumento FOREIGN KEY (id_monumento)
        REFERENCES monumentos(id_monumento) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE usuario_brindes (
    id_usuario_brindes INT AUTO_INCREMENT PRIMARY KEY,
    brinde_id INT NOT NULL,
    id_usuario INT NOT NULL,
    data_resgate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_usuario_brindes_brinde FOREIGN KEY (brinde_id)
        REFERENCES brindes(brinde_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_usuario_brindes_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario) ON DELETE CASCADE ON UPDATE CASCADE
);