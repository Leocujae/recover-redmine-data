import Issues_Redmine
import json


ruta_al_json = "tasks/test_flattened_data/Test-3.json"

# Abre el archivo JSON y carga su contenido
with open(ruta_al_json, 'r') as archivo_json:
    values = json.load(archivo_json)

flattened_data = Issues_Redmine.flattenJSON(values)
print(flattened_data)