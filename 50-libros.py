import random
import requests

base_url = "http://library.demo.local/api/v1"

# 1. Autenticación para obtener el token de acceso
print("Autenticando en la API...")
auth_resp = requests.post(
    f"{base_url}/loginViaBasic", auth=("cisco", "Cisco123!")
)
token = auth_resp.json().get("token")
headers = {"X-API-KEY": token, "Content-Type": "application/json"}

# Listas con nombres, títulos y autores reales con sentido
lista_titulos = [
    "El Señor de los Anillos",
    "Cien Años de Soledad",
    "Don Quijote de la Mancha",
    "Crimen y Castigo",
    "La Odisea",
    "Orgullo y Prejuicio",
    "La Metamorfosis",
    "Fahrenheit 451",
    "1984",
    "Rebelión en la Granja",
    "El Principito",
    "La Sombra del Viento",
    "Rayuela",
    "Pedro Páramo",
    "Los Juegos del Hambre",
]

lista_autores = [
    "Gabriel García Márquez",
    "Isabel Allende",
    "Jorge Luis Borges",
    "Pablo Neruda",
    "Mario Vargas Llosa",
    "Julio Cortázar",
    "Miguel de Cervantes",
    "Fiódor Dostoyevski",
    "Jane Austen",
    "George Orwell",
    "Ray Bradbury",
    "Franz Kafka",
    "Carlos Ruiz Zafón",
    "Juan Rulfo",
    "Alejandro Casona",
]

# 2. Generar y agregar 50 libros adicionales al azar (IDs del 10 al 59)
print("\n--- Agregando 50 libros con nombres reales y con sentido ---")
for i in range(10, 60):
  # Seleccionar título y autor de forma aleatoria de las listas con sentido
  titulo_elegido = random.choice(lista_titulos)
  autor_elegido = random.choice(lista_autores)

  # Añadimos la iteración para mantener títulos únicos en cada registro
  titulo_final = f"{titulo_elegido} (Vol. {i})"
  isbn_azar = "".join(random.choices("0123456789", k=9))

  payload = {
      "id": i,
      "title": titulo_final,
      "author": autor_elegido,
      "isbn": f"978-{isbn_azar}",
  }

  response = requests.post(f"{base_url}/books", json=payload, headers=headers)
  print(f"Libro ID {i} creado - Código HTTP: {response.status_code}")

# 3. Listar la totalidad de los libros creados incluyendo el ISBN
print("\n--- Listado total de libros del catálogo (Ordenados por Autor) ---")
list_params = {"includeISBN": "true", "sortBy": "author"}
list_response = requests.get(f"{base_url}/books", params=list_params)

if list_response.status_code == 200:
  libros = list_response.json()
  for libro in libros:
    print(
        f"ID: {libro.get('id')} | Título: {libro.get('title')} | Autor:"
        f" {libro.get('author')} | ISBN: {libro.get('isbn', 'No disponible')}"
    )
else:
  print(f"Error al listar los libros: {list_response.status_code}")