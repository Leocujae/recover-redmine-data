
import json
from datetime import datetime, timedelta



def calcular_fecha_ultima_semana():
    hoy = datetime.now()
    
    lunes_semana_actual = hoy - timedelta(hoy.weekday())
    lunes_semana_actual = lunes_semana_actual.replace(hour=0, minute=0, second=0, microsecond=0)
    print(lunes_semana_actual)
    return lunes_semana_actual



#obtener proyectos modificados en la ultima semana
def function(url='tasks/test/Test-6.json', BeginningWeek=calcular_fecha_ultima_semana()):

 filter_data = [] 
 missin_value =[]
 
 with open(url, 'r') as archivo_json:
    json_obj = json.load(archivo_json)
 
 for project in json_obj:
     #Agregar manejo de excepciones 
     try:
        date = datetime.strptime(project.get("updated_on"), "%Y-%m-%dT%H:%M:%SZ")
        if date > BeginningWeek:
            filter_data.append(project)
     except:
         print("The update date has incorrect values "+ "project ID :" +  str(project.get("id")))
         missin_value.append(project.get("id"))
 filter_data.append({"count":len(filter_data)})
 
 if(len(missin_value) > 0):
    with open('tasks/file/log_issues.json', 'w') as file:
        json.dump(missin_value, file)
 
 return filter_data
 
 
 
print(function())