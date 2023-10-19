import Issues_Redmine
import json
import tkinter as tk
from tkinter import filedialog


root = tk.Tk()
root.withdraw()
#Issues_Redmine.getIssues("047f85e0b24fe4d7651e576fedd11ad410336e2d")
selected_file = filedialog.askopenfilename()
#Issues_Redmine.getIssues("047f85e0b24fe4d7651e576fedd11ad410336e2d")
if selected_file:
    # Abre el archivo JSON y carga su contenido
    with open(selected_file, 'r',encoding='utf-8') as archivo_json:
        values = json.load(archivo_json)
    
    flattened_data = Issues_Redmine.flattenJSON(values)
    Issues_Redmine.export_jsom(flattened_data)
    #Issues_Redmine.export_jsom(flattened_data)
else:
    print("No se ha seleccionado ninguna carpeta.")

root.destroy()


