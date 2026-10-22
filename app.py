from datetime import datetime
from db import (obtener_platos, obtener_usuarios, obtener_pedidos, barrio_de_plato,
                datos_pedido, pedidos_por_rider)
from pedidos import crear_pedido
from rutas import cargar_grafo, dijkstra, camino, rider_mas_cercano
from turno import planificar_turno


def carta():
    restaurante_actual = ""
    for p in obtener_platos():
        # cuando cambia el restaurante, escribimos su nombre como título
        if p['restaurante'] != restaurante_actual:
            restaurante_actual = p['restaurante']
            print()
            print("---", restaurante_actual, "---")
        print("  ", p['id_plato'], ".", p['nombre'], "-", p['precio'], "€")


def usuarios():
    for u in obtener_usuarios():
        print(u['id_usuario'], ".", u['nombre'], "-", u['barrio'], "- saldo:", u['saldo'], "€")


def pedidos():
    for p in obtener_pedidos():
        print(p['id_pedido'], ".", p['fecha'], "-", p['cliente'], "-", p['total'], "€")


def pedir(grafo):
    usuarios()
    id_usuario = int(input("¿Quién eres? (número): "))

    carta()
    print()
    print("Escribe el número del plato y la cantidad, por ejemplo: 3 2")

    # lista de (id_plato, cantidad)
    lineas = []
    while True:
        entrada = input("Plato y cantidad (vacío para acabar): ")
        if entrada == "":
            break
        partes = entrada.split()
        lineas.append((int(partes[0]), int(partes[1])))

    if len(lineas) == 0:
        print("No has pedido nada")
        return

    # el rider es el más cercano al restaurante del primer plato
    barrio = barrio_de_plato(lineas[0][0])
    minutos, id_rider, nombre = rider_mas_cercano(grafo, barrio)

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    id_pedido, total = crear_pedido(id_usuario, id_rider, lineas, fecha)
    print("Pedido", id_pedido, ":", total, "€, lo lleva", nombre,
          "(a", minutos, "min del restaurante)")


def asignar(grafo):
    pedidos()
    id_pedido = int(input("¿Qué pedido? (número): "))
    pedido = datos_pedido(id_pedido)
    if pedido is None:
        print("No existe")
        return

    restaurante = pedido["restaurante"]
    cliente = pedido["cliente"]

    minutos, _, nombre = rider_mas_cercano(grafo, restaurante)
    dist, previo = dijkstra(grafo, restaurante)
    total = minutos + dist[cliente]

    print("Lo recoge", nombre, ":", minutos, "min hasta", restaurante)
    print("Luego", dist[cliente], "min hasta el cliente. Total:", total, "min")
    print(" -> ".join(camino(previo, cliente)))


def ruta(grafo):
    print("Barrios:", ", ".join(sorted(grafo)))
    origen = input("Origen: ")
    destino = input("Destino: ")
    if origen not in grafo or destino not in grafo:
        print("No existe")
        return

    dist, previo = dijkstra(grafo, origen)
    print(dist[destino], "min:", " -> ".join(camino(previo, destino)))


def estadisticas():
    for r in pedidos_por_rider():
        print(r['nombre'], ":", r['pedidos'], "pedidos,", round(r['facturado'], 2), "€")


def main():
    grafo = cargar_grafo()

    while True:
        print()
        print("1. Ver la carta")
        print("2. Ver usuarios")
        print("3. Ver pedidos")
        print("4. Hacer un pedido")
        print("5. Rider para un pedido")
        print("6. Ruta entre dos barrios")
        print("7. Planificar el turno")
        print("8. Pedidos por rider")
        print("q. Salir")
        opcion = input("Opción: ")

        try:
            if opcion == "1":
                carta()
            elif opcion == "2":
                usuarios()
            elif opcion == "3":
                pedidos()
            elif opcion == "4":
                pedir(grafo)
            elif opcion == "5":
                asignar(grafo)
            elif opcion == "6":
                ruta(grafo)
            elif opcion == "7":
                print(planificar_turno())
            elif opcion == "8":
                estadisticas()
            elif opcion == "q":
                break
            else:
                print("No existe")
        except Exception as e:
            print("Ha habido un error:", e)


main()
