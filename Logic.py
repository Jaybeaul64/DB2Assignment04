import pandas as pd
from DB import get_all_tasks, delete_task, insert_task, edit_task
import re

forbiden_chars = r'[\/\\\\|;#<>*\n]'

def get_tasks_df():
    """
    gets all the tasks into a dataframe with properly named columns
    
    :return: a dataframe containing everything in the "Tasks" table.
    """
    df = pd.DataFrame(get_all_tasks())
    df.rename(columns={0: 'ID', 1: 'Task'}, inplace=True)
    return df

def drop_task(task_id):
    """
    deletes a task with corresponding ID.

    :param task_id: The id of the task to delete.
    :type task_id: int

    :raises TypeError: When the value provided for task_id is not an integer.
    """
    if not isinstance(task_id, int):
            raise TypeError('Value must be an Integer')
    delete_task(task_id)

def create_task(task_desc):
    """
    Inserts a task into the database.
    Will verify that the task is not empty first.

    :param task_desc: the task description to be inserted into the database.
    :type task_desc: str
    """
    verify(task_desc) # test the string. Will raise an exception if it's wrong.
    return insert_task(str(task_desc))
    
def modify_task(id, value):
    """
    modifies a task's description from the task's id.

    :param id: The tasks's id
    :type id: int

    :param value: The new task description.
    :type value: str

    :raises TypeError: when the value provided for the id is not an integer.
    """
    if not isinstance(id, int):
         raise TypeError('Value must be an Integer. Provided value: ' + str(id) + ', type: ' + str(type(id)))
    verify(value) # test the string. Will raise an exception if it's wrong.
    edit_task(id, value)

def verify(string):
     """
     ensures that the string is respecting standards.
     The string must not be empty.
     The string must be at least 3 characters long.
     The string must not contain any of these characters: / \ | ;

     :raises ValueError: When the text provided is empty.
     :raises ValueError: When the text provided is less than 3 characters.
     :raises ValueError: When the text provided contains one or more of the forbiden characters. 
     """

     if string == "":
          raise ValueError("Text must not be empty.")
     if len(string) < 3:
        raise ValueError("Text must be at least 3 characters long")
     if re.search(forbiden_chars, string):
          raise ValueError("Text must not contain any of these characters: " + forbiden_chars)