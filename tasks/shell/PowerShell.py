
# #######################################################################
#
#  Task : PowerShell Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Takes a supplied text file for the Sheepl to type
 the master script will already define the typing speed as part of the master declarations

"""
__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import sys
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD



class PowerShell(BaseCMD):

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
        super(PowerShell, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'PowerShell'

        # current Sheepl Object
        # which might need to be renamed to Sheepl
        self.csh = csh
        # current colour object
        self.cl = cl
        
        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks == True:
            print("[^] creating subtasks >>>>>>>>")
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > command >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > powershell >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt
        # list to hold commands
        self.commands = []
        # track subtasks
        self.subtask = False    
        
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
        
        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >
        
        
        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking 
        # if we are parsing JSON
        
        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    ########################################################################
    # PowerShell Console Commands
    ########################################################################


    def do_new(self, arg):
        """ 
        This command creates a new Powershell interaction
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
            if self.commands:
                self.create_autoIT_block()
            else:
                print("{} There are currently no commands assigned".format(self.cl.red("[!]")))
                print("{} Assign some commands using 'cmd <command>'".format(self.cl.red("[-]")))
                return None

        # now reset the tracking values and prompt
        self.complete_task()

        # reset commands list when new interaction
        self.commands = []


    ######################################################################
    #  PowerShell AutoIT Block Definition
    #######################################################################
    
    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('PowerShell_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_powershell() +
            self.text_typing_block() +
            self.close_powershell()
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
        self.commands = kwargs["cmd"]
        print(f"[*] Setting the commands attribute : {self.commands}")

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
            function_declaration += "PowerShell_{}()".format(str(self.csh.counter.current()))

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

        """.format(str(self.csh.counter.current()), "{ENTER}")

        return textwrap.dedent(_open_powershell)


    # --------------------------------------------------->
    # Typing Ouput

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


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_powershell(self):
        """
        Closes the Command Shell appliation function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)

