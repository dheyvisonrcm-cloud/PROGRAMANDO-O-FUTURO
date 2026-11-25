import bcrypt


def gerar_hash(senha: str) -> str:
    # bcrypt só considera os primeiros 72 bytes da senha
    return bcrypt.hashpw(senha.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode("utf-8")[:72], senha_hash.encode("utf-8"))
    except ValueError:
        # hash inválido (por exemplo, senha antiga em texto puro)
        return False