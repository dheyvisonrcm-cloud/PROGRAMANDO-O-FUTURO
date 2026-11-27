"""Teste de fumaça da API (Programando o Futuro).

Uso:
    pip install requests
   python testar_api.py https://programando-o-futuro-6zpg.onrender.com
    python testar_api.py                      # usa http://localhost:8000

Cria um usuário novo a cada execução (e-mail aleatório) e percorre o fluxo
principal: cadastro, login, resgates de QR Code, missões, favoritos e trilhas.
Requer o banco populado (popular_mvp_postgres.sql). Os usuários de teste
ficam no banco; apague-os depois se quiser.
"""
import sys
import uuid
import requests

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000").rstrip("/")
TIMEOUT = 60  # o Render free pode demorar a "acordar"

falhas = 0


def checar(nome, ok, detalhe=""):
    global falhas
    print(f"[{'OK' if ok else 'FALHOU'}] {nome}" + (f"  -> {detalhe}" if detalhe and not ok else ""))
    if not ok:
        falhas += 1


def chamar(metodo, caminho, token=None, **kw):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return requests.request(metodo, BASE + caminho, headers=headers, timeout=TIMEOUT, **kw)


def resgatar(token, qr):
    return chamar("POST", "/conquistas/resgatar", token, json={"qrcode_hash": qr})


# ---------------------------------------------------------------- status
r = chamar("GET", "/")
checar("GET / (API online)", r.status_code == 200, r.text)

r = chamar("GET", "/testar-banco")
checar("GET /testar-banco", r.status_code == 200, r.text)
total_monumentos = r.json().get("total_monumentos", 0) if r.status_code == 200 else 0
checar("banco tem 14 monumentos", total_monumentos == 14, f"encontrou {total_monumentos}")

# ------------------------------------------------------ cadastro e login
email = f"teste_{uuid.uuid4().hex[:8]}@teste-api.com"
senha = "senha123"

r = chamar("POST", "/cadastrar", json={"nome": "Teste API", "email": email, "senha": senha})
checar("POST /cadastrar", r.status_code == 201, r.text)

r = chamar("POST", "/cadastrar", json={"nome": "Teste API", "email": email, "senha": senha})
checar("cadastro duplicado é recusado (400)", r.status_code == 400, r.text)

r = chamar("POST", "/login", json={"email": email, "senha": "errada123"})
checar("login com senha errada é recusado (401)", r.status_code == 401, r.text)

r = chamar("POST", "/login", json={"email": email, "senha": senha})
checar("POST /login", r.status_code == 200, r.text)
if r.status_code != 200:
    print("Sem token, não dá para continuar.")
    sys.exit(1)
token = r.json()["access_token"]

r = chamar("GET", "/usuarios/me")
checar("rota protegida sem token é recusada", r.status_code in (401, 403), str(r.status_code))

r = chamar("GET", "/usuarios/me", token)
checar("GET /usuarios/me (0 pontos)", r.status_code == 200 and r.json()["pontos_totais"] == 0, r.text)

# ------------------------------------------------------- mapa e trilhas
r = chamar("GET", "/monumentos")
checar("GET /monumentos", r.status_code == 200, r.text)
if r.status_code == 200 and not r.json():
    print("      (aviso: lista vazia, os monumentos ainda estão sem latitude/longitude)")

r = chamar("GET", "/trilhas")
checar("GET /trilhas (3 trilhas)", r.status_code == 200 and len(r.json()) == 3, r.text)
id_trilha = r.json()[0]["id_trilha"] if r.status_code == 200 and r.json() else None

if id_trilha:
    r = chamar("GET", f"/trilhas/{id_trilha}")
    checar("GET /trilhas/{id}", r.status_code == 200 and len(r.json()["monumentos"]) > 0, r.text)
    id_monumento = r.json()["monumentos"][0]["id_monumento"] if r.status_code == 200 else None

    r = chamar("POST", f"/trilhas/{id_trilha}/iniciar", token)
    checar("POST /trilhas/{id}/iniciar", r.status_code == 201, r.text)

    if id_monumento:
        r = chamar("GET", f"/monumentos/{id_monumento}/narrativa")
        checar("GET /monumentos/{id}/narrativa", r.status_code == 200, r.text)
        id_narrativa = r.json().get("id_narrativa_monumento") if r.status_code == 200 else None

        r = chamar("POST", f"/favoritos/{id_monumento}", token)
        checar("POST /favoritos/{id}", r.status_code == 201, r.text)
        r = chamar("GET", "/favoritos", token)
        checar("GET /favoritos", r.status_code == 200 and len(r.json()) == 1, r.text)

        if id_narrativa:
            r = chamar("POST", f"/narrativas/{id_narrativa}/salvar", token)
            checar("POST /narrativas/{id}/salvar", r.status_code == 201, r.text)
            r = chamar("GET", "/narrativas/salvas", token)
            checar("GET /narrativas/salvas", r.status_code == 200 and len(r.json()) == 1, r.text)

# ------------------------------------------------- resgates e missões
r = resgatar(token, "NAO_EXISTE")
checar("QR Code inexistente retorna 404", r.status_code == 404, r.text)

r = chamar("GET", "/missoes", token)
checar("GET /missoes (3 missões, nenhuma concluída)",
       r.status_code == 200 and len(r.json()) == 3 and not any(m["concluida"] for m in r.json()), r.text)


def titulos(resp):
    return [m["titulo"] for m in resp.json().get("missoes_concluidas", [])] if resp.status_code == 200 else []


# Guardião do Alto da Sé: fecha no 3º monumento (Olinda)
for qr in ("OLI_CATEDRAL_SE", "OLI_MIRANTE_SE"):
    r = resgatar(token, qr)
    checar(f"resgatar {qr} (sem missão ainda)", r.status_code == 200 and titulos(r) == [], r.text)

r = resgatar(token, "OLI_MERCADO_SE")
checar("3º do Alto da Sé conclui 'Guardião do Alto da Sé'",
       r.status_code == 200 and titulos(r) == ["Guardião do Alto da Sé"], r.text)

r = resgatar(token, "OLI_MERCADO_SE")
checar("resgate repetido é recusado (400)", r.status_code == 400, r.text)

# Explorador das Duas Cidades: 1 de Olinda + 1 do Recife no mesmo dia
r = resgatar(token, "REC_PRACA_MARCO_ZERO")
checar("1º do Recife conclui 'Explorador das Duas Cidades'",
       r.status_code == 200 and titulos(r) == ["Explorador das Duas Cidades"], r.text)

# Embaixador do Marco Zero: fecha no 3º monumento do Marco Zero
r = resgatar(token, "REC_ROSA_DOS_VENTOS")
checar("resgatar REC_ROSA_DOS_VENTOS (sem missão ainda)", r.status_code == 200 and titulos(r) == [], r.text)
r = resgatar(token, "REC_MARCO_ZERO_ESCULTURICO")
checar("3º do Marco Zero conclui 'Embaixador do Marco Zero'",
       r.status_code == 200 and titulos(r) == ["Embaixador do Marco Zero"], r.text)

# 6 monumentos x 10 pontos + 3 missões x 200 pontos = 660
r = chamar("GET", "/usuarios/me", token)
pontos = r.json().get("pontos_totais") if r.status_code == 200 else None
checar("pontos totais = 660 (60 dos monumentos + 600 das missões)", pontos == 660, f"veio {pontos}")

r = chamar("GET", "/missoes", token)
checar("GET /missoes (as 3 concluídas)",
       r.status_code == 200 and all(m["concluida"] for m in r.json()), r.text)

if id_trilha:
    r = chamar("GET", f"/trilhas/{id_trilha}/progresso", token)
    checar("GET /trilhas/{id}/progresso", r.status_code == 200, r.text)

# ---------------------------------------------------------------- resumo
print()
if falhas:
    print(f"{falhas} verificação(ões) falharam.")
    sys.exit(1)
print("Tudo certo.")

### ------------------------------------------------- pílulas: limites e erros
r = chamar("GET", f"/monumentos/{id_monumento}/narrativa")
if r.status_code == 200:
    dados_pilula = r.json()
    palavras = len(dados_pilula.get("texto", "").split())
    checar("pílula respeita limite de tamanho (<= 90 palavras)", palavras <= 90, f"{palavras} palavras")

    id_atual = dados_pilula["id_narrativa_monumento"]
    r2 = chamar("GET", f"/monumentos/{id_monumento}/narrativa?excluir={id_atual}")
    checar("ver outra retorna variante diferente", r2.status_code == 200 and r2.json()["id_narrativa_monumento"] != id_atual, r2.text)

r_inexistente = chamar("GET", "/monumentos/999999/narrativa")
checar("monumento inexistente/sem pílula retorna 404", r_inexistente.status_code == 404, str(r_inexistente.status_code))

### ------------------------------------------------- isolamento entre usuários
email_b = f"teste_b_{uuid.uuid4().hex[:8]}@teste-api.com"
chamar("POST", "/cadastrar", json={"nome": "Usuario B", "email": email_b, "senha": senha})
token_b = chamar("POST", "/login", json={"email": email_b, "senha": senha}).json()["access_token"]

perfil_b = chamar("GET", "/usuarios/me", token_b)
checar("isolamento: Usuário B começa com 0 pontos", perfil_b.status_code == 200 and perfil_b.json().get("pontos_totais") == 0, perfil_b.text)

r_diario_b = chamar("GET", "/diario", token_b)
checar("GET /diario responde 200 OK", r_diario_b.status_code == 200, f"status={r_diario_b.status_code} body={r_diario_b.text}")
if r_diario_b.status_code == 200:
    diario_b = r_diario_b.json()
    checar(
        "isolamento: Usuário B não vê conquistas, favoritos nem pílulas do Usuário A",
        all(len(v) == 0 for v in diario_b.values() if isinstance(v, list)),
        str(diario_b)
    )