
---

# 🗄️ Banco de Dados Relacional - Programando o Futuro (MVP Turismo Gamificado)

Este repositório contém a modelagem e os scripts SQL responsáveis pelo gerenciamento de dados do ecossistema **Programando o Futuro**. O banco foi desenhado no **MySQL 8.0+** para garantir integridade relacional, alta performance em consultas de perfil e travamento nativo contra fraudes no resgate de pontos.

---

## 📐 Modelo de Entidade e Relacionamento (DER)

A estrutura relacional foi desenvolvida para atender aos 5 Requisitos Funcionais (RF01 a RF05) da aplicação:

```text
       +-------------------+             +-----------------------+
       |      USUARIO      |             |  USUARIO_CONQUISTA    |
       +-------------------+             +-----------------------+
       | PK id_usuario     |<----+       | PK id_conquista       |
       |    nome           |     +-------| FK id_usuario         |
       |    email (UNIQUE) |             | FK id_monumento       |
       |    senha_hash     |     +-------|    data_conquista     |
       |    pontos_totais  |     |       +-----------------------+
       +-------------------+     |       | UNIQUE(usr, mon)      |
                                 |       +-----------------------+
                                 |
       +-------------------+     |       +-----------------------+
       |    MONUMENTOS     |     |       |        BRINDES        |
       +-------------------+     |       +-----------------------+
       | PK id_monumento   |<----+       | PK brinde_id          |
       |    nome_monumento |             | FK id_monumento       |<---+
       |    qrcode_hash    |<------------|    nome_brinde        |    |
       |    pontos         |             |    imagem_url         |    |
       +-------------------+             +-----------------------+    |
                                                                      |
                                         +-----------------------+    |
                                         |    USUARIO_BRINDES    |    |
                                         +-----------------------+    |
                                         | PK id_usuario_brindes |    |
                                         | FK id_usuario --------|----+
                                         | FK brinde_id ---------|----+
                                         |    data_resgate       |
                                         +-----------------------+


---

## 🔒 Regras de Integridade e Regra de Negócio Anti-Fraude

* **Trava Anti-Fraude de Resgate Único (RF03):** A tabela `usuario_conquista` possui uma restrição `UNIQUE KEY uk_usuario_monumento (id_usuario, id_monumento)`. Ela impede diretamente no motor do MySQL que um mesmo usuário consiga registrar o mesmo monumento mais de uma vez.


* **Acúmulo Transacional de Pontos (RF04):** Ao registrar uma nova linha na `usuario_conquista`, o campo `pontos_totais` da tabela `usuario` é somado aos pontos configurados na tabela `monumentos`.


* **Exclusão em Cascata (Foreign Keys):** Mapeadas com `ON DELETE CASCADE` e `ON UPDATE CASCADE` para preservar a consistência relacional.



---

## 📁 Arquivos da Pasta `database/`

1. **`schema.sql` (ou `ddl.sql`):** Script DDL para criar a base de dados `programando_futuro` e a estrutura de todas as 5 tabelas com suas respectivas restrições e chaves estrangeiras.


2. **`seeds_locais.sql`:** Script de carga inicial populando os monumentos históricos do **Sítio Histórico de Olinda** e do **Recife Antigo**, incluindo os hashes de QR Code e galeria de brindes digitais (placeholders).


3. **`consulta_perfil.sql`:** Consulta otimizada com `JOIN` e `LEFT JOIN` utilizada pela API para retornar o inventário e o histórico de conquistas de um perfil.



---

## 🚀 Como Executar o Banco Localmente

### Pré-requisitos

* **MySQL Server 8.0+** instalado e rodando na porta padrão `3306`.


* **MySQL Workbench** ou execução via Terminal.



### Passo a Passo no Terminal MySQL:

1. **Clonar e acessar o repositório:**
```bash
git clone https://github.com/dheyvisonrcm-cloud/PROGRAMANDO-O-FUTURO.git
cd PROGRAMANDO-O-FUTURO/database

```


2. **Criar a Estrutura (DDL):**
```bash
mysql -u root -p < schema.sql

```


3. **Popular os Dados Iniciais (Seeds):**
```bash
mysql -u root -p programando_futuro < seeds_locais.sql

```



---

## 📋 Mapeamento das Tabelas

| Tabela | Função / Requisito Coberto |
| --- | --- |
| **`usuario`** | Armazena dados cadastrais e saldo global de `pontos_totais` **(RF01, RF04)**.

 |
| **`monumentos`** | Contém o catálogo de locais turísticos, coordenadas e os `qrcode_hash` exclusivos **(RF02, RF03)**.

 |
| **`usuario_conquista`** | Tabela pivô de conquistas com trava `UNIQUE` contra resgates duplicados **(RF03)**.

 |
| **`brindes`** | Catálogo dos cards e troféus digitais vinculados aos monumentos **(RF05)**.

 |
| **`usuario_brindes`** | Galeria / inventário dos brindes resgatados e desbloqueados por cada usuário **(RF05)**.

 |