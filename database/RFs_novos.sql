-- =====================================================================
-- Guia Turistico Gamificado com IA
-- Migracao do banco (MySQL 8 / Railway) - RF06 a RF09
-- Pre-requisito: tabelas usuario e monumentos ja existentes (RF01-RF05)
-- Executar uma unica vez, na ordem abaixo.
-- =====================================================================
USE railway;

SET NAMES utf8mb4;

-- ---------------------------------------------------------------------
-- 1. Alteracao em tabela existente (RF06 - mapa e geolocalizacao)
--    Colunas aceitam NULL para nao quebrar monumentos ja cadastrados;
--    preencha as coordenadas e depois, se quiser, torne-as NOT NULL.
-- ---------------------------------------------------------------------
ALTER TABLE monumentos
  ADD COLUMN latitude  DECIMAL(9,6) NULL,
  ADD COLUMN longitude DECIMAL(9,6) NULL;

-- ---------------------------------------------------------------------
-- 2. Trilhas e missoes (RF08)
-- ---------------------------------------------------------------------
CREATE TABLE trilha (
  id_trilha        INT NOT NULL AUTO_INCREMENT,
  nome_trilha      VARCHAR(150) NOT NULL,
  descricao_trilha VARCHAR(500) NULL,
  tema             VARCHAR(100) NULL,
  PRIMARY KEY (id_trilha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE trilha_monumento (
  id_trilha_monumento INT NOT NULL AUTO_INCREMENT,
  id_trilha           INT NOT NULL,
  id_monumento        INT NOT NULL,
  ordem               INT NOT NULL,
  PRIMARY KEY (id_trilha_monumento),
  UNIQUE KEY uq_trilha_monumento (id_trilha, id_monumento),
  UNIQUE KEY uq_trilha_ordem (id_trilha, ordem),
  CONSTRAINT fk_tm_trilha    FOREIGN KEY (id_trilha)    REFERENCES trilha (id_trilha)        ON DELETE CASCADE,
  CONSTRAINT fk_tm_monumento FOREIGN KEY (id_monumento) REFERENCES monumentos (id_monumento) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE missao (
  id_missao        INT NOT NULL AUTO_INCREMENT,
  id_monumento     INT NOT NULL,
  descricao_missao VARCHAR(500) NOT NULL,
  tipo_missao      VARCHAR(50)  NULL,
  raio_metros      INT NOT NULL DEFAULT 200,
  PRIMARY KEY (id_missao),
  CONSTRAINT fk_missao_monumento FOREIGN KEY (id_monumento) REFERENCES monumentos (id_monumento) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE usuario_trilha (
  id_usuario_trilha INT NOT NULL AUTO_INCREMENT,
  id_usuario        INT NOT NULL,
  id_trilha         INT NOT NULL,
  status            ENUM('em_andamento','concluida') NOT NULL DEFAULT 'em_andamento',
  data_inicio       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  data_conclusao    DATETIME NULL,
  PRIMARY KEY (id_usuario_trilha),
  UNIQUE KEY uq_usuario_trilha (id_usuario, id_trilha),
  CONSTRAINT fk_ut_usuario FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario) ON DELETE CASCADE,
  CONSTRAINT fk_ut_trilha  FOREIGN KEY (id_trilha)  REFERENCES trilha (id_trilha)   ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE usuario_missao (
  id_usuario_missao INT NOT NULL AUTO_INCREMENT,
  id_usuario        INT NOT NULL,
  id_missao         INT NOT NULL,
  data_conclusao    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_usuario_missao),
  UNIQUE KEY uq_usuario_missao (id_usuario, id_missao),
  CONSTRAINT fk_um_usuario FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario) ON DELETE CASCADE,
  CONSTRAINT fk_um_missao  FOREIGN KEY (id_missao)  REFERENCES missao (id_missao)   ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------
-- 3. Narrativas curtas "pilulas de lore" (RF07) e diario (RF09)
--    Cada monumento tem 3 a 5 variantes pre-geradas pela IA (uma vez),
--    revisadas pelo time (aprovada = 1) e sorteadas na hora da visita.
--    Se voce JA executou a versao anterior deste script, rode antes:
--    DROP TABLE usuario_narrativa;
-- ---------------------------------------------------------------------
CREATE TABLE narrativa_monumento (
  id_narrativa_monumento INT NOT NULL AUTO_INCREMENT,
  id_monumento           INT NOT NULL,
  variante               TINYINT UNSIGNED NOT NULL,
  texto_narrativa        VARCHAR(400) NOT NULL,   -- pilula curta (~50 palavras)
  desafio                VARCHAR(200) NULL,       -- desafio de uma frase
  aprovada               TINYINT(1) NOT NULL DEFAULT 0,  -- 1 = revisada, pode ser exibida
  data_geracao           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_narrativa_monumento),
  UNIQUE KEY uq_narrativa_variante (id_monumento, variante),
  CONSTRAINT fk_nm_monumento FOREIGN KEY (id_monumento) REFERENCES monumentos (id_monumento) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE usuario_favorito (
  id_favorito   INT NOT NULL AUTO_INCREMENT,
  id_usuario    INT NOT NULL,
  id_monumento  INT NOT NULL,
  data_favorito DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_favorito),
  UNIQUE KEY uq_usuario_favorito (id_usuario, id_monumento),
  CONSTRAINT fk_uf_usuario   FOREIGN KEY (id_usuario)   REFERENCES usuario (id_usuario)        ON DELETE CASCADE,
  CONSTRAINT fk_uf_monumento FOREIGN KEY (id_monumento) REFERENCES monumentos (id_monumento)   ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE usuario_narrativa (
  id_usuario_narrativa   INT NOT NULL AUTO_INCREMENT,
  id_usuario             INT NOT NULL,
  id_narrativa_monumento INT NOT NULL,
  data_salvamento        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_usuario_narrativa),
  UNIQUE KEY uq_usuario_narrativa (id_usuario, id_narrativa_monumento),
  CONSTRAINT fk_un_usuario    FOREIGN KEY (id_usuario)             REFERENCES usuario (id_usuario)                           ON DELETE CASCADE,
  CONSTRAINT fk_un_narrativa  FOREIGN KEY (id_narrativa_monumento) REFERENCES narrativa_monumento (id_narrativa_monumento)  ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------
-- 4. VERIFICACOES OPCIONAIS nas tabelas existentes (descomente se faltar)
--    Rode antes: SHOW CREATE TABLE usuario_conquista; SHOW CREATE TABLE usuario_brindes;
-- ---------------------------------------------------------------------
-- RF03 - trava anti-fraude (um resgate por usuario e monumento):
-- ALTER TABLE usuario_conquista
--   ADD UNIQUE KEY uq_usuario_monumento (id_usuario, id_monumento);

-- Sugestao: impedir o mesmo brinde duplicado para o mesmo usuario:
-- ALTER TABLE usuario_brindes
--   ADD UNIQUE KEY uq_usuario_brinde (id_usuario, brinde_id);

-- Opcional: base de fatos para a IA gerar as pilulas, caso a
-- descricao_monumento seja curta demais.
-- ALTER TABLE monumentos ADD COLUMN fatos_base TEXT NULL;