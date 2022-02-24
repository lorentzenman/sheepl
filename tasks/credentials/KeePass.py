
# #######################################################################
#
#  Task : KeePass Interaction
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

from utils.base.base_cmd_class import BaseCMD
#from utils.typing import TypeWriter


class KeePass(BaseCMD):

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
        super(KeePass, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'KeePass'
        
        # which might need to be renamed to Sheepl
        self.csh = csh
        # current colour object
        self.cl = cl

        #  Overrides Base Class Prompt Setup
        if csh.creating_subtasks == True:
            print("[^] creating subtasks >>>>>>>>")
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > command >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > keepass >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt
         
         # track subtasks
        self.subtask = False  

        # creating my own
        self.introduction = """
        ----------------------------------
        [!] KeePass Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: This task takes in 'database_location' and 'masterpassword'
        3: You can also supply the title to kill any open windows on loop
        4: Complete the interaction using 'complete'
        """

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        self.database_location = ''
        self.masterpassword = ''

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking 
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    ########################################################################
    # KeePass Class Definition
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
            print("[!] Starting : 'KeePass_{}'".format(str(self.csh.counter.current())))
            # OCD Line break
            print()
            self.prompt = self.cl.blue("[*] KeePass_{}".format(str(self.csh.counter.current()))) + "\n" + self.baseprompt


    def do_database_location(self, location):
        """
        Specifies the keepass location > database_location c:\path.to.keepass.db
        """
        if location:
            if self.taskstarted == True:
                print("[!] Database Location : {}".format(location))
                self.database_location = location
            else:
                if self.taskstarted == False:
                    print(self.cl.red("[!] <ERROR> You need to start a new KeePass Interaction."))
                    print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
                print("[!] <ERROR> You need to supply the command for typing")


    def do_masterpassword(self, masterpassword):
        """
        Specifies the keepass masterpassword credential
        """
        if masterpassword:
            if self.taskstarted == True:
                self.masterpassword = masterpassword
            else:
                if self.taskstarted == False:
                    print(self.cl.red("[!] <ERROR> You need to start a new KeePass Interaction."))
                    print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
                print("[!] <ERROR> You need to supply the command for typing")


    def do_show(self):
        """
        Shows the current configured credentials
        """

        current_setup = """
        > Database Location : {}
        > MasterPassword : {}

        """.format(self.database_location, self.masterpassword)

        print(textwrap.dedent(current_setup))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """
        # setup create_keepass for ease and clarity
        # pass in unique contructor arguments for AutoITBlock

        # Call the static method in the task object
        if self.taskstarted:
            # check to see if required stuff is here
            if (self.database_location and self.masterpassword):
                self.create_autoIT_block()
            
                # now reset the tracking values and prompt
                self.complete_task()
        
            else:
                print("[!] You need to supply a database location and MasterPassword")
                return None
        else:
            print("{} There are currently no command assigned".format(self.cl.red("[!]")))
            print("{} Assign some commands using 'cmd <command>'".format(self.cl.red("[-]")))
            return None


    ########################################################################
    # KeePass AutoIT Block Definition
    ########################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('KeePass_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_keepass() +
            self.text_typing_block() +
            self.close_keepass()
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

        try:
            self.database_location  = kwargs["database_location"]
            self.masterpassword     = kwargs["masterpassword"]
 
            print(f"[*] Setting the command attribute : {self.database_location}")
            print(f"[*] Setting the command attribute : {self.masterpassword}")

        
        except:
            print(self.cl.red("[!] Error Setting JSON Profile attributes, check matching key values in the profile"))

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
        ; < --------------------------------- >
        ;         KeePass Interaction
        ; < --------------------------------- >

        KeePass_{}()

        """.format(str(self.csh.counter.current()))

        return textwrap.dedent(function_declaration)


    def open_keepass(self):
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

        _open_keepass = """

        Func KeePass_{}()

            ; Creates a KeePass Interaction

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            ; note this needs to be escaped
            ; Sends path to Keepdatabase on local box
            Send('{}{}')
            ; check to see if we are already in an RDP session
            $active_window = _WinAPI_GetClassName(WinGetHandle("[ACTIVE]"))
            ConsoleWrite($active_window & @CRLF)
            $inRDP = StringInStr($active_window, "TscShellContainerClass")
            ; if the result is greater than 1 we are inside an RDP session
            if $inRDP < 1 Then
                WinWaitActive("[CLASS:ConsoleWindowClass]", "", 10)
                SendKeepActive("[CLASS:ConsoleWindowClass]")
            EndIf
            ; Keep Window Infocus - longer wait delay to let program catchup
            WinWaitActive('Open Database', "", 40)
            SendKeepActive('Open Database')

        """.format(str(self.csh.counter.current()),
		                self.database_location,
                        "{ENTER}",
		                self.masterpassword
		                )

        return textwrap.dedent(_open_keepass)


    def text_typing_block(self):
        """
        Takes the Typing Text Input
        """
	    # open the database using the masterpassword
        typing_text = 'Send({})\n'.format(self.masterpassword)

        # add in exit - this is achieved using CTRL + q
        typing_text += 'Sleep(15677)\n'
        typing_text += "SendKeepActive('KeePass')\n"
        typing_text += 'Send("^q")\n'
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    def close_keepass(self):

        """
        Closes the KeePass appliation function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)

   
