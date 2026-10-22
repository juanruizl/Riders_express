from contextlib import closing
from db import get_conn

def crear_pedido(id_usuario, id_rider, lineas, fecha):
    """lineas = [(id_plato, cantidad), ...]. O se hace entero o no se hace."""
    with closing(get_conn()) as conn, conn:  # commit si todo va bien
        cur = conn.execute(
            "INSERT INTO Pedido (fecha, id_usuario, id_rider) VALUES (?, ?, ?)",
            (fecha, id_usuario, id_rider))
        id_pedido = cur.lastrowid
        for id_plato, cantidad in lineas:
            cur = conn.execute(  # el precio se guarda en la línea
                """INSERT INTO LineaPedido (id_pedido, id_plato, cantidad, precio_unit)
                   SELECT ?, id_plato, ?, precio FROM Plato WHERE id_plato = ?""",
                (id_pedido, cantidad, id_plato))
            if cur.rowcount == 0:  # el SELECT no encontró el plato
                raise ValueError(f"El plato {id_plato} no existe")
        total = conn.execute(
            "SELECT SUM(precio_unit * cantidad) FROM LineaPedido WHERE id_pedido = ?",
            (id_pedido,)).fetchone()[0]
        saldo = conn.execute("SELECT saldo FROM Usuario WHERE id_usuario = ?",
                             (id_usuario,)).fetchone()[0]
        if total > saldo:  # rollback: no queda nada
            raise ValueError(f"Tarjeta rechazada: {total} € y tiene {saldo} €")
        conn.execute("UPDATE Usuario SET saldo = saldo - ? WHERE id_usuario = ?",
                     (total, id_usuario))
        return id_pedido, total
