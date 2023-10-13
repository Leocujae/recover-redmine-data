import json
import csv
import requests as request
from datetime import datetime, timedelta

def conection(KEY):

    headers = {
        "X-Redmine-API-Key": KEY
    }

    url = "https://redmine.generalsoftwareinc.com/issues.json"
    response = request.get(url, headers=headers)
    values = response.json()
    return values

def flattenJSON(values):
    # Flatten the JSON data
        
    issues = dict(values.items()).get('issues')
    if issues is None :
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
            flattened_issue['done_ratio'] = ""

        # flattened_issue['closed_on']
        if "closed_on" in  flattened_issue is None:
            flattened_issue['closed_on'] = ""

        # flattened_issue['due_date']
        if "due_date" in flattened_issue is None:
            flattened_issue['due_date'] = "-1"
       
        # flattened_issue['start_date']
        if "start_date" in flattened_issue is None:
            flattened_issue['start_date'] = "-1"
            
        # flattened_issue['created_on']
        if "created_on" in flattened_issue is None:
            flattened_issue['created_on'] = ""
            
        # flattened_issue['updated_on']
        if "updated_on" in flattened_issue is None:
            flattened_issue['updated_on'] = ""
        
        # flattened_issue['estimated_hours']
        if "estimated_hours" in flattened_issue is None:
            flattened_issue['estimated_hours'] = -1

        # Aplanar campos
        # project
        project = dict(flattened_issue['project'])
        if project is not None:
            flattened_issue.pop('project')
            flattened_issue['project_id'] = project.get('id')
            flattened_issue['project_name'] = project.get('name')
        else:
            flattened_issue['project_id'] = -1
            flattened_issue['project_name'] = ''
        

        """#watchers 
        if dict(flattened_issue['watchers']) is not None:
            flattened_issue.pop('watchers')"""

        # tracker
        tracker = dict(flattened_issue['tracker'])
        if tracker is not None:
            flattened_issue.pop('tracker')
            flattened_issue['tracker_id'] = tracker.get('id')
            flattened_issue['tracker_name'] = tracker.get('name')
        else:
            flattened_issue['tracker_id'] = -1
            flattened_issue['tracker_name'] = ''
       

        # status
        status = dict(flattened_issue['status'])
        if status is not None:
            flattened_issue.pop('status')
            flattened_issue['status_id'] = status.get('id')
            flattened_issue['status_name'] = status.get('name')
        else:
            flattened_issue['status_id'] = -1
            flattened_issue['status_name'] = ''
        

        # priority
        priority = dict(flattened_issue['priority'])
        if priority is not None:
            flattened_issue.pop('priority')
            flattened_issue['priority_id'] = priority.get('id')
            flattened_issue['priority_name'] = priority.get('name')
        else:
            flattened_issue['priority_id'] = -1
            flattened_issue['priority_name'] = ''
        

        # author
        author = dict(flattened_issue['author'])
        if author is not None:
            flattened_issue.pop('author')
            flattened_issue['author_id'] = author.get('id')
            flattened_issue['author_name'] = author.get('name')
        else:
            flattened_issue['author_id'] = -1
            flattened_issue['author_name'] = ''
        

        # assigned_to
        assigned_to = dict(flattened_issue['assigned_to'])
        if assigned_to is not None:
            flattened_issue.pop('assigned_to')
            flattened_issue['assigned_to_id'] = assigned_to.get('id')
            flattened_issue['assigned_to_name'] = assigned_to.get('name')
        else:
            flattened_issue['assigned_to_id'] = -1
            flattened_issue['assigned_to_name'] = ''


        # custom_fields
        custom_fields = dict(flattened_issue).get('custom_fields')
        flattened_issue['Severity'] = -1
        if custom_fields is not None:
            flattened_issue.pop('custom_fields')
            for field in custom_fields:
                if field['name'] == "Severity":
                    flattened_issue['Severity'] = field['value']
                    break

        # parent
        parent = dict(flattened_issue).get('parent')
        if parent is not None:
            flattened_issue.pop('parent')
            flattened_issue['parent_id'] = parent.get("id")
        else:
            flattened_issue['parent_id'] = -1

        # fixed_version'
        fixed_version = dict(flattened_issue).get('fixed_version')
        if fixed_version is not None:
            flattened_issue.pop('fixed_version')
            flattened_issue['fixed_version_id'] = fixed_version.get("id")
            flattened_issue['fixed_version_name'] = fixed_version.get("name")
        else:
            flattened_issue['fixed_version_id'] = -1
            flattened_issue['fixed_version_name'] = ""

        # categories
        categories = dict(flattened_issue).get('category')
        if categories is not None:
            flattened_issue.pop('category')
            flattened_issue['category_id'] = categories.get('id')
            flattened_issue['category_name'] = categories.get('name')
        else:
            flattened_issue['category_id'] = -1
            flattened_issue['category_name'] = ""

        """#relaciones
        relations = dict(flattened_issue).get('relations')
        if dict(flattened_issue).get('relations') is not None:
            for relation in relations:
                flattened_issue['relation_issue_id']= relation['issue_id']
                flattened_issue['relation_issue_type'] = relation['relation_type']
        else :
            flattened_issue['relation_issue_id'] = -1
            flattened_issue['relation_issue_type'] ="""""

        # notes
        if dict(flattened_issue).get('notes') is None:
            flattened_issue['notes'] = ""
        # private_notes
        if dict(flattened_issue).get('private_notes') is None:
            flattened_issue['private_notes'] = ""

        flattened_data.append(flattened_issue)
    return flattened_data

def export_jsom(flattened_data,path = 'tasks/file/flattened_data_issues_'):
    path = path + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".json"

    with open(path, 'w') as file:
        json.dump(flattened_data, file)

    header = flattened_data[0].keys()
    with open(path +'.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(flattened_data)

    for temp in flattened_data:
        print(temp)
        print("")



