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
