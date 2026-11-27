USE programando_futuro;


INSERT INTO usuario (nome, email, senha_hash, pontos_totais) 
VALUES ('Maria Silva', 'maria@email.com', 'hash_senha_123', 0);


INSERT INTO monumentos (nome_monumento, descricao_monumento, qrcode_hash, pontos) 
VALUES ('Marco Zero', 'Praça do Marco Zero no Recife Antigo.', 'REC_MZ_2026', 50);


INSERT INTO brindes (id_monumento, nome_brinde, imagem_url) 
VALUES (1, 'Boneco de Olinda Digital', 'https://exemplo.com/brinde1.png');


INSERT INTO usuario_conquista (id_usuario, id_monumento) 
VALUES (1, 1);


UPDATE usuario 
SET pontos_totais = pontos_totais + 50 
WHERE id_usuario = 1;


INSERT INTO usuario_brindes (id_usuario, brinde_id) 
VALUES (1, 1);