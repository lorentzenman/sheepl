
# #######################################################################
#
#  Task : PuttyConnection Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 : Takes a supplied text file for the Sheepl to type
 : the master script will already define the typing speed as part of the master declarations

 ##############################################
        Add in Task Specific Notes Here
 ##############################################

 Notes:
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
        self.taskname = 'PuttyConnection'
        
        # Overrides Base Class Prompt Setup 
        self.baseprompt = cl.yellow('{} >: puttyconnection :> '.format(csh.name.lower()))
        self.prompt = self.baseprompt

        # creating my own 
        self.introduction = """
        ----------------------------------
        [!] PuttyConnection Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Assign credentials using 'credentials'
        3: Add in commands to type
        4: Complete the interaction using 'complete'
        """
        print(textwrap.dedent(self.introduction))

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        # init blank strings
        self.computer = ''
        self.username = ''
        self.password = ''
        self.commands = []

        # Boolean Switch to check for stored credentials
        self.assigned_credentials = False


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
            print("[!] Starting : 'PuttyConnection_{}'".format(str(self.csh.counter.current())))
            # OCD Line break
            print()
            self.prompt = self.cl.blue("[*] {}_{}".format("PuttyConnection", str(self.csh.counter.current()))) + "\n" + self.baseprompt 
            # reset the assigned commands
            


    def do_credentials(self, arg):
        """
        Enter the computer name
        """
        if self.taskstarted == False:
            print(self.cl.red("[!] <ERROR> You need to start a new PuttyConnection Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        
        else:
            if not self.assigned_credentials:
                self.credential_input()
            else:
                answer = self.ask_yes_no_question("[?] Overwrite stored credentials? {} {} :> ".format(
                                                        (self.cl.green("<yes>")), 
                                                        (self.cl.red("<no>"))
                                                        )
                                                    )
                if answer == True:
                    self.credential_input()
            

        print("[!] PuttyConnection Details" )
        print("[*] The target IP address is :   {}".format(self.cl.green(self.computer)))
        print("[*] The Username is set to :     {}".format(self.cl.green(self.username)))
        print("[*] The Pasword is set to :      {}".format(self.cl.green(self.password)))


    def do_show_credentials(self, arg):
        """
        Shows the currently configured credentials for a session
        """ 

        print("[!] The following putty configuration is in place")
        if self.computer:
            print("[*] The target IP address is :   {}".format(self.cl.green(self.computer)))
        else:
            print("[*] The target IP address is :   {}".format(self.cl.green("None")))
        if self.username:
            print("[*] The Username is set to :     {}".format(self.cl.green(self.username)))
        else:
            print("[*] The Username is set to :     {}".format(self.cl.green("None")))
        if self.password:
            print("[*] The Pasword is set to :      {}".format(self.cl.green(self.password)))
        else:
            print("[*] The Pasword is set to :      {}".format(self.cl.green("None")))


    def do_cmd(self, command):
            """
            First checks to see if a new PuttyConnection Block has been started
            if so allows the command to be issued and then runs some checks
            or prompts to start a new interaction using 'new'
            Specify the command to run in the shell
            """
            if command:
                if self.taskstarted == True:   
                    print(command)
                    self.commands.append(command)
                else:
                    if self.taskstarted == False:
                        print(self.cl.red("[!] <ERROR> You need to start a new PuttyConnection Interaction."))
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
                        print(self.cl.red("[!] <ERROR> You need to start a new PuttyConnection Interaction."))
                        print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
                    print("[!] <ERROR> You need to supply the command for typing")



    def do_assigned(self, arg):
        """ 
        Get the current list of assigned typing commands
        """
        print("[?] Currently Assigned Commands ")
        if self.commands:
            for command in self.commands:
                print("[>] {}".format(command))
        else:
            print("[>] No commands currently assigned")


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """
        # setup create_puttyconnection for ease and clarity
        # pass in unique contructor arguments for AutoITBlock

        # Call the static method in the task object
        if self.taskstarted:
            if self.assigned_credentials:
                PuttyConnection.create_autoIT_block(self.csh, 
                                        # add in other arguments
                                        # for object constructor
                                        # --------------------->                         
                                        computer=self.computer,
                                        username=self.username,
                                        password=self.password,
                                        commands=self.commands
                                        # ---------------------> 
                                        )
                # now reset the tracking values and prompt
                self.complete_task()
                self.commands = []

        else:
            print(self.cl.red("[!] You need to assign credentials in order to complete this task"))



    # --------------------------------------------------->
    #   CMD Util Functions
    # --------------------------------------------------->

    def credential_input(self):
        """
        Small Helper Function to request and store the credentials
        sets the assigned_credential Boolean switch to True
        """
        computer = input("[>] Enter the target IP address : ")
        self.computer = computer
        username = input("[>] Enter the username to connect : ")
        self.username = username
        password = input("[>] Enter the connection password : ")
        self.password = password
        self.assigned_credentials = True


# #######################################################################
#  PuttyConnection Class Definition
# #######################################################################


class PuttyConnection:

    def __init__(self, csh, cl, **kwargs):
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


    # --------------------------------------------------->
    #   End PuttyConnection Constructor
    # --------------------------------------------------->

    # --------------------------------------------------->
    #   PuttyConnection Static Method
    # --------------------------------------------------->

    """
    These are all the elements that get passed into the 
    @static method as keyword arguments
    Essentially, this is everything that needs to be passed
    to create the PuttyConnection object

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

        # for key, value in kwargs.items():
        #     print("The Key is : {}".format(key))
        #     if isinstance(value, (list,)):
        #         print("Found a list to parse")
        #         for v in value:
        #             print("I will execute this : {}".format(v))
        #     else:
        #         print("The value is a single entity >> {}".format(value))

        """
        This now creates an instance of the object with the correct
        counter tracker, and then appends as a task
        Note : add in additional constructor arguments as highlighted
               which get passed in from the 'kwargs' dictionary
        """
   
        csh.add_task('PuttyConnection_' + str(csh.counter.current()),
                                PuttyConnectionAutoITBlock(
                                csh,
                                str(csh.counter.current()),
                                # add in other arguments
                                # for object constructor
                                # ---------------------> 
                                kwargs["computer"],
                                kwargs["username"],
                                kwargs["password"],
                                kwargs["commands"]
                                # ---------------------> 
                                ).create()
                            )

          
# #######################################################################
#  PuttyConnection AutoIT Block Definition
# #######################################################################


class PuttyConnectionAutoITBlock:
    """
    Creates an AutoIT Code Block based on the current counter
    then returns this to Task Console which pushes this upto the Sheepl Object
    with a call to create.
    String returns are pushed through (textwarp.dedent) to strip off indent tabs
    """

    def __init__(self, csh, counter, computer, username, password, commands):

        self.csh            = csh
        self.counter        = counter
        self.indent_space   = '    '
        self.computer       = computer
        self.username       = username
        self.password       = password
        self.commands       = commands


    def func_dec(self):
        """
        Initial Entrypoint Definition for AutoIT function
        when using textwrap.dedent you need to add in the backslash
        to the start of the multiline
        """

        function_declaration = """
        ; < ----------------------------------------- >
        ;         PuttyConnection Interaction        
        ; < ----------------------------------------- >

        """
        if self.csh.creating_subtasks == False:
            function_declaration += "PuttyConnection_{}()".format(str(self.counter))

        return textwrap.dedent(function_declaration)


    def open_puttyconnection(self):
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

            _open_puttyconnection = """

            Func PuttyConnection_{}()

                ; Creates a PuttyConnection Interaction

                Send("#r")
                ; Wait 10 seconds for the Run dialogue window to appear.
                WinWaitActive("Run", "", 10)
                Send("putty{}")
                WinWaitActive("[CLASS:PuTTYConfigBox]", "", 10)
                SendKeepActive("[CLASS:PuTTYConfigBox]")

                Send("!n")
                Send("{}")
                Send("!o")

                WinWaitActive("[CLASS:PuTTY]", "", 10)
                SendKeepActive("[CLASS:PuTTY]")

                sleep(5982)
                ; now log in with creds
                Send("{}")
                sleep(4000)
                Send("{}")
                sleep(4000)

            """.format(str(self.counter), "{ENTER}",
                            self.computer + "{ENTER}",
                            self.username + "{ENTER}",
                            self.password + "{ENTER}"
                        )

            return textwrap.dedent(_open_puttyconnection)


    def text_typing_block(self):
        """
        Takes the Typing Text Input
        """

        # now loop round the input_text
        # represents how someone would use the enter key when typing

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


    def close_puttyconnection(self):
        """
        Closes the PuttyConnection appliation function declaration
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
                        self.open_puttyconnection() +
                        self.text_typing_block() +
                        self.close_puttyconnection()
                        )

        return autoIT_script

