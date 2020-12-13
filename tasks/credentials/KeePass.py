

# #######################################################################
#
#  Task : KeePass Interaction
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
        self.taskname = 'KeePass'
        # Overrides Base Class Prompt Setup
        self.baseprompt = cl.yellow('{} >: keepass :> '.format(csh.name.lower()))
        self.prompt = self.baseprompt

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
        print(textwrap.dedent(self.introduction))

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        self.database_location = ''
        self.masterpassword = ''


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
                KeePass.create_autoIT_block(self.csh,
                                    # add in other arguments
                                    # for object constructor
                                    # --------------------->
                                    database_location=self.database_location,
                                    masterpassword=self.masterpassword

                                    # --------------------->
                                    )
                # now reset the tracking values and prompt
                self.complete_task()
            else:
                print("[!] You need to supply a database location and MasterPassword")





    def do_show(self):
        """
        Shows the current configured credentials
        """

        current_setup = """
        > Database Location : {}
        > MasterPassword : {}

        """.format(self.database_location, self.masterpassword)

        print(textwrap.dedent(current_setup))

    # --------------------------------------------------->
    #   CMD Util Functions
    # --------------------------------------------------->




# #######################################################################
#  KeePass Class Definition
# #######################################################################


class KeePass:

    def __init__(self, csh, cl, **kwargs):
        """
        Initial object setup
        """
        self.__dict__.update(kwargs)

        self.csh = csh

        # Check if this task requires an AutoIT Specifc UDF
        # this gets declared here and then pushed into the master
        # if not then this can be deleted
        # Sheepl AutoIT include header list as part of the 'csh' object

        # self.autoIT_include_statement = "#include <Word.au3>"

        # Check to make sure it's not already there, and if not add
        # if not self.autoIT_include_statement in csh.autoIT_UDF_includes:
        #     csh.autoIT_UDF_includes.append(self.autoIT_include_statement)

        if csh.interactive == True:
            # create the task based sub console
            self.TaskConsole = TaskConsole(csh, cl)
            self.TaskConsole.cmdloop()
        # else:
        #     #self.document_setup()
        #     print("Parse the JSON file")
        #     #self.TypeWriter = TypeWriter()


    # --------------------------------------------------->
    #   End KeePass Constructor
    # --------------------------------------------------->


    # --------------------------------------------------->
    #   KeePass Static Method
    # --------------------------------------------------->

    """
    These are all the elements that get passed into the
    @static method as keyword arguments
    Essentially, this is everything that needs to be passed
    to create the KeePass object

    Parse the 'kwargs' dictionary for the arguments
    """

    @staticmethod
    def create_autoIT_block(csh, **kwargs):
        """
        Creates the AutoIT Script Block
        """

        """
        This now creates an instance of the object with the correct
        counter tracker, and then appends as a task
        Note : add in additional constructor arguments as highlighted
               which get passed in from the 'kwargs' dictionary

        """

        csh.add_task('KeePass_' + str(csh.counter.current()),
                                KeePassAutoITBlock(
                                str(csh.counter.current()),
                                # add in other arguments
                                # for object constructor
                                # --------------------->
                                kwargs["database_location"],
                                kwargs["masterpassword"]

                                # --------------------->
                                ).create()
                            )


# #######################################################################
#  KeePass AutoIT Block Definition
# #######################################################################


class KeePassAutoITBlock(object):
    """
    Creates an AutoIT Code Block based on the current counter
    then returns this to Task Console which pushes this upto the Sheepl Object
    with a call to create.
    String returns are pushed through (textwarp.dedent) to strip off indent tabs
    """

    def __init__(self, counter, database_location, masterpassword):

        self.counter = counter
        self.indent_space = '    '
        self.database_location = database_location
        self.masterpassword = masterpassword



    def func_dec(self):
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

        """.format(str(self.counter))

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

        """.format(str(self.counter),
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

    def create(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        # Add in the constructor calls

        autoIT_script = (self.func_dec() +
                        self.open_keepass() +
                        self.text_typing_block() +
                        self.close_keepass()
                        )

        return autoIT_script
