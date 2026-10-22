from contextlib import closing
from db import get_conn

def planificar_turno():
    """selección de actividades: máximo de repartos sin solapar"""
    with closing(get_conn()) as conn:
        repartos = conn.execute(
            "SELECT zona, inicio, fin FROM Reparto ORDER BY fin"  # el orden lo da SQL
        ).fetchall()

    elegidos, fin_ultimo = [], "00:00"
    for r in repartos:  # ya vienen ordenados por hora de fin
        if r["inicio"] >= fin_ultimo:  # no solapa con el último elegido
            elegidos.append(r["zona"])
            fin_ultimo = r["fin"]
    return elegidos
