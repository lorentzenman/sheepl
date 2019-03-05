
# #######################################################################
#
#  Task : InternetExplorer Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 : Takes a supplied text file for the Sheepl to type
 : the master script will already define the typing speed as part of the master declarations

 ##############################################
        Add in Task Specific Notes Here
 ##############################################

 General Notes:
    The textwrap import is used to keep the AutoIT functions indented in code
    as this messes with the python code (back off OCD) when it's manually 
    appearing to hang outside of the class declarations and also stops code collapse in IDEs.
    So when creating code specific to the AutoIT functions just use tabs to indent insitu
    and the textwarp library will strip all leading tabs from the beginning of the AutoIT block.
    Also uses textwrap.indent() to add indentation to 'Send' commands in text_typing_block()

 Conventions:
    Use 'AutoIT' in code comments and class names and 'autoIT' when using as part of variable names

 Modes:
    Interactive Mode
        This uses the task module assign task requirements
        Add additional CMD functions using do_<argument>
        Once all the arguments are complete
        build the do_complete function out by passing the arguments
        as keywords to the staticmethod of the task object
        <TaskName>.create_autoIT_block(self.csh, 
                                        # add in other arguments
                                        # for object constructor
                                        # ---------------------> 
                                        parm1=self.parm1_value,
                                        parm2=self.parm3_value
                                        # ---------------------> 
                                        )
    Non-Interactive Profile
        This takes an input from the sheepl object
        and this creates a Profile() object. See profile.py

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"

import cmd
import sys
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD
#from utils.typing import TypeWriter


# #######################################################################
#  Task CMD Class Module Loaded into Main Sheepl Console
# #######################################################################


class TaskConsole(BaseCMD):

    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : complete_task()       > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(TaskConsole, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'InternetExplorer'

        # Overrides Base Class Prompt Setup 
        self.baseprompt = cl.yellow('{} >: internetexplorer :> '.format(csh.name.lower()))
        self.prompt = self.baseprompt

        # creating my own 
        self.introduction = """
        ----------------------------------
        [!] InternetExplorer Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: ######### > add in steps
        3: Complete the interaction using 'complete'
        """
        print(textwrap.dedent(self.introduction))

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        self.destination_url = ''


    # --------------------------------------------------->
    #   Task CMD Functions
    # --------------------------------------------------->

    def do_new(self, arg):
        """ 
        This command creates a new Word document
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        # Inverse check to see if task has already started
        # Booleans are set in parent method

        # method from parent class BaseCMD
        if self.check_task_started() == False:
            print("[!] Starting : 'InternetExplorer_{}'".format(str(self.csh.counter.current())))
            # OCD Line break
            print()
            self.prompt = self.cl.blue("[*] InternetExplorer_{}".format(str(self.csh.counter.current()))) + "\n" + self.baseprompt       


    # def do_cmd(self, command):
    #     """
    #     First checks to see if a new InternetExplorer Block has been started
    #     if so allows the command to be issued and then runs some checks
    #     or prompts to start a new interaction using 'new'
    #     Specify the command to run in the shell
    #     """
    #     # Uncomment
    #     """
    #     if command:
    #         if self.taskstarted == True:   
    #             self.commands.append(command)
    #         else:
    #             if self.taskstarted == False:
    #                 print(self.cl.red("[!] <ERROR> You need to start a new InternetExplorer Interaction."))
    #                 print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
    #             print("[!] <ERROR> You need to supply the command for typing")
    #     """
    #     pass


    def do_url(self, destination):
        """
        Grabs the destination URL
        """
        if destination:
            if self.taskstarted: 
                self.destination_url = destination
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new InternetExplorer Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """
        # setup create_internetexplorer for ease and clarity
        # pass in unique contructor arguments for AutoITBlock

        # Call the static method in the task object
        if self.taskstarted:
            InternetExplorer.create_autoIT_block(self.csh, 
                                    # add in other arguments
                                    # for object constructor
                                    # ---------------------> 
                                    url=self.destination_url
                                    # ---------------------> 
                                    )

        # now reset the tracking values and prompt
        self.complete_task()


    # --------------------------------------------------->
    #   CMD Util Functions
    # --------------------------------------------------->



# #######################################################################
#  InternetExplorer Class Definition
# #######################################################################


class InternetExplorer:

    def __init__(self, csh, cl, **kwargs):
        """
        Initial object setup
        """
        self.__dict__.update(kwargs)
        
        self.csh = csh
        self.subtask = False

        # Check if this task requires an AutoIT Specifc UDF
        # this gets declared here and then pushed into the master
        # if not then this can be deleted
        # Sheepl AutoIT include header list as part of the 'csh' object

        self.autoIT_include_statement = "#include <IE.au3>"

        # Check to make sure it's not already there, and if not add
        if not self.autoIT_include_statement in csh.autoIT_UDF_includes:
            csh.autoIT_UDF_includes.append(self.autoIT_include_statement)

        if csh.interactive == True:
            # create the task based sub console
            self.TaskConsole = TaskConsole(csh, cl)
            self.TaskConsole.cmdloop()            
   

    # --------------------------------------------------->
    #   End InternetExplorer Constructor
    # --------------------------------------------------->

    # --------------------------------------------------->
    #   InternetExplorer Static Method
    # --------------------------------------------------->

    """
    These are all the elements that get passed into the 
    @static method as keyword arguments
    Essentially, this is everything that needs to be passed
    to create the InternetExplorer object

    Parse the 'kwargs' dictionary for the arguments
    """

    @staticmethod
    def create_autoIT_block(csh, **kwargs):
        """
        Creates the AutoIT Script Block
        Note :
            Kwargs returns a dictionary
            do these values can be referenced
            by the keys directly
        """
     
        """
        This now creates an instance of the object with the correct
        counter tracker, and then appends as a task
        Note : add in additional constructor arguments as highlighted
               which get passed in from the 'kwargs' dictionary

        """

        csh.add_task('InternetExplorer_' + str(csh.counter.current()),
                                InternetExplorerAutoITBlock(
                                str(csh.counter.current()),
                                # add in other arguments
                                # for object constructor
                                # ---------------------> 
                                kwargs["url"]
                                # ---------------------> 
                                ).create()
                            )




# #######################################################################
#  InternetExplorer AutoIT Block Definition
# #######################################################################


class InternetExplorerAutoITBlock(object):
    """
    Creates an AutoIT Code Block based on the current counter
    then returns this to Task Console which pushes this upto the Sheepl Object
    with a call to create.
    String returns are pushed through (textwarp.dedent) to strip off indent tabs
    """

    def __init__(self, counter, destination_url):

        self.counter = counter
        self.indent_space = '    '
        self.destination_url = destination_url


    def func_dec(self):
        """
        Initial Entrypoint Definition for AutoIT function
        when using textwrap.dedent you need to add in the backslash
        to the start of the multiline
        """

        function_declaration = """
        ; < ------------------------------------------ >
        ;         InternetExplorer Interaction        
        ; < ------------------------------------------ >

        InternetExplorer_{}()
        """.format(str(self.counter))

        return textwrap.dedent(function_declaration)


    def open_internetexplorer(self):
        """
        Creates the AutoIT Function Declaration Entry
        """

        """
        # Note a weird bug that the enter needs to be 
        # passed as format string argument as escaping
        # is ignored on a multiline for some reason
        # if it gets sent as an individual line as in text_typing_block()
        # >> typing_text += "Send('exit{ENTER}')"
        # everything works. Strange, Invoke-OCD, and then stop caring
        # and push it through the format string.

        # Note > Send('yourprogram{ENTER}')
        # Example : Send('powershell{ENTER}')
        """

        _open_internetexplorer = """

        Func InternetExplorer_{}()

            ; Creates a InternetExplorer Interaction

            Local $oIE = _IECreate("{}",1,1,1)
            Sleep(2000)
            ;WinWaitActive("Windows Internet Explorer")
            ;SendKeepActive("Windows Internet Explorer")
            ;WinSetState("Windows Internet Explorer","",@SW_MAXIMIZE)
            ; hardcoded sleep for now
            ; will convert to AutoIT random
            ; this is also where the IE interaction such as logging in etc will happen,
            ; spawning new tabs etc
            ; prob need a call out function to trigger a subroutine
            Sleep(20000)
            Send("!{}")

        """.format(str(self.counter),
                    self.destination_url,
                    "{F4}"
                    )

        return textwrap.dedent(_open_internetexplorer)   


    # def text_typing_block(self):
    #     """
    #     Takes the Typing Text Input
    #     """

    #     typing_text = 'Send("")'
    #     # now loop round the input_text
    #     # represents how someone would use the enter key when typing


    #     for command in self.commands:
    #         # these are individual send commands so don't need to be wrapped in a block
    #         typing_text += 'Send("' + command + '{ENTER}")'
    #         command_delay = str(random.randint(2000, 20000))
    #         typing_text += 'sleep(" + command_delay + ")'

    #     # add in exit
    #     typing_text += 'Send("exit{ENTER}")'
    #     typing_text += "; Reset Focus"
    #     typing_text += 'SendKeepActive("")'

    #     return textwrap.indent(typing_text, self.indent_space)


    def close_internetExplorer(self):

        """
        Closes the InternetExplorer appliation function declaration
        """

        end_func = """

        SendKeepActive("")
        _IEQuit($oIE)

        EndFunc

        """

        return textwrap.dedent(end_func)


    def create(self):
        """ 
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        # Add in the constructor calls

        autoIT_script = (self.func_dec() +
                        self.open_internetexplorer() +
                        self.close_internetExplorer()
                        )

        return autoIT_script

