import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import Logic
import pytest
import pandas as pd
from unittest.mock import patch
import re

def test_verify():
    """
    Tests that the verify method throws the appropriate errors when a string doesn't meet requirements
    """
    with pytest.raises(ValueError, match=re.escape("Text must not contain any of these characters: " + Logic.forbiden_chars)):
        Logic.verify("Th/s /s an /llegal str/ng")

    with pytest.raises(ValueError, match="Text must not be empty."):
        Logic.verify("")

    with pytest.raises(ValueError, match="Text must be at least 3 characters long"):
        Logic.verify("12")

    try:
        Logic.verify("Valid Task")
    except ValueError:
        pytest.fail("verify() raised ValueError unexpectedly!")

def test_get_tasks_df():
    """
    Tests that data fetched from the database gets processed properly by the get_tasks_df() method.
    """
    mock_data = [(1, "Task 1"), (2, "Task 2"), (3, "Task 3")]
    
    with patch('Logic.get_all_tasks', return_value=mock_data):
        df = Logic.get_tasks_df()
        
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ['ID', 'Task']
        assert df.shape == (3, 2)
        assert df['Task'][0] == "Task 1"

def test_drop_task_invalid_id():
    """
    Tests that the drop_task() method raises an error when feeding it an id of the wrong datatype.
    """
    with pytest.raises(TypeError):
        Logic.drop_task("string_id")

def test_drop_task_valid_id():
    """
    Tests that the delete_task() method gets called properly without messing up the database.
    """
    with patch('Logic.delete_task') as mock_delete:
        Logic.drop_task(1)
        mock_delete.assert_called_once_with(1)

def test_create_task():
    """
    Tests that the create_task() method throws an error when an invalid id is entered.
    """
    with patch('Logic.insert_task') as mock_insert:
        Logic.create_task("New Task")
        mock_insert.assert_called_once_with("New Task")
    
    # I modified the Logic script sp that id "forbiden_chars" regex changes for some reason, it won't fuck up the tests.
    with pytest.raises(ValueError, match=re.escape("Text must not contain any of these characters: " + Logic.forbiden_chars)):
        Logic.create_task("Invalid/Task")


def test_modify_task_invalid_id():
    """
    Tests that an error gets raised when creating a task with the wrong id.
    """
    with pytest.raises(TypeError):
        Logic.modify_task("string_id", "Updated Task")

def test_modify_task_valid_id():
    """
    Tests that the method doesn't throw an error when a valid Id is provided.
    """
    with patch('Logic.edit_task') as mock_edit:
        Logic.modify_task(1, "Updated Task")
        mock_edit.assert_called_once_with(1, "Updated Task")