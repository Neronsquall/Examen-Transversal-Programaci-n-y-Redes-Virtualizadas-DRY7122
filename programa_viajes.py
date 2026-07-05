import requests

# ==============================
# CONFIGURACIÓN
# ==============================

API_KEY = "c8bd4c3c-d194-40b9-9a35-305ecaa4c0ce"

# Función para obtener coordenadas desde el nombre de la ciudad
def obtener_coordenadas(ciudad):
    url = "https://graphhopper.com/api/1/geocode"

    parametros = {
        "q": ciudad,
        "locale": "es",
        "limit": 1,
        "key": API_KEY
    }

    respuesta = requests.get(url, params=parametros)

    if respuesta.status_code != 200:
        return None

    datos = respuesta.json()

    if len(datos["hits"]) == 0:
        return None

    lat = datos["hits"][0]["point"]["lat"]
    lon = datos["hits"][0]["point"]["lng"]

    return lat, lon


# Función para obtener la ruta
def obtener_ruta(origen, destino, transporte):

    url = "https://graphhopper.com/api/1/route"

    parametros = {
        "point": [
            f"{origen[0]},{origen[1]}",
            f"{destino[0]},{destino[1]}"
        ],
        "profile": transporte,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": API_KEY
    }

    respuesta = requests.get(url, params=parametros)

    if respuesta.status_code != 200:
        return None

    return respuesta.json()


# ==============================
# PROGRAMA PRINCIPAL
# ==============================

print("=========================================")
print("     RUTAS CHILE - PERÚ (GraphHopper)")
print("=========================================")

while True:

    ciudad_origen = input("\nCiudad de Origen (o s para salir): ")

    if ciudad_origen.lower() == "s":
        print("Programa finalizado.")
        break

    ciudad_destino = input("Ciudad de Destino (o s para salir): ")

    if ciudad_destino.lower() == "s":
        print("Programa finalizado.")
        break

    print("\nMedios de transporte:")

    print("1. Automóvil")
    print("2. Bicicleta")
    print("3. Caminando")

    opcion = input("Seleccione una opción: ")

    perfiles = {
        "1": "car",
        "2": "bike",
        "3": "foot"
    }

    if opcion not in perfiles:
        print("Opción inválida.")
        continue

    transporte = perfiles[opcion]

    print("\nBuscando ciudades...")

    origen = obtener_coordenadas(ciudad_origen + ", Chile")
    destino = obtener_coordenadas(ciudad_destino + ", Perú")

    if origen is None:
        print("No se encontró la ciudad de origen.")
        continue

    if destino is None:
        print("No se encontró la ciudad de destino.")
        continue

    print("Calculando ruta...")

    ruta = obtener_ruta(origen, destino, transporte)

    if ruta is None or "paths" not in ruta:
        print("No fue posible calcular la ruta.")
        continue

    datos = ruta["paths"][0]

    distancia_km = datos["distance"] / 1000
    distancia_millas = distancia_km * 0.621371

    tiempo_seg = datos["time"] / 1000

    horas = int(tiempo_seg // 3600)
    minutos = int((tiempo_seg % 3600) // 60)

    print("\n========== RESULTADOS ==========")

    print(f"Origen : {ciudad_origen}, Chile")
    print(f"Destino: {ciudad_destino}, Perú")
    print(f"Transporte: {transporte}")

    print(f"\nDistancia: {distancia_km:.2f} km")
    print(f"Distancia: {distancia_millas:.2f} millas")

    print(f"Duración: {horas} horas {minutos} minutos")

    print("\nNarrativa del viaje:")

    for paso in datos["instructions"]:
        print("-", paso["text"])

    print("\n====================================")
