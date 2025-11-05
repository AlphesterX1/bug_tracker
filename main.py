import mysql.connector
from mysql.connector import Error

def create_db_connection(host_name, user_name, user_password, db_name):
    """Establishes a connection to the MySQL database."""
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
    return connection

# --- Database Credentials ---
# !! REPLACE with your root password set during installation
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "your_mysql_root_password" 
DB_NAME = "bug_tracker_db" # <-- Make sure you've created this database

# Create the main connection object
cnx = create_db_connection(DB_HOST, DB_USER, DB_PASS, DB_NAME)

def add_new_user(connection, username, email):
    """Adds a new user to the Users table."""
    cursor = connection.cursor()
    query = "INSERT INTO Users (username, email) VALUES (%s, %s)"
    try:
        cursor.execute(query, (username, email))
        connection.commit()  # <-- !! Must commit to save changes
        print(f"User '{username}' added successfully.")
        return cursor.lastrowid  # <-- Gets the ID of the new user
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()

def add_new_project(connection, name, description):
    """Adds a new project to the Projects table."""
    cursor = connection.cursor()
    query = "INSERT INTO Projects (name, description) VALUES (%s, %s)"
    try:
        cursor.execute(query, (name, description))
        connection.commit()
        print(f"Project '{name}' added successfully.")
        return cursor.lastrowid # <-- Gets the ID of the new project
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()

def report_new_issue(connection, project_id, reported_by_user_id, title, description, priority="Medium"):
    """Adds a new issue to the Issues table, linking it to a project and user."""
    cursor = connection.cursor()
    query = """
    INSERT INTO Issues 
    (project_id, reported_by_user_id, title, description, priority) 
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (project_id, reported_by_user_id, title, description, priority))
        connection.commit()
        print(f"New issue '{title}' reported successfully.")
        return cursor.lastrowid # <-- Gets the ID of the new issue
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()

def add_comment_to_issue(connection, issue_id, user_id, body):
    """Adds a new comment to the Comments table."""
    cursor = connection.cursor()
    query = "INSERT INTO Comments (issue_id, user_id, body) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (issue_id, user_id, body))
        connection.commit()
        print(f"Comment added to issue {issue_id}.")
        return cursor.lastrowid
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()


if cnx and cnx.is_connected():
    cnx.close()
    print("MySQL connection is closed.")