import mysql.connector
from mysql.connector import Error
import sys

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
        sys.exit(f"Failed to connect to database: {e}")
    return connection

#-- INSERT --#
def add_new_user(connection, username, email):
    cursor = connection.cursor()
    query = "INSERT INTO Users (username, email) VALUES (%s, %s)"
    try:
        cursor.execute(query, (username, email))
        connection.commit()  
        user_id = cursor.lastrowid
        print(f"User '{username}' added successfully with ID: {user_id}.")
        return user_id  
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()

def add_new_project(connection, name, description):
    cursor = connection.cursor()
    query = "INSERT INTO Projects (name, description) VALUES (%s, %s)"
    try:
        cursor.execute(query, (name, description))
        connection.commit()
        project_id = cursor.lastrowid
        print(f"Project '{name}' added successfully with ID: {project_id}.")
        return project_id 
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()

def report_new_issue(connection, project_id, reported_by_user_id, title, description, priority="Medium"):
    cursor = connection.cursor()
    query = """
    INSERT INTO Issues 
    (project_id, reported_by_user_id, title, description, priority) 
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (project_id, reported_by_user_id, title, description, priority))
        connection.commit()
        issue_id = cursor.lastrowid
        print(f"New issue '{title}' reported successfully with ID: {issue_id}.")
        return issue_id 
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()

#-- UPDATE --#
def update_issue_status(connection, issue_id: int, status: str):
    if status not in ('Open', 'In Progress', 'Closed'):
        print(f"Invalid status: {status}. Must be 'Open', 'In Progress', or 'Closed'.")
        return
        
    cursor = connection.cursor()
    query = "UPDATE Issues SET status = %s WHERE issue_id = %s"
    try:
        cursor.execute(query, (status, issue_id))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"-> Updated issue {issue_id} status to '{status}'")
        else:
            print(f"-> No issue found with ID {issue_id}. No updates made.")
    except Error as e:
        print(f"The error '{e}' occurred while updating issue status")
    finally:
        cursor.close()


def assign_issue(connection, issue_id: int, assigned_to_user_id: int):
    cursor = connection.cursor()
    query = "UPDATE Issues SET assigned_to_user_id = %s WHERE issue_id = %s"
    try:
        cursor.execute(query, (assigned_to_user_id, issue_id))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"-> Assigned issue {issue_id} to user {assigned_to_user_id}")
        else:
            print(f"-> No issue or user found. No assignment made.")
    except Error as e:
        print(f"The error '{e}' occurred. Check if issue ID and user ID are valid.")
    finally:
        cursor.close()

def add_comment_to_issue(connection, issue_id, user_id, body):
    cursor = connection.cursor()
    query = "INSERT INTO Comments (issue_id, user_id, body) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (issue_id, user_id, body))
        connection.commit()
        comment_id = cursor.lastrowid
        print(f"Comment {comment_id} added to issue {issue_id}.")
        return comment_id
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()


#-- DELETE --#
def delete_user(connection):
    cursor = connection.cursor()
    email = input('Enter User email to delete: ')
    c = input(f'Are you sure you want to delete user {email}? (Y)es or (N)o: ')
    
    if c.lower().startswith('y'):
        query = "DELETE FROM Users WHERE email = %s"
        try:
            cursor.execute(query, (email,)) 
            connection.commit()
            if cursor.rowcount > 0:
                print(f"User with email '{email}' deleted successfully.")
            else:
                print(f"No user found with email '{email}'.")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()
    else:
        print("Delete operation cancelled.")
        cursor.close()


def delete_project(connection):
    cursor = connection.cursor()
    project_id_str = input('Enter Project ID to delete: ')
    
    try:
        project_id = int(project_id_str)
    except ValueError:
        print("Invalid Project ID. Must be a number.")
        cursor.close()
        return

    c = input(f'Are you sure you want to delete project {project_id}? (Y)es or (N)o: ')
    if c.lower().startswith('y'):
        query = "DELETE FROM Projects WHERE project_id = %s"
        try:
            cursor.execute(query, (project_id,))
            connection.commit()
            if cursor.rowcount > 0:
                print(f"Project {project_id} deleted successfully.")
            else:
                print(f"No project found with ID {project_id}.")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()
    else:
        print("Delete operation cancelled.")
        cursor.close()


def delete_issue(connection):
    cursor = connection.cursor()
    issue_id_str = input('Enter Issue ID to delete: ')

    try:
        issue_id = int(issue_id_str)
    except ValueError:
        print("Invalid Issue ID. Must be a number.")
        cursor.close()
        return

    c = input(f'Are you sure you want to delete issue {issue_id}? (Y)es or (N)o: ')
    if c.lower().startswith('y'):
        query = "DELETE FROM Issues WHERE issue_id = %s"
        try:
            cursor.execute(query, (issue_id,))
            connection.commit()
            if cursor.rowcount > 0:
                print(f"Issue {issue_id} deleted successfully.")
            else:
                print(f"No issue found with ID {issue_id}.")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()
    else:
        print("Delete operation cancelled.")
        cursor.close()


def delete_comment(connection):
    cursor = connection.cursor()
    comment_id_str = input('Enter Comment ID to delete: ')
    
    try:
        comment_id = int(comment_id_str)
    except ValueError:
        print("Invalid Comment ID. Must be a number.")
        cursor.close()
        return

    c = input(f'Are you sure you want to delete comment {comment_id}? (Y)es or (N)o: ')
    if c.lower().startswith('y'):
        query = "DELETE FROM Comments WHERE comment_id = %s"
        try:
            cursor.execute(query, (comment_id,))
            connection.commit()
            if cursor.rowcount > 0:
                print(f"Comment {comment_id} deleted successfully.")
            else:
                print(f"No comment found with ID {comment_id}.")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()
    else:
        print("Delete operation cancelled.")
        cursor.close()


def main():
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASS = "@L3m0n0rang3"  
    DB_NAME = "bug_tracker_db"          

    cnx = create_db_connection(DB_HOST, DB_USER, DB_PASS, DB_NAME)

    try:
        print("\n--- Running Bug Tracker Demo ---")
        
        user_id_1 = add_new_user(cnx, "mithun_dev", "mithun@example.com")
        user_id_2 = add_new_user(cnx, "Landa_manager", "oc.landa@example.com")
        
        if not (user_id_1 and user_id_2):
            raise Exception("Failed to create initial users. Halting demo.")

        project_id_1 = add_new_project(cnx, "E-commerce Website", "The main company online store.")
        
        if not project_id_1:
            raise Exception("Failed to create project. Halting demo.")

        issue_id_1 = report_new_issue(
            cnx, project_id_1, user_id_1, 
            "Login button not working", 
            "The login button on the homepage does nothing when clicked.",
            "High"
        )
        
        if not issue_id_1:
             raise Exception("Failed to report issue. Halting demo.")

        assign_issue(cnx, issue_id_1, user_id_1) 

        update_issue_status(cnx, issue_id_1, "In Progress")

        add_comment_to_issue(cnx, issue_id_1, user_id_2, "Alice, please look into this ASAP.")
        add_comment_to_issue(cnx, issue_id_1, user_id_1, "On it. Starting work now.")

        print("\n--- Testing invalid status ---")
        update_issue_status(cnx, issue_id_1, "Finished") 

        print("\n--- Demo Complete ---")
        
    except Exception as e:
        print(f"An error occurred during the demo: {e}")
    finally:
        if cnx and cnx.is_connected():
            cnx.close()
            print("\nMySQL connection is closed.")

if __name__ == "__main__":
    main()
