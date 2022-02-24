
# #######################################################################
#
#  Task : PuttyConnection Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile
 Creates a putty connection and then issues commands

"""
__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"

import cmd
import sys
import random
import textwrap

from utils.base.base_cmd_class import BaseCMD
#from utils.typing import TypeWriter


class PuttyConnection(BaseCMD):

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
        super(PuttyConnection, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'PuttyConnection'

        # current Sheepl Object
        # which might need to be renamed to Sheepl
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks == True:
            print("[^] creating subtasks >>>>>>>>")
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > puttyconnection >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > puttyconnection >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt
        
        # Set boolean switch to confirm if this can be used as a subtask
        self.subtask = False
        
       
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
        self.indent_space = '    '

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

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking 
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()

    #######################################################################
    # PuttyConnection Console Commands
    #######################################################################

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
                self.create_autoIT_block()
                # now reset the tracking values and prompt
                self.complete_task()
                self.commands = []
        else:
            print(self.cl.red("[!] You need to assign credentials in order to complete this task"))


######################################################################
# PuttyConnection AutoIT Block Definition
#######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('PuttyConnection' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """ 
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_puttyconnection() +
            self.text_typing_block() +
            self.close_puttyconnection()
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
            self.computer = kwargs["computer"]
            self.username = kwargs["username"]
            self.password = kwargs["password"]
            self.commands = kwargs["cmd"]

            # if multiple commands are sent then the raise an error and show that the RunCommands only take the latest
            # parse the list and grab the first one
            print(f"[*] Setting the command attribute : {self.computer}")
            print(f"[*] Setting the command attribute : {self.username}")
            print(f"[*] Setting the command attribute : {self.password}")
            print(f"[*] Setting the command attribute : {self.commands}")
        
        except:
            print(self.cl.red("[!] Error Setting JSON Profile attributes, check matching key values in the profile"))

        # once these have all been set in here, then self.create_autoIT_block() gets called which pushes the task on the stack
        self.create_autoIT_block()

    
    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
         """

        function_declaration = """
        ; < ----------------------------------------- >
        ;         PuttyConnection Interaction        
        ; < ----------------------------------------- >

        """
        if self.csh.creating_subtasks == False:
            function_declaration += "PuttyConnection_{}()".format(str(self.csh.counter.current()))

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

                ; need an if else check here--
                ; if the window title is "PuTTY Security Alert then this is asking for host verification
                ; so need to send the ALT Y to this to accept the warning
                ; else this is the active PUTTY class

                WinWaitActive("[CLASS:PuTTY]", "", 10)
                SendKeepActive("[CLASS:PuTTY]")

                sleep(5982)
                ; now log in with creds
                Send("{}")
                sleep(4000)
                Send("{}")
                sleep(4000)

            """.format(str(self.csh.counter.current()), "{ENTER}",
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