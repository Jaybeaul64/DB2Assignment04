import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
# Establish a connection to the MySQL DB.
def connect_db():
    """
    Creates a database connection using credentials from the .env file.

    :return: The database connection.
    """
    try:
        connection = mysql.connector.connect(
            host= os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            passwd=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB')
        )
        connection.autocommit = False
        return connection
    except mysql.connector.Error as error:
        print(f"database connection failed: {error}")
        return None
    
# gets all the tasks from the database.
def get_all_tasks():
    """
    Fetches all the tasks from the database.

    :return: All the tasks from the task database.
    """
    connection = connect_db()
    if not connection:
        return[]
    
    cursor = connection.cursor()
    sql_query = f"SELECT id, description FROM Tasks"
    cursor.execute(sql_query)
    results = cursor.fetchall()
    cursor.close()
    return results

def delete_task(task_id):
    """
    removes a task matching the provided ID from the database and logs the change in the Task_audit table.

    :param task_id: the ID of the task to be deleted.
    :type task_id: int

    :raises Exception: if the database transaction fails for any reason.
    """
    audit_query=f"""
    INSERT INTO Task_audit (task_id, description, user_action, user)
    VALUES (%s, %s, %s, CURRENT_USER())
    """

    connection = connect_db()
    try:
        cursor = connection.cursor()
        sql_query = f"SELECT description FROM Tasks WHERE id={task_id}"
        cursor.execute(sql_query)
        result = cursor.fetchone()
        sql_query = f"DELETE FROM Tasks WHERE id={task_id};"
        cursor.execute(sql_query)
        cursor.execute(audit_query, (task_id, result[0], 'DELETE'))
        connection.commit()
        cursor.close()
    except Exception as error:
        print(error)
        connection.rollback()

def insert_task(task=""):
    """
    Creates a task in Tasks table, log the change in the Task_audit table and returns the new tasks's id.

    :param task: The task description to insert into the database.
    :type task: str

    :return: the new row's id

    :raises Exception: if the database transaction fails for any reason.
    """

    audit_query=f"""
    INSERT INTO Task_audit (task_id, description, user_action, user)
    VALUES (%s, %s, %s, CURRENT_USER())
    """
    sql_query1 = f"""
    INSERT INTO Tasks (description)
    VALUES (%s);
    """
    sql_query2 = """
    SELECT LAST_INSERT_ID();
    """
    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute(sql_query1, (task,))
        cursor.execute(sql_query2)
        result = cursor.fetchall()[0][0]
        cursor.execute(audit_query, (result, task, 'INSERT'))
        connection.commit()
        cursor.close()
        return result
    except Exception as error:
        print(error)
        connection.rollback()

def edit_task(id, update):
    """
    Updates a task in the Tasks table and logs the change in the Task_audit table.

    :param update: the new task description
    :type update: str

    :raises Exception: if the database transaction fails for any reason.
    """
    audit_query=f"""
    INSERT INTO Task_audit (task_id, description, old_description, user_action, user)
    VALUES (%s, %s, %s, %s, CURRENT_USER())
    """
    sql_query = f"""
    UPDATE Tasks
    SET description=%s
    WHERE id=%s
    """
    try:
        connection = connect_db()
        cursor = connection.cursor()
        getter_query = f"SELECT description FROM Tasks WHERE id={id}"
        cursor.execute(getter_query)
        result = cursor.fetchone()
        cursor.execute(sql_query, (update, id))
        cursor.execute(audit_query, (id, update, result[0], 'UPDATE'))
        connection.commit()
    except Exception as error:
        print(error)
        connection.rollback()
        
        