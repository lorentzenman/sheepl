"""
 Creates a Task object than go through, identify all the current tasks
 available and then return this as an object with methods to list
 them and create the
 Has to be it's own class so that it can be used in the interactive console
 or through the JSON profiles import
"""


__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


#import glob
import os
import sys
import pathlib
import importlib



class Tasks(object):

    """
    This is the task object. It uses pathlib to parse the class files
    that are defined for tasks
    """
    class_start = ''

    def __init__(self):
        
        self.tasks_root = pathlib.Path.cwd() / 'tasks'
        self.task_list = self.locate_available_tasks()
    

    def list_categories(self):
        """
        Uses the pathlib module to get the name of the categories
        """
        print("[!] Avaliable Categories")
        for category in self.tasks_root.iterdir():
            print("* " + category.name)


    def locate_available_tasks(self):
        """
        Goes through the actions parent directory
        and finds files and Class definitions
        for dynamic import and returns a dictionary of module path and name
        Uses the pathlib modules from 3.4 onwards
        Much cleaner than having to split paths and can create a 
        string on just the parts required
        """

        tasks = {}
       
        for category in self.tasks_root.iterdir():
            for task in category.glob('*.py'): 
                module_import_path = 'tasks.' + category.name + '.' + task.stem
                tasks[module_import_path] = task.stem 

        return tasks


    def create_task(self, module_import_path, module, interactive, id):
        """
        Creates a task an imports the path to the module
        """
        try:
            task_module = importlib.import_module(module_import_path)
            self.class_start = getattr(task_module, module)

        except:
            print("Error importing module")

        return self.class_start


    def display_available_tasks(self, task_list):
        """
        Takes the available tasks based on the module import list
        """
        for task in task_list:
            print("[*] {}".format(task))
