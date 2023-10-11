import Issues_Redmine
import json
import tkinter as tk
from tkinter import filedialog


root = tk.Tk()
root.withdraw()

selected_file = filedialog.askopenfilename()


if selected_file:
    # Abre el archivo JSON y carga su contenido
    with open(selected_file, 'r') as archivo_json:
        values = json.load(archivo_json)
    
    flattened_data = Issues_Redmine.flattenJSON(values)
    
    Issues_Redmine.export_jsom(flattened_data)
    print(flattened_data)
    
else:
    print("No se ha seleccionado ninguna carpeta.")

root.destroy()


