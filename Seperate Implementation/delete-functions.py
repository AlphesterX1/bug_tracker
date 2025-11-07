import mysql.connector

username = ''
password = ''

connectione = mysql.connector.connect(host='localhost', user=username, password = password, database = 'bug_tracker_db', auth_plugin='mysql_native_password')

mycursor = connectione.cursor()

target_table = ''
target_field = ''
target_condition = '' 


def delete_user():
    userId = input('Enter User email: ')
    c = input('Are you sure you want to delete this guy? (Y)es or (N)o')
    if c[0].lower() == 'y':
        target_table = 'users'
        target_field = 'email'
        target_condition = userId
        query_structure = f"DELETE FROM {target_table} WHERE {target_field} = '{target_condition}'"
        mycursor.execute(query_structure)
        connectione.commit()

def delete_project():
    userId = input('Enter Project ID: ')
    c = input('Are you sure you want to delete this guy? (Y)es or (N)o')
    if c[0].lower() == 'y':
        target_table = 'projects'
        target_field = 'project_id'
        target_condition = userId
        query_structure = f"DELETE FROM {target_table} WHERE {target_field} = '{target_condition}'"
        mycursor.execute(query_structure)
        connectione.commit()

def delete_issue():
    userId = input('Enter Issue ID: ')
    c = input('Are you sure you want to delete this guy? (Y)es or (N)o')
    if c[0].lower() == 'y':
        target_table = 'issues'
        target_field = 'issue_id'
        target_condition = userId
        query_structure = f"DELETE FROM {target_table} WHERE {target_field} = '{target_condition}'"
        mycursor.execute(query_structure)
        connectione.commit()

def delete_comment():
    userId = input('Enter Comment ID: ')
    c = input('Are you sure you want to delete this guy? (Y)es or (N)o')
    if c[0].lower() == 'y':
        target_table = 'comments'
        target_field = 'comment_id'
        target_condition = userId
        query_structure = f"DELETE FROM {target_table} WHERE {target_field} = '{target_condition}'"
        mycursor.execute(query_structure)
        connectione.commit()
     
print('Enter your options for deleting: (U)ser (P)roject (I)ssue (C)omment')
while True:
    prompt = input('> ')
    if prompt[0].lower() == 'u':
        delete_user()
    elif prompt[0].lower() == 'p':
        delete_project()
    elif prompt[0].lower() == 'i':
        delete_issue()
    elif prompt[0].lower() == 'c':
        delete_comment()
    else:
        print('Invalid Command Entered')
        
    






