import sqlite3
from datetime import datetime
from db import obtener_platos, barrio_de_plato, datos_pedido, pedidos_por_rider
from pedidos import crear_pedido
from rutas import cargar_grafo, dijkstra, camino, rider_mas_cercano
from turno import planificar_turno

def carta():
    for p in obtener_platos():
        print(f"{p['id_plato']}. {p['nombre']} - {p['precio']} € ({p['restaurante']})")

def pedir(grafo):
    carta()
    try:
        id_usuario = int(input("Usuario (id): "))
        lineas = []
        while True:
            entrada = input("Plato y cantidad, ej. '3 2' (vacío para acabar): ").split()
            if not entrada:
                break
            lineas.append((int(entrada[0]), int(entrada[1])))
        # el rider es el más cercano al restaurante del primer plato
        minutos, id_rider, nombre = rider_mas_cercano(grafo, barrio_de_plato(lineas[0][0]))
        id_pedido, total = crear_pedido(id_usuario, id_rider, lineas,
                                        datetime.now().strftime("%Y-%m-%d %H:%M"))
        print(f"Pedido {id_pedido}: {total} €, lo lleva {nombre} "
              f"(a {minutos} min del restaurante)")
    except (ValueError, IndexError, TypeError, sqlite3.Error) as e:
        print("No se ha podido hacer el pedido:", e)

def asignar(grafo):
    try:
        pedido = datos_pedido(int(input("Pedido (id): ")))
    except ValueError:
        print("Tiene que ser un número")
        return
    if pedido is None:
        print("No existe")
        return
    minutos, id_rider, nombre = rider_mas_cercano(grafo, pedido["restaurante"])
    dist, previo = dijkstra(grafo, pedido["restaurante"])
    print(f"Lo recoge {nombre}: {minutos} min hasta {pedido['restaurante']} "
          f"+ {dist[pedido['cliente']]} min hasta el cliente = {minutos + dist[pedido['cliente']]} min")
    print(" -> ".join(camino(previo, pedido["cliente"])))

def ruta(grafo):
    print("Barrios:", ", ".join(sorted(grafo)))
    origen, destino = input("Origen: "), input("Destino: ")
    if origen not in grafo or destino not in grafo:
        print("No existe")
        return
    dist, previo = dijkstra(grafo, origen)
    print(f"{dist[destino]} min:", " -> ".join(camino(previo, destino)))

def estadisticas():
    for r in pedidos_por_rider():
        print(f"{r['nombre']}: {r['pedidos']} pedidos, {r['facturado']:.2f} €")

def main():
    grafo = cargar_grafo()
    opciones = {
        "1": ("Ver la carta",            carta),
        "2": ("Hacer un pedido",         lambda: pedir(grafo)),
        "3": ("Rider para un pedido",    lambda: asignar(grafo)),
        "4": ("Ruta entre dos barrios",  lambda: ruta(grafo)),
        "5": ("Planificar el turno",     lambda: print(planificar_turno())),
        "6": ("Pedidos por rider",       estadisticas),
    }
    while True:
        for k, (texto, _) in opciones.items():
            print(k, texto)
        eleccion = input("Opción (q para salir): ")
        if eleccion == "q":
            break
        opciones.get(eleccion, ("", lambda: print("No existe")))[1]()

if __name__ == "__main__":
    main()
