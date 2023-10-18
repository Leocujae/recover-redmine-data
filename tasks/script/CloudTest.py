import Issues_Redmine


value = Issues_Redmine.getIssues("047f85e0b24fe4d7651e576fedd11ad410336e2d")
flattened_data = Issues_Redmine.flattenJSON(value)
Issues_Redmine.saveS3(flattened_data)