from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.factory import Factory
from typing import Optional, Callable
import pandas as pd
import Logic
import os

# Load KVs
root_dir = os.path.dirname(os.path.abspath(__file__))
kv_dir = os.path.join(os.path.join(root_dir, "kvs"))
Builder.load_file(os.path.join(kv_dir, 'UI.kv'))
Builder.load_file(os.path.join(kv_dir, 'editMenu.kv'))
Builder.load_file(os.path.join(kv_dir, 'message.kv'))

class TaskManagerUI(BoxLayout):
    """
    A class for managing and displaying tasks in the UI. This includes adding,
    removing, and editing tasks in the database and updating the display.

    :param BoxLayout: Inherits from Kivy's BoxLayout for layout management.
    :type BoxLayout: kivy.uix.boxlayout.BoxLayout
    """

    def on_kv_post(self, base_widget):
        """
        Get the data from the database and loop through it all to create the task widgets.
        """
        self.data = Logic.get_tasks_df()
        self.stack = self.ids.task_stack
        for index, row in self.data.iterrows():
            self.add_task_widget(index)

    def add_task_widget(self, index: int) -> None:
        """
        Creates a BoxLayout widget containing an "Edit" button and a task description label based on a row in the data DataFrame.
        The widget is added to the task stack in the UI.

        :param index: The DataFrame's row index to create a widget from. Must be an integer.
        :type index: int
        """
        box = BoxLayout(orientation='horizontal', size_hint=(1, None))
        label = Label(text=str(self.data.loc[index]["Task"]), size_hint=(0.85, None), height=40, valign='center', halign='center')
        button = Button(text='Edit', size_hint=(0.15, None))

        button.bind(on_release=lambda x, box=box: self.edit_menu(box))

        box.add_widget(button)
        box.add_widget(label)
        self.stack.add_widget(box)

        self.data.loc[(index), ['Widget']] = box

    def get_index(self, task: BoxLayout) -> int:
        """
        gets the index in the data dataframe from a widget instance.

        :param task: The widget instance to get the index of.
        :type task: kivy.uix.boxlayout.BoxLayout

        :return: The index of the provided widget instance
        """
        return self.data.loc[self.data['Widget'] == task].index[0]


    def add_task(self) -> None:
        """
        Adds a new task from the input field to the UI and database.
        """
        inputText = self.ids.description_TextInput.text
        try:
            self.ids.description_TextInput.text = "" # clear the text input
            id = Logic.create_task(inputText) # inserts into the database and get ID
            row = pd.DataFrame({'ID': [id], 'Task': [inputText]}) # creates new dataframe to concat into existing one
            self.data = pd.concat([self.data, row], axis=0, ignore_index=True) # concat new row into the dataframe
            self.add_task_widget(self.data.loc[self.data['ID'] == id].index[0]) # create widget on the screen
        except Exception as error:
            self.confirm_popup(str(error), "Error", None, True, False)

    def remove_task(self, widget: BoxLayout) -> None:
        """
        Removes a Task from the database, then the UI and finally the dataframe from a widget instance.

        :param widget: The task widget to delete.
        :type widget: kivy.uix.boxlayout.BoxLayout
        """
        try:
            task = self.data.loc[self.data['Widget'] == widget] # Get the row's information form the DF
            id = int(task['ID']) # Get the ID from the dataframe
            Logic.drop_task(id) # remove item from the database.
            self.stack.remove_widget(widget) # remove item from the UI
            self.data = self.data.drop(task.index[0]) # remove item from the list
        except Exception as error:
            self.confirm_popup(str(error), "Error", None, True, False)

    # sometimes I use index, sometimes the instance... I know, consistency, but it's getting late and this must be done by midnight (not happening)
    def edit_task(self, index: int, input: TextInput) -> None:
        """
        Calls the appropriate methods to edit the task in the database, and if successful, will modify the value from the front end also.

        :param index (int): the index of the task in the dataframe.
        :type index: int

        :param input: the TextInput to get the text from.
        :type input: class:`TextInput`
        """
        row = self.data.iloc[index]
        try:
            Logic.modify_task(int(row['ID']), input.text) # modify in the database
            self.data.loc[index, 'Task'] = input.text # modify in the df
            row.loc['Widget'].children[0].text = input.text # modify in the UI
        except Exception as error:
            self.confirm_popup(str(error), "Error", None, True, False)

    def edit_menu(self, box: BoxLayout) -> None:
        """
            Opens the Edit Menu Popup. Contains an InputField widget containing the value, a cancel button, a save button and a delete button.
            The Cancel button dissmisses the popup and doesn't save any change.
            The Save button will open a confirmation popup. If the confirmation is successful, it will save all changes.
            The delete button will open a confirmation popup. If the confirmation is successfulm it will delete the task.

            :param box: The task's boxlayout
            :type box: kivy.uix.boxlayout.BoxLayout
        """
        popup = Factory.EditMenu() # gets the popup kivy string
        popup.open() # opens the edit popup
        delete_button = popup.ids.delete_button # Find the delete button
        save_button = popup.ids.save_button # find the save button
        input_field = popup.ids.TaskInput # Finds the TextInput
        index = self.get_index(box) # get the input from the df
        input_field.text = str(self.data.loc[index]['Task'])

        # binds the buttons to open a confirmation pop up.
        delete_button.bind(on_release=lambda _:(self.confirm_popup("Are you sure you want to delete this task?", "Warning", (lambda _:(self.remove_task(box))))))
        save_button.bind(on_release=lambda _:(self.confirm_popup("Are you sure you want to delete this task?", "Warning", (lambda _:(self.edit_task(index, input_field))))))

    def confirm_popup(self, message, title, method: Optional[Callable[[], None]], confirm=True, cancel=True) -> None:
        """
        Displays a popup message to the user.
        The message has a title, a label and two optional buttons.
        The confirm button will call a method when press if present. If no method is specified, it will simply act as a dismiss button.
        The Cancel button is just a dismiss button that will close the popup.
        The title should be as short as possible, ideally just one word such as "warning" or "confirmation". It should reflect the nature of the message itself.
        The Label contains the message itself, with details if necessary.

        :param message: The message to be displayed in the popup.
        :type message: str

        :param title: The popup title.
        :type title: str

        :param method: the function to be executed when the confurm button is pressed.
        :type method: Optional[Callable[[], None]]

        :param confirm: wether to display the confirm button or not.
        :type confirm: bool
        :default confirm: True

        :param cancel: wether to display the cancel button or not.
        :type cancel: bool
        :default cancel: True
        """
        popup = Factory.MessagePopup() # gets the popup kivyu string
        popup.open() # opens the edit popup
        popup.title = title # changes the title
        popup.ids.message_label.text = message # changes the message
        if not confirm:
            popup.remove_widget(popup.ids.confirm_button) # delete the confirm button if not needed
        elif method is not None:
            popup.ids.confirm_button.bind(on_release=method) # Bind the confirm button to the method
        if not cancel:
            popup.ids.cancel_button.parent.remove_widget(popup.ids.cancel_button) # Delete the confirm


class TaskManagerApp(App):
    """
        Builds the fronted of the Kivy Application.
    """
    def build(self):
        return TaskManagerUI()
if __name__ == "__main__":
    TaskManagerApp().run()