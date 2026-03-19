def criar_pedido(sender, message):
    return f"PED-{hash(sender) % 10000}"