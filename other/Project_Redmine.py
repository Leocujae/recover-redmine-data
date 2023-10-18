import requests as request 
#import GlueContext 
#import boto3 
import json 
import csv
#import StringIO 
#import requests as request 
#from awsglue.transforms import *
#from awsglue.utils import getResolvedOptionsfrom pyspark.context 
#import SparkContext 
#from pyspark.sql import SparkSessionfrom awsglue.context 

headers = {
    "X-Redmine-API-Key": "047f85e0b24fe4d7651e576fedd11ad410336e2d"
}



# writing projects to raw folder in S3 Bucket 
""" s3 = boto3.client('s3')
s3.put_object( 
     Body=(bytes(json.dumps(values).encode('UTF-8'))),     
     Bucket='bucketfor008182637297', 
     Key='redmine/projects/raw_data/projects.json')  """


url = "https://redmine.generalsoftwareinc.com/projects.json?offset=0&limit=100"
response = request.get(url, headers=headers)
values = response.json()
# Flatten the JSON data
projects = dict(values.items()).get('projects')

flattened_data = []
for project in projects:
    custom_fields = dict(project).get('custom_fields')
    parent = dict(project).get('parent')
    if parent is not None:
        project.pop('parent')
    project.pop('custom_fields')
    flattened_project = project.copy()
    # procesamiento del custom_field
    for field in custom_fields:
        flattened_project['custom_fields_id'] = field['id']
        flattened_project['custom_fields_name'] = field['name']
        flattened_project['custom_fields_value'] = field['value']

    # procesamiento del parent
    if parent is not None:
        flattened_project['parent_id'] = dict(parent).get('id')
        flattened_project['parent_name'] = dict(parent).get('name')
    else:
        flattened_project['parent_id'] = -1
        flattened_project['parent_name'] = ""
    flattened_data.append(flattened_project)

# Write the flattened data to a CSV file

with open('flattened_data2.json', 'w') as file:
    json.dump(flattened_data, file)

header = flattened_data[0].keys()
with open('flattened_data.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    writer.writerows(flattened_data)
print(projects)
print(flattened_data)


""" s3.put_object( 
     Body=(bytes(json.dumps(flattened_data).encode('UTF-8'))),     
     Bucket='bucketfor008182637297', 
     Key='redmine/projects/flatten_data/projects/projects.json') 

csv_buffer = StringIO() 
header = flattened_data[0].keys()# Write the CSV data to the in-memory buffer 
writer = csv.DictWriter(csv_buffer, fieldnames=header)
writer.writeheader() 
writer.writerows(flattened_data) 
# Get the CSV contents from the buffercsv_content = csv_buffer.getvalue() 
# Close the buffer 
csv_buffer.close() 

s3.put_object(     
     Body=csv_content, 
     Bucket='bucketfor008182637297',     
     Key='redmine/projects/flatten_csv/projects/projects_csv.csv' 
) """