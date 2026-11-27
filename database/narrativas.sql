-- =====================================================================
-- Guia Turistico Gamificado com IA - Pilulas de lore do MVP (PostgreSQL / Neon)
-- 14 monumentos x 3 variantes = 42 pilulas, escritas pela equipe de apoio
-- com base em fontes publicas (listadas em cada bloco).
--
-- COMO RODAR
--  * Pre-requisito: o popular_mvp_postgres.sql (monumentos) ja foi executado.
--  * SQL Editor do Neon: pode rodar o arquivo inteiro de uma vez.
--  * Cada bloco busca o id do monumento pelo qrcode_hash. Rode os blocos 1 a 3
--    UMA vez: repetir gera erro de duplicidade (UNIQUE id_monumento+variante),
--    o que protege contra pilulas repetidas.
--
-- REVISAO: as pilulas entram com aprovada = TRUE (aparecem no app).
-- Se quiser revisar antes, troque TRUE por FALSE no INSERT, ou use o BLOCO 5.
-- Limites do banco: texto ate 400 caracteres, desafio ate 200.
-- =====================================================================


-- ---------------------------------------------------------------------
-- BLOCO 1 - TRILHA 1 - Coração do Alto da Sé (Olinda)
-- ---------------------------------------------------------------------
-- Catedral da Sé (Olinda) (OLI_CATEDRAL_SE) | Fontes: Melhores Destinos, Meer (Alto da Sé), Redalyc (restauro da Sé), UAI, Revista Ave Maria
-- Caixa d’Água do Alto da Sé (Olinda) (OLI_MIRANTE_SE) | Fontes: Estado de Minas, ArchDaily, Prefeitura de Olinda, Mercado & Eventos, Portal São Francisco, Melhores Destinos
-- Mercado de Artesanato do Alto da Sé (Olinda) (OLI_MERCADO_SE) | Fontes: Melhores Destinos, Wanderlog, Redalyc (tapioqueiras), Mercado & Eventos
-- Observatório Astronômico do Alto da Sé (Olinda) (OLI_OBSERVATORIO) | Fontes: Meer (Alto da Sé), Folha de Pernambuco, Wanderlog, Revista Relea (Marcgrave)
-- Casa de Alceu Valença (Olinda) (OLI_CASA_ALCEU) | Fontes: Folha de Pernambuco, Airbnb Newsroom, Catraca Livre, Diario de Pernambuco, Caras
INSERT INTO narrativa_monumento (id_monumento, variante, texto_narrativa, desafio, aprovada) VALUES
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_CATEDRAL_SE'), 1, 'Tudo começou com uma capela simples de taipa, por volta de 1540. Hoje, a Catedral da Sé é uma das igrejas mais antigas do Brasil e o coração do Alto da Sé. Quase cinco séculos de história esperando por você, explorador!', 'Pare em frente à catedral e escolha um detalhe que só você notou: uma porta, uma janela ou uma torre.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_CATEDRAL_SE'), 2, 'Invasão holandesa, reconstrução, restauros... a Catedral da Sé já viu muita coisa e continua de pé no alto da colina. Ela é a igreja principal da Arquidiocese de Olinda e Recife, ou seja, a “sé” que dá nome ao lugar.', 'Dê uma volta pela praça e encontre o melhor ângulo para a catedral aparecer inteira.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_CATEDRAL_SE'), 3, 'Do alto da Sé, Olinda e Recife se encontram no horizonte. O terraço da catedral tem uma das vistas mais bonitas das duas cidades-irmãs. Olhe longe, explorador: a próxima aventura está logo ali!', 'Procure no horizonte os prédios do Recife. Dá para ver daqui?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_MIRANTE_SE'), 1, 'Em 1934, num morro cheio de igrejas coloniais, nasceu uma torre moderna: a Caixa d’Água, projeto do arquiteto Luiz Nunes. Do alto, a vista alcança o Sítio Histórico e o Recife. Passado e futuro lado a lado!', 'Aponte para a construção mais antiga e para a mais nova que você consegue ver daqui.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_MIRANTE_SE'), 2, 'A Caixa d’Água abastecia o bairro e boa parte da cidade, e o nome pegou tanto que virou nome de bairro! Hoje, o que era um reservatório virou mirante e cartão-postal de Olinda.', 'Ache o melhor ângulo para ver a torre junto com a Catedral da Sé. Qual dupla fica mais bonita?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_MIRANTE_SE'), 3, 'No fim da tarde, o Alto da Sé vira plateia: moradores e visitantes se juntam para ver o pôr do sol, com o mar e o Recife ao fundo. Um intervalo de explorador também merece paisagem!', 'Procure o lado do horizonte onde o sol se põe e fique um minuto observando o céu.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_MERCADO_SE'), 1, 'Aqui o artesanato pernambucano vira lembrança: bolsas de fibras trançadas, bordados e muito mais. No fim do corredor, ainda tem uma vista de Olinda até o Recife. Cultura, compras e paisagem no mesmo lugar!', 'Escolha uma peça de artesanato que lembre as cores de Olinda e explique em uma frase o porquê.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_MERCADO_SE'), 2, 'Bem pertinho, cerca de 40 tapioqueiras preparam tapioca na hora, em fogareiros a carvão. A tradição é tão importante que é reconhecida como patrimônio imaterial e referência cultural de Olinda. Aqui a cultura tem sabor!', 'Descubra quantos recheios diferentes aparecem nas barracas de tapioca. Qual seria o seu?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_MERCADO_SE'), 3, 'Este lugar tem nome e sobrenome: Mercado de Artesanato Sylvia Pontual. Ele faz parte da revitalização do Alto da Sé, junto com o Largo da Sé e a Caixa d’Água, e valoriza o trabalho de artesãos locais.', 'Veja qual material aparece mais nas bancas: fibra, bordado, madeira ou cerâmica? Conte ao seu grupo.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_OBSERVATORIO'), 1, 'Esta torre redonda, de estilo neoclássico, é do século XIX e já serviu para observar os astros. A história dela se cruza com o chamado cometa Olinda e com a observação do trânsito de Vênus. Olhar para o céu também é patrimônio!', 'Imagine um telescópio no topo da torre e escolha o astro que você apontaria primeiro.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_OBSERVATORIO'), 2, 'Entre 1922 e 1960, o prédio deixou de observar estrelas e passou a observar o tempo: virou observatório meteorológico. Hoje volta a receber curiosos do céu em sessões abertas ao público.', 'Olhe o céu agora: está limpo, nublado ou com poucas nuvens? Você acaba de fazer uma observação meteorológica!', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_OBSERVATORIO'), 3, 'Curiosidade de explorador: o primeiro observatório astronômico do hemisfério Sul foi construído no Recife, no tempo dos holandeses, pelo astrônomo Georg Marcgrave. Pernambuco olha para as estrelas há muito tempo!', 'Pense em uma pergunta que você faria ao céu e guarde. Qual seria?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_CASA_ALCEU'), 1, 'O sobrado colorido de Alceu Valença é um ponto que muita gente faz questão de visitar em Olinda. No mesmo terreno fica a Casa Estação da Luz, centro de arte e cultura. Aqui, música e história moram na mesma rua!', 'Observe a fachada colorida e descreva em três palavras o que ela lembra: som, cor ou festa?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_CASA_ALCEU'), 2, 'Num pré-carnaval, Alceu apareceu na janela de casa e cantou para os foliões lá embaixo. O vídeo viralizou. Em Olinda, até a janela vira palco!', 'Imagine que você está na janela: qual música cantaria para a rua? Vale cantarolar baixinho!', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_CASA_ALCEU'), 3, 'Alceu Valença é pernambucano e leva a energia do Nordeste para o Brasil inteiro. Em Olinda, ele virou parte da paisagem e da trilha sonora da cidade, cantando a cultura da sua terra.', 'Procure um som ao redor (música, sino, conversa) e descubra de onde ele vem.', TRUE);

-- ---------------------------------------------------------------------
-- BLOCO 2 - TRILHA 2 - Marco Zero & Cultura Viva (Recife)
-- ---------------------------------------------------------------------
-- Praça do Marco Zero (Recife) (REC_PRACA_MARCO_ZERO) | Fontes: Guia da Semana, Melhores Destinos, Folha de Pernambuco, Prefeitura do Recife, Revista do Clube Naval
-- Rosa dos Ventos de Cícero Dias (Recife) (REC_ROSA_DOS_VENTOS) | Fontes: QuintoAndar Guias, Melhores Destinos, Folha de Pernambuco, Buser, Prefeitura do Recife
-- Marco Zero de Pernambuco (Recife) (REC_MARCO_ZERO_ESCULTURICO) | Fontes: Prefeitura do Recife (guia e mapa turístico), QuintoAndar Guias, Folha de Pernambuco
-- Paço do Frevo (Recife) (REC_PACO_DO_FREVO) | Fontes: Portal de Prefeitura, QuintoAndar Guias, 360 Meridianos, Movimento Econômico, Agência Brasil
-- Museu Cais do Sertão (Recife) (REC_CAIS_SERTAO) | Fontes: Panrotas, Folha de Pernambuco, 360 Meridianos, Melhores Destinos, Lonely Planet
INSERT INTO narrativa_monumento (id_monumento, variante, texto_narrativa, desafio, aprovada) VALUES
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_PRACA_MARCO_ZERO'), 1, 'Aqui o Recife começou. A Praça do Marco Zero, que na verdade se chama Praça Rio Branco, fica à beira do porto e marca o ponto de partida da cidade. Tudo o que você vê ao redor cresceu a partir daqui.', 'Fique no centro da praça e gire devagar: quantos prédios históricos você consegue contar ao redor?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_PRACA_MARCO_ZERO'), 2, 'Um pórtico por aqui anuncia: “Aqui nasce o Atlântico”. Pela tradição popular, é o encontro dos rios que forma o oceano. No Recife, até o mar tem lenda!', 'Procure o pórtico ou a placa do Atlântico. O que está escrito?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_PRACA_MARCO_ZERO'), 3, '“Eu vi o mundo… ele começava no Recife”, escreveu o pintor Cícero Dias. No Marco Zero, você está no ponto onde, dizem, o mundo do Recife começa. Dê o primeiro passo da aventura!', 'Dê um passo em direção a cada ponto cardeal: norte, sul, leste e oeste. Você é a bússola!', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_ROSA_DOS_VENTOS'), 1, 'Sob seus pés há uma obra de arte: a Rosa dos Ventos, de Cícero Dias, com 20 metros de diâmetro, feita de pedras de quartzo e granito coloridas. Arte para pisar, olhar e fotografar!', 'Ache o norte na Rosa dos Ventos e aponte para ele. Para onde fica o mar?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_ROSA_DOS_VENTOS'), 2, 'Cícero Dias foi um dos grandes nomes do modernismo brasileiro. Na sua Rosa dos Ventos aparecem os pontos cardeais e nomes de astros do Sistema Solar. É bússola e mapa do céu em uma obra só.', 'Leia os nomes ao redor da rosa dos ventos. Quantos astros você reconhece?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_ROSA_DOS_VENTOS'), 3, 'A Rosa dos Ventos simboliza as distâncias contadas a partir do Marco Zero: daqui os caminhos se abrem para todos os lados. Cícero Dias projetou e pintou a obra no centro da praça.', 'Escolha uma direção da rosa e imagine para onde ela leva. Que aventura você seguiria?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_MARCO_ZERO_ESCULTURICO'), 1, 'Este é o marco do quilômetro zero do Recife: daqui partem as contagens de distância. Uma placa de bronze avisa que você está no ponto de partida da cidade. Hora de zerar o hodômetro, explorador!', 'Encontre o marco e leia a inscrição. Depois, escolha um destino e imagine a distância a partir daqui.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_MARCO_ZERO_ESCULTURICO'), 2, 'Em 1999, a praça foi transformada: a estátua do Barão do Rio Branco e o Marco Zero foram levados para um canto, abrindo espaço para a obra de Cícero Dias no centro. Até os marcos mudam de lugar!', 'O marco está no centro ou na borda da praça? Descubra e conte ao seu grupo.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_MARCO_ZERO_ESCULTURICO'), 3, 'Zero é o começo de tudo. O Marco Zero marca o Km 0 do Recife e fica pertinho de onde a cidade nasceu, junto ao porto. Quem começa aqui começa pelo começo!', 'Tire uma foto do marco e diga aos amigos: “Estou no quilômetro zero!”', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_PACO_DO_FREVO'), 1, 'Este casarão já foi sede da Western Telegraph Company, pioneira do telégrafo no Brasil. Hoje abriga o Paço do Frevo. E o nome do ritmo vem de “ferver”, porque o frevo ferve mesmo!', 'Diga “ferver” e depois “frevo”, bem rápido. Notou a ligação?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_PACO_DO_FREVO'), 2, 'O frevo é Patrimônio Imaterial da Humanidade pela UNESCO desde 2012. E o Paço do Frevo foi inaugurado em 9 de fevereiro de 2014, justamente no Dia do Frevo. Coincidência? Não, tradição!', 'Marque o passo: faça dois passinhos de frevo, nem que seja só na imaginação!', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_PACO_DO_FREVO'), 3, 'O prédio ficou fechado por quase 40 anos antes de virar casa do frevo. Hoje tem museu, escola de dança e música e estúdio: aqui o ritmo é ensinado e vivido, não só exposto.', 'Observe a fachada, tombada pelo IPHAN, e procure um detalhe que mostre que ela é histórica.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_CAIS_SERTAO'), 1, 'Um armazém do porto virou um pedaço do sertão no litoral: o Museu Cais do Sertão, no antigo Armazém 10, inaugurado em 2014, homenageia o Rei do Baião, Luiz Gonzaga. Aqui o sertão encontra o mar!', 'Olhe para o prédio e imagine-o como armazém de porto. Descreva em uma palavra o que mudou.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_CAIS_SERTAO'), 2, 'O museu conta a vida no sertão em sete territórios: Viver, Trabalhar, Cantar, Ocupar, Crer, Migrar e Criar. Qual deles combina mais com você, explorador?', 'Escolha o território que mais combina com você e conte ao grupo por quê.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_CAIS_SERTAO'), 3, 'Entre as peças do museu está uma sanfona de 120 baixos que pertenceu a Luiz Gonzaga e depois a Dominguinhos. O som do sertão mora aqui, guardado como um tesouro.', 'Cantarole baixinho um trecho de uma música de Luiz Gonzaga e conte ao grupo qual foi.', TRUE);

-- ---------------------------------------------------------------------
-- BLOCO 3 - TRILHA 3 - Lendas, Ladeiras & Pontes (Recife & Olinda)
-- ---------------------------------------------------------------------
-- Igreja da Misericórdia (Olinda) (OLI_MISERICORDIA) | Fontes: Viagem e Luxo (Issuu), UFPE (patologias da Igreja da Misericórdia), Portal São Francisco
-- Ladeira da Misericórdia (Olinda) (OLI_LADEIRA_MISERICORDIA) | Fontes: Terra Brasil Notícias, Bahia.ws (cidades históricas do Nordeste), Correio 24 Horas (UNESCO 1982)
-- Ponte Maurício de Nassau (Recife) (REC_PONTE_NASSAU) | Fontes: Diario de Pernambuco (2015, 2017, 2018, 2019, 2024), Câmara dos Deputados (apresentação sobre pontes), Diário do Litoral
-- Caixa Cultural Recife (REC_CAIXA_CULTURAL) | Fontes: UFCG (Munier e o edifício), ABC do ABC (45 anos da Caixa Cultural), Diario de Pernambuco (Caixa Natal), Kupi, Lonely Planet
INSERT INTO narrativa_monumento (id_monumento, variante, texto_narrativa, desafio, aprovada) VALUES
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_MISERICORDIA'), 1, 'A Igreja da Misericórdia fazia parte do antigo hospital da Santa Casa de Misericórdia de Olinda. O nome já diz tudo: misericórdia é cuidar de quem precisa. Um lugar de fé e de acolhimento no meio da ladeira.', 'Observe a igreja e descubra: ela fica no alto ou na parte baixa da rua? O que dá para ver de lá?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_MISERICORDIA'), 2, 'As paredes dessa igreja chegam a 1,5 metro de espessura! Feitas de pedras de arenito, elas atravessaram séculos e restauros e seguem firmes. Resistência de explorador!', 'Estique o braço junto a uma parede ou porta e compare com 1,5 metro. Dá para imaginar?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_MISERICORDIA'), 3, 'O Largo da Misericórdia é um dos mirantes de Olinda, a cidade das colinas. De cima dá para ver telhados, árvores e, se o dia ajudar, o mar. Respire fundo e olhe longe.', 'Ache o ponto do largo com a melhor vista e descreva o que vê em uma frase.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_LADEIRA_MISERICORDIA'), 1, 'Prepare as pernas: a Ladeira da Misericórdia é uma das ruas mais íngremes de Olinda, rodeada de casarões históricos. Cada trecho de chão de pedra guarda um pedacinho da história colonial.', 'Suba ou desça com calma e conte quantas cores diferentes de casarões você vê.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_LADEIRA_MISERICORDIA'), 2, 'Pertinho da ladeira fica o Quatro Cantos, onde se cruzam as ruas Prudente de Morais e São Bento e a própria ladeira. É o coração do Carnaval de Olinda, cercado de casas antigas.', 'Imagine o Carnaval aqui. O que você ouviria? Frevo, orquestra, bonecos gigantes? Escolha um som.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'OLI_LADEIRA_MISERICORDIA'), 3, 'Olinda é cheia de ladeiras, casarões e cores, e seu centro histórico é Patrimônio Mundial da UNESCO desde 1982. Esta ladeira faz parte dessa paisagem protegida.', 'Procure uma porta ou janela de cor forte e imagine: de que época ela parece ser?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_PONTE_NASSAU'), 1, 'Uma ponte com quase 400 anos de história! A Ponte Maurício de Nassau, inaugurada em 1643, foi a primeira grande ponte do Brasil, feita pelos holandeses. A primeira era de madeira; a atual, de concreto, é de 1917.', 'Imagine a ponte original de madeira cruzando o Capibaribe. O que seria mais difícil: atravessar ou construir?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_PONTE_NASSAU'), 2, 'Conta a lenda que Nassau prometeu um boi voador para atrair o povo à ponte nova. Verdade ou não, o episódio do Boi Voador virou história famosa do Recife.', 'Imagine um boi voando sobre o rio. Que nome você daria a ele?', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_PONTE_NASSAU'), 3, 'A ponte liga o bairro do Recife a Santo Antônio, sobre o rio Capibaribe. Na época dos holandeses, ela ajudou a cidade a crescer para além da pequena ilha onde tudo começou.', 'De que lado do rio você está agora: Recife Antigo ou Santo Antônio? Procure uma referência para confirmar.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_CAIXA_CULTURAL'), 1, 'Este edifício de 1912 já foi sede de banco e, depois, da Bolsa de Valores de Pernambuco e da Paraíba. Hoje é a Caixa Cultural Recife, com exposições e espetáculos, de frente para o Marco Zero.', 'Olhe a fachada e procure sinais de um prédio imponente de outros tempos: portas altas, janelas, varandas.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_CAIXA_CULTURAL'), 2, 'No Natal, as janelas e varandas deste prédio viram palco do Caixa Natal Recife, um espetáculo ao ar livre que reúne muita gente no Recife Antigo. Um edifício histórico que vira teatro de rua!', 'Conte as varandas e janelas da fachada e imagine o espetáculo de Natal acontecendo nelas.', TRUE),
((SELECT id_monumento FROM monumentos WHERE qrcode_hash = 'REC_CAIXA_CULTURAL'), 3, 'A Caixa Cultural Recife foi inaugurada em 15 de maio de 2012, num prédio histórico adquirido pelo banco em 2006. Fica pertinho de tudo: Marco Zero, Rosa dos Ventos e Cais do Sertão. Boa aventura!', 'Pense: qual parada da sua aventura foi a mais surpreendente? Guarde a resposta!', TRUE);

-- ---------------------------------------------------------------------
-- BLOCO 4 - CONFERENCIA (somente leitura)
-- ESPERADO: 14 linhas, cada uma com total_variantes = 3 e aprovadas = 3
-- ---------------------------------------------------------------------
SELECT m.qrcode_hash, COUNT(*) AS total_variantes, SUM(n.aprovada::int) AS aprovadas,
       MAX(CHAR_LENGTH(n.texto_narrativa)) AS maior_texto
FROM narrativa_monumento n
JOIN monumentos m ON m.id_monumento = n.id_monumento
GROUP BY m.qrcode_hash
ORDER BY m.qrcode_hash;

-- ---------------------------------------------------------------------
-- BLOCO 5 - OPCIONAL: tirar todas as pilulas do ar para revisar
-- (depois de revisar, troque FALSE por TRUE para publicar de volta)
-- ---------------------------------------------------------------------
-- UPDATE narrativa_monumento SET aprovada = FALSE;