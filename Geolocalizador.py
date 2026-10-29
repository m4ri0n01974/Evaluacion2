import urllib.parse
import requests

main_api = "https://graphhopper.com/api/1/route?"
key = "8e363d7f-6b0c-4e87-9934-381e9cf1331c"


def geocoding(location, api_key):
  geocode_url = "https://graphhopper.com/api/1/geocode?"
  url = geocode_url + urllib.parse.urlencode(
      {"q": location, "limit": "1", "key": api_key}
  )
  reply = requests.get(url)
  json_data = reply.json()

  if reply.status_code == 200 and len(json_data.get("hits", [])) > 0:
    lat = json_data["hits"][0]["point"]["lat"]
    lng = json_data["hits"][0]["point"]["lng"]
    return 200, lat, lng
  else:
    return reply.status_code, None, None


def main():
  while True:
    origen = input(
        "\nIngrese el punto de origen (o escriba 's' / 'salir' para terminar): "
    ).strip()
    if origen.lower() in ["s", "salir"]:
      print("Saliendo del programa de geolocalización. ¡Hasta luego!")
      break

    destino = input(
        "Ingrese el punto de destino (o escriba 's' / 'salir' para terminar): "
    ).strip()
    if destino.lower() in ["s", "salir"]:
      print("Saliendo del programa de geolocalización. ¡Hasta luego!")
      break

    # Obtener coordenadas de origen y destino
    orig_status, orig_lat, orig_lng = geocoding(origen, key)
    dest_status, dest_lat, dest_lng = geocoding(destino, key)

    if orig_status == 200 and dest_status == 200:
      # Construcción corregida de la URL usando doseq=True para aceptar múltiples puntos
      op_url = main_api + urllib.parse.urlencode(
          {
              "point": [f"{orig_lat},{orig_lng}", f"{dest_lat},{dest_lng}"],
              "vehicle": "car",
              "locale": "es",
              "instructions": "true",
              "key": key,
          },
          doseq=True,
      )

      response = requests.get(op_url)
      paths_data = response.json()

      # Verificamos si la API devolvió la ruta correctamente
      if response.status_code == 200 and "paths" in paths_data:
        path = paths_data["paths"][0]

        distancia_km = path["distance"] / 1000
        tiempo_min = path["time"] / 1000 / 60

        print(f"\n--- RESUMEN DEL VIAJE ---")
        print(f"Distancia total: {distancia_km:.2f} km")
        print(f"Tiempo estimado: {tiempo_min:.2f} minutos")

        print("\n--- NARRATIVA DEL VIAJE (PASO A PASO) ---")
        for paso in path.get("instructions", []):
          texto_instruccion = paso["text"]
          dist_paso = paso["distance"] / 1000
          print(f"- {texto_instruccion} ({dist_paso:.2f} km)")
      else:
        print(
            "Error de la API de rutas: No se pudo procesar el trayecto entre"
            " los puntos."
        )
        print(
            "Detalle del error:", paths_data.get("message", "Desconocido")
        )
    else:
      print(
          "Error: No se pudieron encontrar las coordenadas geográficas para"
          " el origen o destino ingresado. Intente con otra ubicación."
      )


if __name__ == "__main__":
  main()