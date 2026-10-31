-- Consulta para ver o perfil completo do usuário e suas conquistas
SELECT 
    u.nome AS Usuario,
    u.pontos_totais AS Pontos_Acumulados,
    m.nome_monumento AS Monumento_Visitado,
    b.nome_brinde AS Brinde_Resgatado,
    uc.data_conquista AS Data_Visita
FROM usuario u
JOIN usuario_conquista uc ON u.id_usuario = uc.id_usuario
JOIN monumentos m ON uc.id_monumento = m.id_monumento
LEFT JOIN usuario_brindes ub ON u.id_usuario = ub.id_usuario
LEFT JOIN brindes b ON ub.brinde_id = b.brinde_id
WHERE u.id_usuario = 1;