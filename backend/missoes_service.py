"""Missoes (RF08): conclusao automatica a cada resgate de QR Code.

Uso no /conquistas/resgatar: chamar `verificar_missoes` DEPOIS de adicionar a
conquista e somar os pontos do monumento, e ANTES do commit. Assim conquista,
pontos e missoes concluidas entram na mesma transacao.
"""
from datetime import timezone, timedelta
from sqlalchemy.orm import Session

from models import (
    Usuario, Monumento, UsuarioConquista,
    Missao, MissaoMonumento, UsuarioMissao,
)

CIDADES_DUAS = {"Olinda", "Recife"}

# Recife e UTC-3 o ano todo (sem horario de verao). data_conquista e salva em
# UTC (datetime.utcnow), entao convertemos para o dia local antes de comparar.
FUSO_RECIFE = timezone(timedelta(hours=-3))


def _dia_local(dt):
    return dt.replace(tzinfo=timezone.utc).astimezone(FUSO_RECIFE).date()


def _estado(db: Session, usuario: Usuario):
    """Monumentos resgatados e cidades visitadas por dia (dia local de Recife)."""
    conquistas = (
        db.query(UsuarioConquista.id_monumento, Monumento.cidade, UsuarioConquista.data_conquista)
        .join(Monumento, Monumento.id_monumento == UsuarioConquista.id_monumento)
        .filter(UsuarioConquista.id_usuario == usuario.id_usuario)
        .all()
    )
    monumentos_ok = {c.id_monumento for c in conquistas}
    cidades_por_dia: dict = {}
    for c in conquistas:
        if c.cidade:
            cidades_por_dia.setdefault(_dia_local(c.data_conquista), set()).add(c.cidade)
    return monumentos_ok, cidades_por_dia


def _exigidos(db: Session, id_missao: int) -> set:
    return {
        r.id_monumento
        for r in db.query(MissaoMonumento.id_monumento).filter(MissaoMonumento.id_missao == id_missao)
    }


def _progresso(db: Session, missao: Missao, monumentos_ok: set, cidades_por_dia: dict):
    """(feitos, total) da missao para o usuario."""
    if missao.tipo_regra == "todos_monumentos":
        exigidos = _exigidos(db, missao.id_missao)
        return len(exigidos & monumentos_ok), len(exigidos)
    if missao.tipo_regra == "cidades_mesmo_dia":
        melhor = max((len(CIDADES_DUAS & c) for c in cidades_por_dia.values()), default=0)
        return melhor, len(CIDADES_DUAS)
    return 0, 0


def verificar_missoes(db: Session, usuario: Usuario) -> list[Missao]:
    """Conclui as missoes que o usuario acabou de cumprir e soma os pontos.

    Retorna as missoes concluidas AGORA (lista vazia se nenhuma).
    Nao faz commit: quem chama controla a transacao.
    """
    db.flush()  # a conquista recem-criada precisa estar visivel nas consultas

    ja_concluidas = {
        r.id_missao
        for r in db.query(UsuarioMissao.id_missao).filter(UsuarioMissao.id_usuario == usuario.id_usuario)
    }
    pendentes = [m for m in db.query(Missao).all() if m.id_missao not in ja_concluidas]
    if not pendentes:
        return []

    monumentos_ok, cidades_por_dia = _estado(db, usuario)

    novas = []
    for missao in pendentes:
        feitos, total = _progresso(db, missao, monumentos_ok, cidades_por_dia)
        if total > 0 and feitos >= total:
            db.add(UsuarioMissao(id_usuario=usuario.id_usuario, id_missao=missao.id_missao))
            usuario.pontos_totais += missao.pontos_recompensa
            novas.append(missao)
    return novas


def listar_missoes_com_progresso(db: Session, usuario: Usuario) -> list[dict]:
    """Todas as missoes, com status e progresso do usuario (para a tela de missoes)."""
    concluidas = {
        r.id_missao
        for r in db.query(UsuarioMissao.id_missao).filter(UsuarioMissao.id_usuario == usuario.id_usuario)
    }
    monumentos_ok, cidades_por_dia = _estado(db, usuario)

    resultado = []
    for m in db.query(Missao).order_by(Missao.id_missao).all():
        feitos, total = _progresso(db, m, monumentos_ok, cidades_por_dia)
        feita = m.id_missao in concluidas
        resultado.append({
            "id_missao": m.id_missao,
            "titulo": m.titulo,
            "descricao_missao": m.descricao_missao,
            "tipo_regra": m.tipo_regra,
            "pontos_recompensa": m.pontos_recompensa,
            "concluida": feita,
            "progresso": total if feita else feitos,
            "total": total,
        })
    return resultado