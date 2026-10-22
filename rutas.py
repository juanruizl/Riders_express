import heapq
from contextlib import closing
from db import get_conn

def cargar_grafo():
    """{barrio: {vecino: minutos}} a partir de la tabla Tramo"""
    grafo = {}
    with closing(get_conn()) as conn:
        for t in conn.execute("SELECT origen, destino, minutos FROM Tramo"):
            grafo.setdefault(t["origen"], {})[t["destino"]] = t["minutos"]
            grafo.setdefault(t["destino"], {})[t["origen"]] = t["minutos"]  # ida y vuelta
    return grafo

def dijkstra(grafo, origen):
    """devuelve (distancias, previo) desde origen: minutos mínimos y barrio anterior en el camino"""
    dist = {barrio: float("inf") for barrio in grafo}
    previo = {origen: None}  # de dónde vengo: para reconstruir la ruta
    dist[origen] = 0
    cola = [(0, origen)]
    cerrados = set()
    while cola:
        d, u = heapq.heappop(cola)  # el pivote: el más cercano sin cerrar
        if u in cerrados:
            continue
        cerrados.add(u)
        for v, peso in grafo[u].items():
            if d + peso < dist[v]:  # relajar la arista u -> v
                dist[v] = d + peso
                previo[v] = u
                heapq.heappush(cola, (dist[v], v))
    return dist, previo

def camino(previo, destino):
    ruta = []
    while destino is not None:
        ruta.append(destino)
        destino = previo[destino]
    return ruta[::-1]

def rider_mas_cercano(grafo, barrio_restaurante):
    """devuelve (minutos, id_rider, nombre)"""
    dist, _ = dijkstra(grafo, barrio_restaurante)
    with closing(get_conn()) as conn:
        riders = conn.execute(
            "SELECT id_rider, nombre, barrio FROM Rider WHERE barrio IS NOT NULL").fetchall()
    return min((dist[r["barrio"]], r["id_rider"], r["nombre"]) for r in riders)
