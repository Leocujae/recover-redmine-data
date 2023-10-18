import json
import csv
import requests as request
#import boto3 
#from datetime import datetime, timedelta


def getIssues(KEY,Bucket='bucketfor008182637297',Key='redmine/issues/raw_data/issues.json'):
    
    headers = {
        "X-Redmine-API-Key": KEY
    }
    #Realizo una petición para saber el numero total de issues
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

    #export_jsom(values,'tasks/file/issues')
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
        if "id" in flattened_issue is None:
            flattened_issue['id'] = -1

        # flattened_issue['subject']
        if "subject" in flattened_issue is None:
            flattened_issue['subject'] = ""

        # flattened_issue['description']
        if  "description" in flattened_issue is None:
            flattened_issue['description'] = ""

        # flattened_issue['is_private']
        if "is_private" in flattened_issue is None:
            flattened_issue['is_private'] = ""

        # flattened_issue['done_ratio']
        if "done_ratio" in  flattened_issue is None:
            flattened_issue['done_ratio'] = -1

        # flattened_issue['closed_on']
        if "closed_on" in  flattened_issue is None:
            flattened_issue['closed_on'] = -1

        # flattened_issue['due_date']
        if "due_date" in flattened_issue is None:
            flattened_issue['due_date'] = -1
       
        # flattened_issue['start_date']
        if "start_date" in flattened_issue is None:
            flattened_issue['start_date'] = -1
            
        # flattened_issue['created_on']
        if "created_on" in flattened_issue is None:
            flattened_issue['created_on'] = -1
            
        # flattened_issue['updated_on']
        if "updated_on" in flattened_issue is None:
            flattened_issue['updated_on'] = -1
        
        # flattened_issue['estimated_hours']
        if "estimated_hours" in flattened_issue is None:
            flattened_issue['estimated_hours'] = -1

        #watchers 
        if "watchers" in flattened_issue :
            flattened_issue.pop('watchers')

        # notes
        if "notes" in flattened_issue is None:
            flattened_issue['notes'] = ""
            
        # private_notes
        if "private_notes" in flattened_issue is None:
            flattened_issue['private_notes'] = ""


        # Aplanar campos
        # project
        if "project" in flattened_issue:
            project = dict(flattened_issue['project'])
            flattened_issue.pop('project')
            flattened_issue['project_id'] = project.get('id')
            flattened_issue['project_name'] = project.get('name')
        else:
            flattened_issue['project_id'] = -1
            flattened_issue['project_name'] = ''
        
        # tracker
        if "tracker" in flattened_issue:
            tracker = dict(flattened_issue['tracker'])
            flattened_issue.pop('tracker')
            flattened_issue['tracker_id'] = tracker.get('id')
            flattened_issue['tracker_name'] = tracker.get('name')
        else:
            flattened_issue['tracker_id'] = -1
            flattened_issue['tracker_name'] = ''
       
        # status
        if "status" in flattened_issue:
            status = dict(flattened_issue['status'])
            flattened_issue.pop('status')
            flattened_issue['status_id'] = status.get('id')
            flattened_issue['status_name'] = status.get('name')
        else:
            flattened_issue['status_id'] = -1
            flattened_issue['status_name'] = ''
        
        # priority
        if "priority" in flattened_issue:
            priority = dict(flattened_issue['priority'])
            flattened_issue.pop('priority')
            flattened_issue['priority_id'] = priority.get('id')
            flattened_issue['priority_name'] = priority.get('name')
        else:
            flattened_issue['priority_id'] = -1
            flattened_issue['priority_name'] = ''
        

        # author
        if "author" in flattened_issue:
            author = dict(flattened_issue['author'])
            flattened_issue.pop('author')
            flattened_issue['author_id'] = author.get('id')
            flattened_issue['author_name'] = author.get('name')
        else:
            flattened_issue['author_id'] = -1
            flattened_issue['author_name'] = ''
        

        # assigned_to
        if "assigned_to" in flattened_issue:
            assigned_to = dict(flattened_issue['assigned_to'])
            flattened_issue.pop('assigned_to')
            flattened_issue['assigned_to_id'] = assigned_to.get('id')
            flattened_issue['assigned_to_name'] = assigned_to.get('name')
        else:
            flattened_issue['assigned_to_id'] = -1
            flattened_issue['assigned_to_name'] = ''


        # custom_fields
        flattened_issue['Severity'] = -1
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
            flattened_issue['parent_id'] = -1

        # fixed_version'
        if "fixed_version" in flattened_issue:
            fixed_version = dict(flattened_issue).get('fixed_version')
            flattened_issue.pop('fixed_version')
            flattened_issue['fixed_version_id'] = fixed_version.get("id")
            flattened_issue['fixed_version_name'] = fixed_version.get("name")
        else:
            flattened_issue['fixed_version_id'] = -1
            flattened_issue['fixed_version_name'] = ""

        # categories
        if "category" in flattened_issue:
            categories = dict(flattened_issue).get('category')
            flattened_issue.pop('category')
            flattened_issue['category_id'] = categories.get('id')
            flattened_issue['category_name'] = categories.get('name')
        else:
            flattened_issue['category_id'] = -1
            flattened_issue['category_name'] = ""

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
        json.dump(flattened_data, file)

    """header = flattened_data[0].keys()
    with open(path +'.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(flattened_data)

    for temp in flattened_data:
        print(temp)
        print("")
    """
