
# #######################################################################
#
#  Task : InternetExplorer Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 : Takes a supplied text file for the Sheepl to type
 : the master script will already define the typing speed as part of the master declarations

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


class InternetExplorer(BaseCMD):

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
        super(InternetExplorer, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'InternetExplorer'

        # current Sheepl Object
        # which might need to be renamed to Sheepl
        self.csh = csh
        # current colour object
        self.cl = cl

        #  Overrides Base Class Prompt Setup
        if csh.creating_subtasks == True:
            print("[^] creating subtasks >>>>>>>>")
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > command >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > runcommand >: '.format(csh.name.lower()))

        self.prompt = self.basepromptt

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

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        self.destination_url = ''
        self.autoIT_include_statement = "#include <IE.au3>"

        # Check to make sure it's not already there, and if not add
        if not self.autoIT_include_statement in self.csh.autoIT_UDF_includes:
            self.csh.autoIT_UDF_includes.append(self.autoIT_include_statement)

        
        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking 
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    ########################################################################
    # InternetExplorer Console Commands
    ########################################################################


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
            if self.destination_url:
                self.create_autoIT_block()

                # now reset the tracking values and prompt
                self.complete_task()
        else:
            print("{} There is currently no URL assigned".format(self.cl.red("[!]")))


 
    ########################################################################
    # InternetExplorer AutoIT Block Definition
    ########################################################################

    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('InternetExplorer_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """ 
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.func_dec() +
            self.open_internetexplorer() +
            self.close_internetExplorer()
        )

        return autoIT_script
 
 
    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and build out task variables when using JSON profiles
        this function sets the various object attributes in the same way
        that the interactive mode does
        """
    
        print("[%] Setting attributes from JSON Profile")
        # This snippet takes the keys ignoring the first key which is task and then shows
        # what should be set in the kwargs parsing. 
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")
        
        self.destination_url = kwargs["destination_url"]
      
        print(f"[*] Setting the command attribute : {self.destination_url}")

        # once these have all been set in here, then self.create_autoIT_block() gets called which pushes the task on the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block


    def autoit_function_open(self):
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
        """.format(str(self.csh.counter.current()))

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

        """.format(str(self.csh.counter.current()),
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


    

