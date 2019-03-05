"""
 This creates a Sheepl based on reading a JSON file
 need to print an example of a profile structure
"""


__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import json
import importlib

from utils.base.base_sheepl_class import Sheepl


class Profile(object):
    """
    Creates a profile object for use with the sheepl object
    takes in colour object
    """

    def __init__(self, cl, profile_file, tasks):
        self.cl = cl
        self.tasks = tasks
        # now parse the profile_file
        self.interactive = False

        self.verbose = True

        # emptys for module strings
        self.module_import_path = ''
        self.module = ''

        # return the parsed JSON profile
        self.profile = self.parse_profile_file(profile_file)

        # create the filename
        self.file_name = self.profile["name"].replace(' ', '_')
        self.file_name = self.profile["name"].lower() + '.au3'

        # self.csh = Sheepl(name, total_time, typing_speed, loop, self.cl) 
        self.csh = Sheepl(self.profile["name"],     
                            self.profile["total_time"],
                            self.profile["typing_speed"], 
                            self.profile["loop"], 
                            cl,
                            self.interactive)

        # create a list for base_class_names
        self.base_class_names = []
        #self.class_path, self.class_name = self.tasks.locate_available_tasks().items()
        #print(self.base_class_names)
        self.create_sheepl_tasks(self.csh, self.profile)



        #print(self.assign_tasks(self.profile["tasks"]))

        # now grab tasks within the JSON profile
        #self.create_sheepl_tasks(self.csh, self.profile)

        #self.csh.write_file(self.file_name)


    def parse_profile_file(self, profile_file):
        """
        Parses JSON profile file
        """
        with open(profile_file) as json_file:
            profile = json.load(json_file)

            return profile["sheepl"]


    def assign_tasks(self, tasks):
        """
        Takes Sheepl dictionary from JSON 
        and parses to find the available tasks
        Checks to see if the task suports subtasking and then 
        passes the task to a process function that parses
        the individual task list and assigns
        """
        for task in tasks:

            # ocd print line
            print()
            task_name = task["task"]
    
            self.process_task(task)
        

    def process_subtask(self, subtask_output):
        """
        Need to take the subtask dictionary and call tasks on this
        that get appended to the subtasks dict

        The following are needed to create a task.
        You create a task object
        then you call the static method on this 
        task
        What gets passed in here is a list of dictionaries
        these need to get parsed 
        """ 

        self.csh.creating_subtasks = True

        for output in subtask_output:
            # check to see if there is a list - ie
            # this will be the supplied arguments
            # output passed in is a dictionary
            # dirty testing by creating another dictionary
            subtask_arguments = {}
            for k, v in output.items():
                if k == "task":
                    subtask_name = v
                    print("The Subtask name is : " + subtask_name)
                    sheepl_task = self.csh.generate_task(subtask_name)
                    #print(sheepl_task)
                else:
                    subtask_arguments[k] = v

            #print("subtask args.....")
            #print(subtask_arguments)



            # dictionary comprehension
            sheepl_task.create_autoIT_block(self.csh, **subtask_arguments)

           # print(self.csh.subtasks.items())
           

    def process_task(self, task):
        """
        Processes each individual task
        Checks to see whether subtasking is enabled or not
        and then assigns the task output
        """

        print(self.cl.yellow("[>] Processing : {} Task".format(task["task"])))
        # Task Name
        
        # creates the task objects
        current_task = self.csh.generate_task(task["task"])
        # shows the current counter
        print("[+] The counter is : " + str(self.csh.counter.current()))


        # as the task is a dictonary parse the task requirements
        if self.verbose:
            print("[!] {}".format(self.cl.blue("Task requirements")))
            for key, value in task.items():
                # serious format foo to just grab commands if not part


                # check to see if subtasking is enabled
                if key == "subtasks":
                    # increment counter
                    # set global counter for creating a subtask

                    print(" : [>] {}".format(self.cl.red("Subtask Assignment")))
                    self.process_subtask(value)
                  # this requests the sheepl object to generate a task
                    # the add_task method of the Sheepl task takes the
                    # task name as the key and then the output as a list
                    
                    # calls the static method
                    #current_task.create_autoIT_block(self.csh, **{subtask_name : s})
                    # call the Sheepl add_task method
                    # it takes the kwargs option
                        #self.csh.add_task(task)
        
                # of a subtask as this is below                
                elif value != task["task"]:
                
                    # check to see if this value is list
                    # if it is, then we have a sequence of commands
                    if type(value) == list:
                        print(" : [>] {}".format(self.cl.red(">: commands")))
                        for c in value:
                            print(" : [*] {} {}".format(self.cl.blue("[cmd]"), c))
                    else:
                        print(" : [*] The Key is : {} , with a value of {}".format(key, value))                
                    current_task.create_autoIT_block(self.csh, **task)
            #
    

    def create_sheepl_tasks(self, csh, profile):
        """
        Creates Tasks and compares to availabel
        """

        for task in profile["tasks"]:
            #print(task)
            task_name = task["task"]
            #print(task_class_name)
            # temp dictionary
            task_arguments = {}
            #print(task_class_name)
            for key, value in task.items():
                if value == task_name:
                    print(self.cl.green("[*] Creating Sheepl Task : {}".format(task_name)))
                    #print("The Task Name is : {}".format(task_name))
                # check to see if subtasks are defined
                if key == 'subtasks':
                    self.process_subtask(value)

                else:
                    task_arguments.update({ key : value })
                
            print("The Final Task Arguments \n" + str(task_arguments))
            print("-------------------------------------\n")

            """
            Now we use importlub to import the module path and 
            create an instance of the task
            """

            # now reset the subtask switch as all these
            # subtasks have already been appended to the Sheepl object
            self.csh.creating_subtasks = False

            for path, module in self.tasks.locate_available_tasks().items():
                if task_name == module:
                    task_module = importlib.import_module(path)
                    #print(task_module)
                    sheepl_task = getattr(task_module, module)
                    
                    sheepl_task.create_autoIT_block(self.csh, **task_arguments)
                    # increment the counter
                    self.csh.counter.increment()

                    #print("the assigned tasks")
                    #print(csh.tasks)
  
        """
        After tasking has been parsed, this is the call to write the file
        """
        print("[!] Writing the file {} :".format(self.cl.green(self.csh.file_name)))
        self.csh.write_file(self.csh.file_name)
        print("[!] Written the file {} :".format(self.cl.green(self.csh.file_name)))

