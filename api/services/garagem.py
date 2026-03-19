def criar_orcamento(sender, message):
    return f"ORC-{hash(sender) % 10000}"