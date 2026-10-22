import os
import sqlite3
from contextlib import closing

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "riders_express")
SQL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "riders_express.sql")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # fila["nombre"] en vez de fila[1]
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """borra y vuelve a crear las tablas con sus datos"""
    with open(SQL_PATH, encoding="utf-8") as f:
        script = f.read()
    with closing(get_conn()) as conn, conn:
        conn.executescript(script)

def crear_usuario(nombre, barrio, saldo=0):  # Create
    with closing(get_conn()) as conn, conn:
        conn.execute("INSERT INTO Usuario (nombre, barrio, saldo) VALUES (?, ?, ?)",
                     (nombre, barrio, saldo))

def obtener_usuarios():  # Read
    with closing(get_conn()) as conn:
        return conn.execute("SELECT * FROM Usuario ORDER BY id_usuario").fetchall()

def recargar_saldo(id_usuario, euros):  # Update
    with closing(get_conn()) as conn, conn:
        conn.execute("UPDATE Usuario SET saldo = saldo + ? WHERE id_usuario = ?",
                     (euros, id_usuario))

def borrar_usuario(id_usuario):  # Delete
    with closing(get_conn()) as conn, conn:
        conn.execute("DELETE FROM Usuario WHERE id_usuario = ?", (id_usuario,))

def obtener_platos():
    with closing(get_conn()) as conn:
        return conn.execute(
            """SELECT p.id_plato, p.nombre, p.precio, r.nombre AS restaurante
               FROM Plato p JOIN Restaurante r ON r.id_restaurante = p.id_restaurante
               ORDER BY p.id_plato""").fetchall()

def barrio_de_plato(id_plato):
    """barrio del restaurante donde se cocina el plato"""
    with closing(get_conn()) as conn:
        fila = conn.execute(
            """SELECT r.barrio FROM Plato p JOIN Restaurante r ON r.id_restaurante = p.id_restaurante
               WHERE p.id_plato = ?""", (id_plato,)).fetchone()
    if fila is None:
        raise ValueError(f"El plato {id_plato} no existe")
    return fila["barrio"]

def datos_pedido(id_pedido):
    """barrio del restaurante (el del primer plato) y barrio del cliente"""
    with closing(get_conn()) as conn:
        return conn.execute(
            """SELECT r.barrio AS restaurante, u.barrio AS cliente
               FROM Pedido pe
               JOIN Usuario u ON u.id_usuario = pe.id_usuario
               JOIN LineaPedido lp ON lp.id_pedido = pe.id_pedido
               JOIN Plato p ON p.id_plato = lp.id_plato
               JOIN Restaurante r ON r.id_restaurante = p.id_restaurante
               WHERE pe.id_pedido = ? ORDER BY lp.id_plato LIMIT 1""", (id_pedido,)).fetchone()

def pedidos_por_rider():
    """cuántos pedidos y cuánto dinero ha movido cada rider (JOIN + COUNT + SUM + GROUP BY)"""
    with closing(get_conn()) as conn:
        return conn.execute(
            """SELECT r.nombre, COUNT(DISTINCT pe.id_pedido) AS pedidos,
                      COALESCE(SUM(lp.precio_unit * lp.cantidad), 0) AS facturado
               FROM Rider r
               LEFT JOIN Pedido pe ON pe.id_rider = r.id_rider
               LEFT JOIN LineaPedido lp ON lp.id_pedido = pe.id_pedido
               GROUP BY r.id_rider ORDER BY pedidos DESC""").fetchall()
