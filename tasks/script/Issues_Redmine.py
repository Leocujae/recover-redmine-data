import json
import csv
import requests as request
#import boto3 
#from datetime import datetime, timedelta


def getIssues(KEY,Bucket='bucketfor008182637297',Key='redmine/issues/raw_data/issues.json'):
    
    headers = {
        "X-Redmine-API-Key": KEY
    }
    # Realizo una petición para saber el numero total de issues , aprovecho para cargar los primeros 100
    # creo la variable values y la tomo como base para almacenar el resto de issues 

    i = 100
    url = "https://redmine.generalsoftwareinc.com/issues.json?offset=0&limit=100"
    response = request.get(url, headers=headers)
    resp = response.json()
    values = resp.copy()
    
    limit = values.get("total_count")
    
    #Recuperar todos los issues
    while(i <= limit):
        url = "https://redmine.generalsoftwareinc.com/issues.json?offset="+str(i)+"&limit=100"
        response = request.get(url, headers=headers)
        resp = response.json()
        values["issues"].extend(resp.get("issues"))
        i +=100
        print(i)

    export_jsom(values,'tasks/file/issues')
    #Sustituir por el código para almacenar en S3 que está funcional 
    """ # writing projects to raw folder in S3 Bucket 
    s3 = boto3.client('s3')
    s3.put_object( 
        Body=(bytes(json.dumps(values).encode('UTF-8'))),     
        Bucket=Bucket, 
        Key=Key)      """
    return values

def flattenJSON(values):
    # Flatten the JSON data
    # MISSING VALUES   
    MISSING_DATE    = "1999-1-1"
    MISSING_TEXT  = ""
    MISSING_VALUE   = "-1"
    
    if "issues" in values is None :
        raise ValueError("Error: The JSON file is corrupted or invalid. Please check the file format and try again.")
    
    issues = dict(values.items()).get('issues')
    if issues is None:
        raise ValueError("Error: The JSON file is corrupted or invalid. Please check the file format and try again.")
    
    
    flattened_data = []
    for issue in issues:
        # Copia el issue original para no modificarlo
        flattened_issue = issue.copy()

        # flattened_issue['id']
        if not("id" in flattened_issue and flattened_issue["id"] is not None):
            flattened_issue['id'] = MISSING_VALUE

        # flattened_issue['subject']
        if not("subject" in flattened_issue and flattened_issue["subject"] is not None):
            flattened_issue['subject'] = MISSING_TEXT

        # flattened_issue['description']
        if not("description" in flattened_issue and flattened_issue["description"] is not None):
            flattened_issue['description'] = MISSING_TEXT

        # flattened_issue['is_private']
        if not("is_private" in flattened_issue and flattened_issue["is_private"] is not None):
            flattened_issue['is_private'] = MISSING_TEXT

        # flattened_issue['done_ratio']
        if not("done_ratio" in  flattened_issue and flattened_issue["done_ratio"] is not None):
            flattened_issue['done_ratio'] = 0

        # flattened_issue['closed_on']
        if not("closed_on" in  flattened_issue and flattened_issue["closed_on"] is not None):
            flattened_issue['closed_on'] = MISSING_DATE

        # flattened_issue['due_date']
        if not("due_date" in flattened_issue and flattened_issue["due_date"] is not None):
            flattened_issue['due_date'] = MISSING_DATE
       
        # flattened_issue['start_date']
        if not("start_date" in flattened_issue and flattened_issue["start_date"] is not None):
            flattened_issue['start_date'] = MISSING_DATE
            
        # flattened_issue['created_on']
        if not("created_on" in flattened_issue and flattened_issue["created_on"] is not None):
            flattened_issue['created_on'] = MISSING_DATE
            
        # flattened_issue['updated_on']
        if not("updated_on" in flattened_issue and flattened_issue["updated_on"] is not None):
            flattened_issue['updated_on'] = MISSING_DATE
        
        # flattened_issue['estimated_hours']
        if not("estimated_hours" in flattened_issue and flattened_issue["estimated_hours"] is not None):
            flattened_issue['estimated_hours'] = MISSING_VALUE

        #watchers 
        if "watchers" in flattened_issue :
            flattened_issue.pop('watchers')

        # notes
        if not("notes" in flattened_issue  and flattened_issue['notes'] is not None):
            flattened_issue['notes'] = MISSING_TEXT
            
        # private_notes
        if not("private_notes" in flattened_issue and flattened_issue["private_notes"] is not None):
            flattened_issue['private_notes'] = MISSING_TEXT


        # Aplanar campos
        # project
        if "project" in flattened_issue:
            project = dict(flattened_issue['project'])
            flattened_issue.pop('project')
            flattened_issue['project_id'] = project.get('id')
            flattened_issue['project_name'] = project.get('name')
        else:
            flattened_issue['project_id'] = MISSING_VALUE
            flattened_issue['project_name'] = MISSING_TEXT
        
        # tracker
        if "tracker" in flattened_issue:
            tracker = dict(flattened_issue['tracker'])
            flattened_issue.pop('tracker')
            flattened_issue['tracker_id'] = tracker.get('id')
            flattened_issue['tracker_name'] = tracker.get('name')
        else:
            flattened_issue['tracker_id'] = MISSING_VALUE
            flattened_issue['tracker_name'] = MISSING_TEXT
       
        # status
        if "status" in flattened_issue:
            status = dict(flattened_issue['status'])
            flattened_issue.pop('status')
            flattened_issue['status_id'] = status.get('id')
            flattened_issue['status_name'] = status.get('name')
        else:
            flattened_issue['status_id'] = MISSING_VALUE
            flattened_issue['status_name'] = MISSING_TEXT
        
        # priority
        if "priority" in flattened_issue:
            priority = dict(flattened_issue['priority'])
            flattened_issue.pop('priority')
            flattened_issue['priority_id'] = priority.get('id')
            flattened_issue['priority_name'] = priority.get('name')
        else:
            flattened_issue['priority_id'] = MISSING_VALUE
            flattened_issue['priority_name'] = MISSING_TEXT
        

        # author
        if "author" in flattened_issue:
            author = dict(flattened_issue['author'])
            flattened_issue.pop('author')
            flattened_issue['author_id'] = author.get('id')
            flattened_issue['author_name'] = author.get('name')
        else:
            flattened_issue['author_id'] = MISSING_VALUE
            flattened_issue['author_name'] = MISSING_TEXT
        

        # assigned_to
        if "assigned_to" in flattened_issue:
            assigned_to = dict(flattened_issue['assigned_to'])
            flattened_issue.pop('assigned_to')
            flattened_issue['assigned_to_id'] = assigned_to.get('id')
            flattened_issue['assigned_to_name'] = assigned_to.get('name')
        else:
            flattened_issue['assigned_to_id'] = MISSING_VALUE
            flattened_issue['assigned_to_name'] = MISSING_TEXT


        # custom_fields
        flattened_issue['Severity'] = MISSING_VALUE
        if "custom_fields" in flattened_issue:
            custom_fields = dict(flattened_issue).get('custom_fields')
            flattened_issue.pop('custom_fields')
            for field in custom_fields:
                if field['name'] == "Severity":
                    flattened_issue['Severity'] = field['value']
                    break

        # parent
        if "parent" in flattened_issue:
            parent = dict(flattened_issue).get('parent')
            flattened_issue.pop('parent')
            flattened_issue['parent_id'] = parent.get("id")
        else:
            flattened_issue['parent_id'] = MISSING_VALUE

        # fixed_version'
        if "fixed_version" in flattened_issue:
            fixed_version = dict(flattened_issue).get('fixed_version')
            flattened_issue.pop('fixed_version')
            flattened_issue['fixed_version_id'] = fixed_version.get("id")
            flattened_issue['fixed_version_name'] = fixed_version.get("name")
        else:
            flattened_issue['fixed_version_id'] = MISSING_VALUE
            flattened_issue['fixed_version_name'] = MISSING_TEXT

        # categories
        if "category" in flattened_issue:
            categories = dict(flattened_issue).get('category')
            flattened_issue.pop('category')
            flattened_issue['category_id'] = categories.get('id')
            flattened_issue['category_name'] = categories.get('name')
        else:
            flattened_issue['category_id'] = MISSING_VALUE
            flattened_issue['category_name'] = MISSING_TEXT

        flattened_data.append(flattened_issue)
    return flattened_data

def saveS3(flattened_data,Bucket='bucketfor008182637297',Key='redmine/issues/flatten_data/issues/issues.json'):
    s3 = boto3.client('s3')
    s3.put_object( 
     Body=(bytes(json.dumps(flattened_data).encode('UTF-8'))),     
     Bucket=Bucket, 
     Key=Key) 

def export_jsom(flattened_data,path = 'tasks/file/flattened_data_issues'):
 
    path = path + ".json"
    with open(path, 'w') as file:
        json.dump(flattened_data, file, indent=4)

    """header = flattened_data[0].keys()
    with open(path +'.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(flattened_data)

    for temp in flattened_data:
        print(temp)
        print("")
    """
