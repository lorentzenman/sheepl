"""
Base class for CMD Blocks so that the core menu options functions are based.
Purely for inheritance

Pushes the common menu functionality such as back and discard into this class

    # TODO - sort out the issue of not repeating the last commmand on enter in CMD
"""


__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd

try:
    import readline
except:
    print("[>] Cannot import readline")


# Sheepl Modules
from utils.tasks import Tasks
from utils.counter import Counter


#######################################################################
#  Base AutoIT Block Definition
#######################################################################

class BaseCMD(cmd.Cmd):

    """
    # Uniform CMD Constructor Arguments
    : cl            > colour object
    : csh           > current Sheepl object
    : completed     > tracking boolean
    : discard       > tracking boolean
    : taskstarted   > tracking boolean
    : baseprompt    > current task CMD prompt
    : prompt        > extends baseprompt as needed
    : taskname      > current taskname
    """

    def __init__(self, csh, cl):
        cmd.Cmd.__init__(self)

        self.cl = cl
        self.csh = csh
        self.completed = True
        self.discard = False
        self.taskstarted = False
        self.baseprompt = ''
        self.prompt = ''
        self.taskname = ''
        self.subtask_supported = False
        


    def do_back(self, arg):
        """
        Return to main menu
        """
        if self.completed == False:
            print(self.cl.red("[!] <ERROR> Still creating task : ") + self.taskname)
            print("[!] Run 'discard' to reset\n")

        else:
            print(self.cl.red('[>] Returning to the main menu'))
            return -1


    def emptyline(self):
        pass


    def do_killwindow(self, window_title):
        """
        Adds the Window title to the 'Kill Windows list'
        """
        if window_title:
            print("[!] Adding {} to the Kill Window Title list".format(window_title))
            self.csh.window_kill_list.append(window_title)


    def do_discard(self, arg):
        """
        Gets called based on a discard option
        """
        # sets the switch to allow the menu to exit
        self.discard        = True
        self.completed      = True
        self.taskstarted    = False
        self.csh.creating_subtasks = False
        print('[>] Discarding : ' + self.cl.red("{}".format(self.taskname)))
        self.prompt = self.baseprompt
        # if subtask already has a commands list applied
        # it gets reset

        try:
            if self.commands:
                self.commands = []
        except:
            pass


    def check_task_started(self):
        """
        Check to see if we are in a current task
        based on boolean
        """
        if self.taskstarted == True:
            print(self.cl.red("[!] <ERROR> Already creating a task. Run 'discard' to reset"))
            # OCD space
            print()
        else:
            # tracking booleans
            self.taskstarted    = True
            self.completed      = False
            # return that the task has not yet started
            # if self.check_task_started == False:
            #   do stuff
            return False


    def complete_task(self):
        """
        Closes out the tast with the following actions:
            > increments the counter
            > resets the prompt back
            > sets the completed value to True
            > sets the taskstarted value to False
        """

        # increment the counter in the Sheepl Object ready for the next task
        # fix for multiple completion commands
        if self.taskstarted:
            print(self.cl.green("[>] Completing this task interaction"))
            # reset the prompt back
            self.prompt = self.baseprompt
            # Flick completed Switch
            self.completed      = True
            self.taskstarted    = False
            self.csh.creating_subtasks = False
        else:
            print("{} There is no current task to complete.".format(self.cl.red("[!]")))
            print("{} Issue the 'new' command to create new interaction.".format(self.cl.red("[!]")))



    def ask_yes_no_question(self, question):
            """
            Small helper function to take in a question and check the response
            is either yes or no
            Returns True if 'yes'
            """
            while 1:
                input_answer = input(question)
                if input_answer.lower() == "yes" or input_answer.lower() == "no":
                    break

            if input_answer.lower() == "yes":
                return True
            else:
                return False


    def active_task(self, active_task):
        """
        Helper to check whether task has started or not
        Encapsulates repetitive if/else CMD statements
        """

        pass


    # --------------------------------------------------->
    #   SubTask CMD Functions
    # --------------------------------------------------->

    def do_subtask_list(self, arg=None):
        """ List out the subtasks assigned to the current RDP task """
        # this was always crashing, and the reason is that the 
        # cmd module needs the second argument. So adding this as None
        # just runs the code below.
        print("[*] Assigned the following subtasks to this RDP session")
        for task in self.csh.subtasks.keys():
            print(f"[-] {task}")
  


    def do_subtask(self, st):
            """
            Checks to see if subtasks are supported in
            the module ie RDP etc
            """
            if self.subtask_supported == False:
                print(self.cl.red("[!] SubTasks are not supported in the this module"))

            else:

                # List the available Tasks to assign to a Sheepl
                print(self.cl.green("\n[!] Sheepl can create the following sub tasks inside the RDP session: \n"))
                #self.tasks.display_available_tasks(self.locate_available_tasks().values())
                for task in self.csh.task_list.values():
                    print("[*] {}".format(task))
                # OCD line break
                print()
                print(self.cl.green("\n[!] Assign with 'subtask' <TaskName> \n"))


            for task in self.csh.task_list.values():
                if st == task:
                    print(self.cl.blue("[>] Creating SubTask Assignment >> {}".format(st)))
                    self.csh.creating_subtasks = True
                    # add the subtask to the tracking
                    # need to empty tracking list each time a new RDP session task is 
                    # assigned as well
                    
                    self.csh.generate_task(task)



class SubTaskCMD(BaseCMD):
    """
    Inherits core menu functions from base console
    """

    def __init__(self, csh, cl):
        super(SubTaskCMD, self).__init__(csh, cl)
        self.subtask_prompt()
        self.subtask_counter = Counter()


    def subtask_prompt(self):
        """
        Updates the prompt to reflect subtask
        """
        print(self.subtask_counter.current())
        self.prompt = self.prompt[:-1] + " subtask :>"


    def do_subtasks_complete(self):
        """
        Adds in menu option for subtasking
        """

        print("this is a subtask")
