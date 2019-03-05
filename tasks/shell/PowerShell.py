
# #######################################################################
#
#  Task : PowerShell Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Takes a supplied text file for the Sheepl to type
 the master script will already define the typing speed as part of the master declarations

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
        self.taskname = 'PowerShell'
        # Overrides Base Class Prompt Setup 
        self.baseprompt = cl.yellow('{} >: powershell >: '.format(csh.name.lower()))
        self.prompt = self.baseprompt

        # creating my own 
        self.introduction = """
        ----------------------------------
        [!] PowerShell Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Add in PowerShell commands using cmd
        3: Complete the interaction using 'complete'
        """
        print(textwrap.dedent(self.introduction))

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        # List to hold commands for current interaction
        self.commands = []


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
            print("[!] Starting : 'PowerShell_{}'".format(str(self.csh.counter.current())))
            # OCD Line break
            print()
            self.prompt = "[*] Current Task : PowerShell_{}".format(str(self.csh.counter.current())) + "\n" + self.baseprompt



    def do_cmd(self, command):
            """
            First checks to see if a new PowerShell BLock has been started
            if so allows the command to be issued and then runs some checks
            or prompts to start a new interaction using 'new'
            Specify the command to run in the shell
            <> Example : gwmi win32_service | ? {S_.Status -eq 'Running'}
            """
            if command:
                if self.taskstarted == True:   
                    print(command)
                    self.commands.append(command)
                else:
                    if self.taskstarted == False:
                        print(self.cl.red("[!] <ERROR> You need to start a new PowerShell Interaction."))
                        print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
                    print("[!] <ERROR> You need to supply the command for typing")


    def do_command_file(self, input_file):
            """
            Takes an input command file and parses
            expect one per line
            """
            if input_file:
                if self.taskstarted == True:
                    try:
                        with open(input_file) as command_file:
                            for command in command_file.readlines():  
                                self.commands.append(command.rstrip('\n'))

                    except:
                        print("[!] Error reading file : {}".format(self.cl.red(input_file)))
                else:
                    if self.taskstarted == False:
                        print(self.cl.red("[!] <ERROR> You need to start a new PowerShell Interaction."))
                        print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
                    print("[!] <ERROR> You need to supply the command for typing")


    def do_assigned(self, arg):
        """ 
        Get the current list of assigned PowerShell commands
        """
        print(self.cl.green("[?] Currently Assigned Commands "))
        for command in self.commands:
            print("[>] {}".format(command))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements      
        """

        if self.taskstarted:
            # Call the static method in the task object
            PowerShell.create_autoIT_block(self.csh, 
                                    # add in other arguments
                                    # for object constructor
                                    # ---------------------> 
                                    cmd=self.commands
                                    # ---------------------> 
                                    )


        # now reset the tracking values and prompt
        self.complete_task()

        # reset commands list when new interaction
        self.commands = []


# #######################################################################
#  PowerShell Class Definition
# #######################################################################


class PowerShell:

    def __init__(self, csh, cl, **kwargs):
        """
        Initial object setup
        """
        self.__dict__.update(kwargs)
        
        self.csh = csh
        self.commands = []
        
        if csh.interactive == True:
            # create the task based sub console
            self.TaskConsole = TaskConsole(csh, cl)
            self.TaskConsole.cmdloop()    

    # --------------------------------------------------->
    #   End PowerShell Constructor
    # --------------------------------------------------->        

    # --------------------------------------------------->
    #   PowerShell Static Method
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
       
        This now creates an instance of the object with the correct
        counter tracker, and then appends as a task
        Note : add in additional constructor arguments as highlighted
               which get passed in from the 'kwargs' dictionary

        """

        csh.add_task('PowerShell_' + str(csh.counter.current()),
                                PowerShellAutoITBlock(
                                csh,
                                str(csh.counter.current()),
                                # add in other arguments
                                # for object constructor
                                # ---------------------> 
                                kwargs["cmd"]
                                # ---------------------> 
                                ).create()
                            )

    # --------------------------------------------------->
    #   End PowerShell Static Method
    # --------------------------------------------------->


# #######################################################################
#  PowerShell AutoIT Block Definition
# #######################################################################


class PowerShellAutoITBlock(object):
    """
    Creates an AutoIT Code Block based on the current counter
    then returns this to Task Console which pushes this upto the Sheepl Object
    with a call to create.
    String returns are pushed through (textwarp.dedent) to strip off indent tabs
    """

    def __init__(self, csh, counter, commands):

        self.csh = csh
        self.counter = counter
        self.commands = commands
        self.indent_space = '    '


    def func_dec(self):
        """
        Initial Entrypoint Definition for AutoIT function
        when using textwrap.dedent you need to add in the backslash
        to the start of the multiline
        """
        function_declaration = """\
        ; < ----------------------------------- >
        ; <      PowerShell Interaction
        ; < ----------------------------------- >
        
        """
        # this is an important check as you cannot have nested functions in autoit
        # so you need to check whether to include the command call or not
        # if you are creating subtasks then this call gets pulled from the 
        # 'key' of the subtasks dictionary so cannot be included here
        # which is the reason for this check
        # in other words, all functions need to be declared without nesting
        # it is about where you call the function that matters which in the case
        # of subtasking, is from the parent

        if self.csh.creating_subtasks == False:
            function_declaration += "PowerShell_{}()".format(str(self.counter))

        return textwrap.dedent(function_declaration)


    def open_powershell(self):
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
            """

            _open_powershell = """

            Func PowerShell_{}()

                ; Creates a PowerShell Interaction

                Send("#r")
                ; Wait 10 seconds for the Run dialogue window to appear.
                WinWaitActive("Run", "", 10)
                ; note this needs to be escaped
                Send('powershell{}')
                ; check to see if we are already in an RDP session
                $active_window = _WinAPI_GetClassName(WinGetHandle("[ACTIVE]"))
                ConsoleWrite($active_window & @CRLF)
                $inRDP = StringInStr($active_window, "TscShellContainerClass")
                ; if the result is greater than 1 we are inside an RDP session
                if $inRDP < 1 Then
                    WinWaitActive("Windows PowerShell", "", 10)
                    SendKeepActive("Windows PowerShell")
                EndIf

            """.format(str(self.counter), "{ENTER}")

            return textwrap.dedent(_open_powershell)


    def text_typing_block(self):
        """
        Takes the Typing Text Input
        """

        # Grabas the command list and goes through it
        # This uses the textwrap.indent to add in the indentation
        

        typing_text = '\n'        

        for command in self.commands:
            # these are individual send commands so don't need to be wrapped in a block
            typing_text += ('Send("' + command + '{ENTER}")\n')
            command_delay = str(random.randint(2000, 20000))
            typing_text += ("sleep(" + command_delay + ")\n")
     
        # add in exit
        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    def close_powershell(self):
            """
            Closes the Command Shell appliation function declaration
            """

            end_func = """

            EndFunc

            """

            return textwrap.dedent(end_func)


    def create(self):
        """ 
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        # Add in the constructor calls

        autoIT_script = (self.func_dec() +
                        self.open_powershell() +
                        self.text_typing_block() +
                        self.close_powershell()
                        )

        return autoIT_script

