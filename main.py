import mysql.connector
from mysql.connector import Error
import sys
from datetime import datetime

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

def view_all_projects(connection):
    """Fetches and prints all projects."""
    cursor = connection.cursor()
    query = "SELECT project_id, name, description FROM Projects"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        if not results:
            print("No projects found.")
            return

        print("\n--- All Projects ---")
        for (project_id, name, description) in results:
            print(f"[{project_id}] {name} - {description[:50]}...")
        print("--------------------\n")
            
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

def view_issues_for_project(connection):
    """Fetches and prints all issues for a specific project."""
    view_all_projects(connection) # Show projects first
    try:
        project_id = int(input("Enter Project ID to see its issues: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    cursor = connection.cursor()
    # Query with a JOIN to get user names
    query = """
    SELECT 
        i.issue_id, i.title, i.status, i.priority, 
        u_reporter.username AS reporter,
        u_assignee.username AS assignee
    FROM Issues AS i
    LEFT JOIN Users AS u_reporter ON i.reported_by_user_id = u_reporter.user_id
    LEFT JOIN Users AS u_assignee ON i.assigned_to_user_id = u_assignee.user_id
    WHERE i.project_id = %s
    """
    try:
        cursor.execute(query, (project_id,))
        results = cursor.fetchall()
        
        if not results:
            print(f"No issues found for project ID {project_id}.")
            return

        print(f"\n--- Issues for Project {project_id} ---")
        for (issue_id, title, status, priority, reporter, assignee) in results:
            reporter = reporter or "N/A"
            assignee = assignee or "Unassigned"
            print(f"  [{issue_id}] {title} ({status}, {priority})")
            print(f"      Reported by: {reporter}, Assigned to: {assignee}")
        print("--------------------------\n")

    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

def view_all_users(connection):
    """Fetches and prints all users."""
    cursor = connection.cursor()
    query = "SELECT user_id, username, email FROM Users"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        if not results:
            print("No users found.")
            return

        print("\n--- All Users ---")
        for (user_id, username, email) in results:
            print(f"[{user_id}] {username} ({email})")
        print("-------------------\n")
            
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

#-- INSERT --#
def add_new_user(connection):
    """CLI wrapper to add a new user."""
    username = input("Enter new username: ")
    email = input("Enter new user's email: ")
    
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

def add_new_project(connection):
    """CLI wrapper to add a new project."""
    name = input("Enter new project name: ")
    description = input("Enter project description: ")

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

def report_new_issue(connection):
    view_all_projects(connection)
    view_all_users(connection)
    
    try:
        project_id = int(input("Enter Project ID for this issue: "))
        reported_by_user_id = int(input("Enter your User ID (reporter): "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    title = input("Enter issue title: ")
    description = input("Enter full issue description: ")
    priority = input("Enter priority (Low, Medium, High, Critical): ")

    cursor = connection.cursor()
    query = """
    INSERT INTO Issues 
    (project_id, reported_by_user_id, title, description, priority, updated_at) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (project_id, reported_by_user_id, title, description, priority, datetime.now()))
        connection.commit()
        issue_id = cursor.lastrowid
        print(f"New issue '{title}' reported successfully with ID: {issue_id}.")
        return issue_id 
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()

def add_comment_to_issue(connection):
    """CLI wrapper to add a comment."""
    try:
        issue_id = int(input("Enter Issue ID to comment on: "))
        user_id = int(input("Enter your User ID: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    body = input("Enter your comment: ")

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

#-- UPDATE --#
def update_issue_status(connection):
    """CLI wrapper to update an issue's status."""
    try:
        issue_id = int(input("Enter Issue ID to update: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return
        
    status = input("Enter new status (Open, In Progress, Testing, Closed): ")
    
    valid_statuses = ('Open', 'In Progress', 'Testing', 'Closed')
    if status not in valid_statuses:
        print(f"Invalid status: {status}. Must be one of: {valid_statuses}")
        return
         
    cursor = connection.cursor()
    query = "UPDATE Issues SET status = %s, updated_at = %s WHERE issue_id = %s"
    try:
        cursor.execute(query, (status, datetime.now(), issue_id))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"-> Updated issue {issue_id} status to '{status}'")
        else:
            print(f"-> No issue found with ID {issue_id}. No updates made.")
    except Error as e:
        print(f"The error '{e}' occurred while updating issue status")
    finally:
        cursor.close()

def assign_issue(connection):
    """CLI wrapper to assign an issue to a user."""
    view_all_users(connection)
    try:
        issue_id = int(input("Enter Issue ID to assign: "))
        assigned_to_user_id = int(input("Enter User ID to assign to: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    cursor = connection.cursor()
    query = "UPDATE Issues SET assigned_to_user_id = %s, updated_at = %s WHERE issue_id = %s"
    try:
        cursor.execute(query, (assigned_to_user_id, datetime.now(), issue_id))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"-> Assigned issue {issue_id} to user {assigned_to_user_id}")
        else:
            print(f"-> No issue or user found. No assignment made.")
    except Error as e:
        print(f"The error '{e}' occurred. Check if issue ID and user ID are valid.")
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
                print(f"Project {project_id} deleted successfully (and all its issues/comments).")
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
                print(f"Issue {issue_id} deleted successfully (and all its comments).")
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
        
def show_menu():
    """Prints the main menu options."""
    print("\n--- 🐞 Bug Tracker Main Menu ---")
    print("--- View Data ---")
    print("  1. View all projects")
    print("  2. View issues for a project")
    print("  3. View all users")
    print("--- Add Data ---")
    print("  4. Add new project")
    print("  5. Report new issue")
    print("  6. Add new user")
    print("  7. Add comment to issue")
    print("--- Update Data ---")
    print("  8. Update issue status")
    print("  9. Assign issue to user")
    print("--- Delete Data ---")
    print("  10. Delete project (WARNING: Deletes all its issues!)")
    print("  11. Delete issue (WARNING: Deletes all its comments!)")
    print("  12. Delete comment")
    print("  13. Delete user")
    print("  q. Quit")
    print("---------------------------------")
    return input("Enter your choice: ")

def main():
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASS = "@L3m0n0rang3" 
    DB_NAME = "bug_tracker_db"     
    
    cnx = create_db_connection(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    
    if not cnx:
        return # Connection failed, exit
        
    while True:
        choice = show_menu()
        
        if choice == '1':
            view_all_projects(cnx)
        elif choice == '2':
            view_issues_for_project(cnx)
        elif choice == '3':
            view_all_users(cnx)
        elif choice == '4':
            add_new_project(cnx)
        elif choice == '5':
            report_new_issue(cnx)
        elif choice == '6':
            add_new_user(cnx)
        elif choice == '7':
            add_comment_to_issue(cnx)
        elif choice == '8':
            update_issue_status(cnx)
        elif choice == '9':
            assign_issue(cnx)
        elif choice == '10':
            delete_project(cnx)
        elif choice == '11':
            delete_issue(cnx)
        elif choice == '12':
            delete_comment(cnx)
        elif choice == '13':
            delete_user(cnx)
        elif choice.lower() == 'q':
            print("Exiting Bug Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1-13 or 'q'.")

    if cnx and cnx.is_connected():
        cnx.close()
        print("\nMySQL connection is closed.")

if __name__ == "__main__":
    main()
