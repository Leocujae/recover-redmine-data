import Issues_Redmine




values = Issues_Redmine.conection()
flattened_data = Issues_Redmine.flattenJSON(values)
Issues_Redmine.export_jsom(flattened_data)