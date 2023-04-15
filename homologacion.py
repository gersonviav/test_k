import csv
import json
from fuzzywuzzy import fuzz

# Leer el archivo de universidades
with open('universidades.json', 'r') as f:
    universidades = json.load(f)

# Añadir la clave 'Sinonimos' en el diccionario de cada universidad
for u in universidades:
    u['Sinonimos'] = set()

# Leer el archivo de instituciones educativas
with open('instituciones_educativas.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = [row for row in reader]

sinonimos_diccionario = {}
for row in rows:
    universidad = row['value'].lower()
    homologada = None
    for u in universidades:
        nombre_uni = u['Nombre '].lower()
        siglas_uni = u['Siglas '].lower()
        # Comparar la cadena de texto de la universidad con el nombre y las siglas de las universidades
        if fuzz.ratio(universidad, nombre_uni) >= 80 or fuzz.ratio(universidad, siglas_uni) >= 80:
            homologada = u['Nombre ']
            break
    if not homologada:
        for s, sin in sinonimos_diccionario.items():
            if universidad in sin:
                homologada = s
                break
    if homologada:
        row['universidad_homologada'] = "Si"
        if homologada in sinonimos_diccionario:
            sinonimos_diccionario[homologada].add(universidad)
        else:
            sinonimos_diccionario[homologada] = set([universidad]) # Aquí se añade la línea que faltaba
    else:
        row['universidad_homologada'] = "No"

with open('instituciones_educativas_homologadas.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['candidateId', 'value', 'universidad_homologada']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow({'candidateId': row['candidateId'], 'value': row['value'], 'universidad_homologada': row['universidad_homologada']})
 
# Crear el diccionario de sinónimos con el formato solicitado
sinonimos_universidades = []
for homologada in sinonimos_diccionario:
    sinonimos_universidades.append({
        "nombre": homologada,
        "sinonimos": list(sinonimos_diccionario[homologada])
    })

# Escribir el archivo de sinónimos de universidades
with open('sinonimos_universidades.json', 'w', encoding='utf-8') as f:
    json.dump(sinonimos_universidades, f, ensure_ascii=False)