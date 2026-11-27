-- =====================================================================
-- Carga inicial do MVP (PostgreSQL / Neon)
-- 14 monumentos, 3 trilhas, 14 paradas, 3 missoes (200 pontos cada)
--
-- COMO RODAR: SQL Editor do Neon, arquivo inteiro de uma vez.
-- Rode UMA vez. (O bloco 1 pode repetir; os blocos 2 a 4 duplicam.)
-- Pre-requisito: schema_postgres.sql (ou a migracao de missoes) ja rodado.
-- =====================================================================

-- BLOCO 1 - Monumentos (7 de Olinda, 7 do Recife)
INSERT INTO monumentos (nome_monumento, descricao_monumento, qrcode_hash, pontos, cidade) VALUES
('Catedral de São Salvador do Mundo (Igreja da Sé)', 'Igreja da Sé, no Alto da Sé, em Olinda.', 'OLI_CATEDRAL_SE', 10, 'Olinda'),
('Caixa d''Água do Alto da Sé (Mirante da Sé)', 'Mirante panorâmico no Alto da Sé, em Olinda.', 'OLI_MIRANTE_SE', 10, 'Olinda'),
('Mercado do Alto da Sé', 'Mercado do Alto da Sé, em Olinda.', 'OLI_MERCADO_SE', 10, 'Olinda'),
('Observatório Astronômico do Alto da Sé', 'Observatório astronômico no Alto da Sé, em Olinda.', 'OLI_OBSERVATORIO', 10, 'Olinda'),
('Casa de Alceu Valença', 'Casa de Alceu Valença, ícone da música pernambucana, em Olinda.', 'OLI_CASA_ALCEU', 10, 'Olinda'),
('Praça Rio Branco (Praça do Marco Zero)', 'Praça do Marco Zero, no Recife Antigo.', 'REC_PRACA_MARCO_ZERO', 10, 'Recife'),
('Rosa dos Ventos (Obra de Cícero Dias)', 'Obra a céu aberto de Cícero Dias, no Recife.', 'REC_ROSA_DOS_VENTOS', 10, 'Recife'),
('Marco Zero de Pernambuco (Marco Escultórico)', 'Marco escultórico do Marco Zero de Pernambuco, no Recife.', 'REC_MARCO_ZERO_ESCULTURICO', 10, 'Recife'),
('Paço do Frevo', 'Espaço cultural dedicado ao frevo, no Recife.', 'REC_PACO_DO_FREVO', 10, 'Recife'),
('Museu Cais do Sertão', 'Museu dedicado à cultura sertaneja, no Recife.', 'REC_CAIS_SERTAO', 10, 'Recife'),
('Igreja de Nossa Senhora da Misericórdia', 'Igreja de Nossa Senhora da Misericórdia, em Olinda.', 'OLI_MISERICORDIA', 10, 'Olinda'),
('Casario Colonial da Ladeira da Misericórdia', 'Casario colonial da Ladeira da Misericórdia, em Olinda.', 'OLI_LADEIRA_MISERICORDIA', 10, 'Olinda'),
('Ponte Maurício de Nassau', 'Ponte histórica do Recife.', 'REC_PONTE_NASSAU', 10, 'Recife'),
('Caixa Cultural Recife', 'Centro cultural no Recife.', 'REC_CAIXA_CULTURAL', 10, 'Recife')
ON CONFLICT (qrcode_hash) DO UPDATE SET
  nome_monumento = EXCLUDED.nome_monumento,
  descricao_monumento = EXCLUDED.descricao_monumento,
  cidade = EXCLUDED.cidade;

-- BLOCO 2 - Trilhas
INSERT INTO trilha (nome_trilha, descricao_trilha, tema) VALUES
('Coração do Alto da Sé (Olinda)', 'Roteiro pelo ponto mais alto e emblemático de Olinda, unindo arquitetura colonial, mirantes panorâmicos e a casa de um ícone da música pernambucana.', 'Histórica & Cultural'),
('Marco Zero & Cultura Viva (Recife)', 'Caminhada pelo berço do Recife Antigo passando pelas obras a céu aberto e pelos principais templos do frevo e da cultura sertaneja.', 'Arte & Cultura Popular'),
('Lendas, Ladeiras & Pontes (Recife & Olinda)', 'Rota de contraste entre as ladeiras históricas de Olinda e os casarões e pontes centenárias do Recife.', 'Arquitetura & Lendas');

-- BLOCO 3 - Paradas das trilhas (ordem das paradas)
INSERT INTO trilha_monumento (id_trilha, id_monumento, ordem)
SELECT t.id_trilha, m.id_monumento, v.ordem
FROM (VALUES
  ('Coração do Alto da Sé (Olinda)', 'OLI_CATEDRAL_SE', 1),
  ('Coração do Alto da Sé (Olinda)', 'OLI_MIRANTE_SE', 2),
  ('Coração do Alto da Sé (Olinda)', 'OLI_MERCADO_SE', 3),
  ('Coração do Alto da Sé (Olinda)', 'OLI_OBSERVATORIO', 4),
  ('Coração do Alto da Sé (Olinda)', 'OLI_CASA_ALCEU', 5),
  ('Marco Zero & Cultura Viva (Recife)', 'REC_PRACA_MARCO_ZERO', 1),
  ('Marco Zero & Cultura Viva (Recife)', 'REC_ROSA_DOS_VENTOS', 2),
  ('Marco Zero & Cultura Viva (Recife)', 'REC_MARCO_ZERO_ESCULTURICO', 3),
  ('Marco Zero & Cultura Viva (Recife)', 'REC_PACO_DO_FREVO', 4),
  ('Marco Zero & Cultura Viva (Recife)', 'REC_CAIS_SERTAO', 5),
  ('Lendas, Ladeiras & Pontes (Recife & Olinda)', 'OLI_MISERICORDIA', 1),
  ('Lendas, Ladeiras & Pontes (Recife & Olinda)', 'OLI_LADEIRA_MISERICORDIA', 2),
  ('Lendas, Ladeiras & Pontes (Recife & Olinda)', 'REC_PONTE_NASSAU', 3),
  ('Lendas, Ladeiras & Pontes (Recife & Olinda)', 'REC_CAIXA_CULTURAL', 4)
) AS v(nome_trilha, hash, ordem)
JOIN trilha t ON t.nome_trilha = v.nome_trilha
JOIN monumentos m ON m.qrcode_hash = v.hash;

-- BLOCO 4 - Missoes (200 pontos cada)
INSERT INTO missao (titulo, descricao_missao, tipo_regra, pontos_recompensa) VALUES
('Guardião do Alto da Sé', 'Resgate o QR Code da Catedral da Sé, do Mirante da Sé e do Mercado do Alto da Sé.', 'todos_monumentos', 200),
('Embaixador do Marco Zero', 'Resgate o QR Code da Praça do Marco Zero, da Rosa dos Ventos e do Marco Escultórico.', 'todos_monumentos', 200),
('Explorador das Duas Cidades', 'Resgate o QR Code de um monumento de Olinda e de um do Recife no mesmo dia.', 'cidades_mesmo_dia', 200);

-- Monumentos exigidos (so para tipo 'todos_monumentos').
-- ATENCAO: confirme com o time quais 3 monumentos formam o Guardião.
INSERT INTO missao_monumento (id_missao, id_monumento)
SELECT mi.id_missao, m.id_monumento
FROM (VALUES
  ('Guardião do Alto da Sé', 'OLI_CATEDRAL_SE'),
  ('Guardião do Alto da Sé', 'OLI_MIRANTE_SE'),
  ('Guardião do Alto da Sé', 'OLI_MERCADO_SE'),
  ('Embaixador do Marco Zero', 'REC_PRACA_MARCO_ZERO'),
  ('Embaixador do Marco Zero', 'REC_ROSA_DOS_VENTOS'),
  ('Embaixador do Marco Zero', 'REC_MARCO_ZERO_ESCULTURICO')
) AS v(titulo, hash)
JOIN missao mi ON mi.titulo = v.titulo
JOIN monumentos m ON m.qrcode_hash = v.hash;

-- BLOCO 5 - CONFERENCIA (somente leitura)
-- Esperado: 7 Olinda + 7 Recife
SELECT cidade, COUNT(*) FROM monumentos GROUP BY cidade;
-- Esperado: 14 linhas (5 + 5 + 4)
SELECT t.nome_trilha, tm.ordem, m.nome_monumento
FROM trilha_monumento tm
JOIN trilha t ON t.id_trilha = tm.id_trilha
JOIN monumentos m ON m.id_monumento = tm.id_monumento
ORDER BY t.id_trilha, tm.ordem;
-- Esperado: Guardião 3, Embaixador 3, Explorador 0 (regra por cidade)
SELECT mi.titulo, mi.pontos_recompensa, COUNT(mm.id_monumento) AS monumentos_exigidos
FROM missao mi LEFT JOIN missao_monumento mm ON mm.id_missao = mi.id_missao
GROUP BY mi.id_missao ORDER BY mi.id_missao;

-- BLOCO 6 - COORDENADAS (preencher depois)
-- Troque os NULL por numeros do Google Maps (botao direito no local; o
-- 1o numero e a latitude, o 2o a longitude; use ponto como decimal).
-- Linhas que continuarem NULL sao ignoradas. Pode rodar varias vezes.
UPDATE monumentos m SET latitude = v.lat, longitude = v.lng
FROM (VALUES
  ('OLI_CATEDRAL_SE',            NULL::numeric, NULL::numeric),
  ('OLI_MIRANTE_SE',             NULL, NULL),
  ('OLI_MERCADO_SE',             NULL, NULL),
  ('OLI_OBSERVATORIO',           NULL, NULL),
  ('OLI_CASA_ALCEU',             NULL, NULL),
  ('REC_PRACA_MARCO_ZERO',       NULL, NULL),
  ('REC_ROSA_DOS_VENTOS',        NULL, NULL),
  ('REC_MARCO_ZERO_ESCULTURICO', NULL, NULL),
  ('REC_PACO_DO_FREVO',          NULL, NULL),
  ('REC_CAIS_SERTAO',            NULL, NULL),
  ('OLI_MISERICORDIA',           NULL, NULL),
  ('OLI_LADEIRA_MISERICORDIA',   NULL, NULL),
  ('REC_PONTE_NASSAU',           NULL, NULL),
  ('REC_CAIXA_CULTURAL',         NULL, NULL)
) AS v(hash, lat, lng)
WHERE m.qrcode_hash = v.hash AND v.lat IS NOT NULL AND v.lng IS NOT NULL;
