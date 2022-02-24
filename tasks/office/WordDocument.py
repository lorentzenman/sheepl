
# #######################################################################
#
#  Task : WordDocument Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile
 Takes a supplied text file for the Sheepl to type into a wordocument

"""
__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import sys
import textwrap

#from utils.typing import TypeWriter
from utils.base.base_cmd_class import BaseCMD


class WordDocument(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(WordDocument, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'WordDocument'

        self.csh = csh
        # current colour object
        self.cl = cl
        
         # Overrides Base Class Prompt Setup
        if csh.creating_subtasks == True:
            print("[^] creating subtasks >>>>>>>>")
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > command >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > worddocument >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # booleans to enforce requirements
        #self.typing_block = ''

        # creating my own 
        self.introduction = """
        ----------------------------------
        [!] WordDocument Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new document using 'new'
        2: Add content with 'input_file'
        3: Complete the document using 'complete'
        """
          
        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        self.save_name = ""
        self.input_file = None
        self.typing_block = ''

        # AutoIT header file
        self.autoIT_include_statement = "#include <Word.au3>"

        # might be good to uplift this to the base class as
        # all modules might want the option
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
    # WordDocument Console Commands
    ########################################################################


    def do_new(self, arg):
        """ 
        This command creates a new Word document
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        # Inverse check to see if task has already started
        # Booleans are set in parent method
        if self.check_task_started() == False:
            print("[!] Starting : 'WordDocument_{}'".format(str(self.csh.counter.current())))

            # init typing block with an empty string when new is first called
            self.typing_block = ""

            print("[?] Enter the name to save the document")
            ## BUG check for extension!!
            file_name = input(self.cl.yellow(">: "))
            print("[?] Enter the Windows path location for document save")
            save_path = input(self.cl.yellow(">: "))
            # need to escape the Windows backslash
            if not save_path.endswith("\\"):
                save_path = save_path + '\\'
            # set the taskname to the word document path and name
            self.save_name = save_path + file_name

            print("[!] Saving the file as : {}".format(self.cl.red(self.save_name)))
            # OCD Line break
            print()
            self.prompt = self.cl.blue("[*] Active Document : " + self.save_name) + "\n" + self.baseprompt       


    def do_input_file(self, inputf):
        """
        Specify the path to the input text file for typing
        < input_file /path/to/file >
        """

        """
        This file will also get pushed through the TypeWriter eventually
        """

        try:
            if inputf:
                if self.taskstarted:
                    print("[+] Assigning '{}' for typing ".format(inputf))
                    
                    # now open and read this file and append to the 
                    # typing block
                    with open(inputf) as f:
                        self.typing_block += (f.read().strip())
                else:
                    print(self.cl.red("[!] <ERROR> You need to start a new WordDocument Interaction."))
                    print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))

            else:
                print(self.cl.red("[!] <ERROR> You need to supply the input file for typing"))
        except:
            print(self.cl.red("[!] <ERROR> Accessing input file"))


    def do_complete(self, arg):
        """ 
        This command assigns the save and close Word Functions
        """
        # check check to see if this is already set after a succesful document creation
        # should never been 

        print("task close out and write object for :" + self.csh.name)
        print("[!] Completing Task : {}".format(self.taskname))
        # >>>>>>>>>>>>>>>>>  COMMITS THE DOC <<<<<<<<<<<<<<<<<<<<<
        
        # Here you can perform some checks based on what the task needs        
        if self.taskstarted:
            if self.typing_block:
                self.create_autoIT_block()
            else:
                print("{} Nothing has been set to type into the document - set input_file".format(self.cl.red("[!]")))
                return None
            

        # now reset the tracking values and prompt
        self.complete_task()

        # reset various inputs when new interaction
        self.save_name = ""
        self.typing_block = ""

        
    #######################################################################
    #  WordDocument AutoIT Block Definition
    #######################################################################

    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        Note :
            Kwargs returns a dictionary
            do these values can be referenced
            by the keys directly
        """
        
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('WordDocument_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """ 
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.new_document() +
            self.text_typing_block() +
            self.save_file() +
            self.close_word()
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

        self.input_file = kwargs["input_file"]
        self.save_name = kwargs["save_name"]

        print(f"[*] Setting the input file attribute : {self.input_file}")
        print(f"[*] Setting the save filename attribute : {self.save_name}")

        # now read the input file and set 'self.typing_block' the contents
        # TODO - look at making this into a path object using PathLib (checks for valid path as well)
        #      - next version implement typing object
        
        with open(self.input_file) as f:
            self.typing_block += (f.read().strip()) 

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
        ; <         Word Interaction
        ; < ----------------------------------- >

        """
        if self.csh.creating_subtasks == False:
            function_declaration += "WordDocument_{}()".format(str(self.csh.counter.current()))

        return textwrap.dedent(function_declaration)


    def new_document(self):
        """
        Creates the AutoIT Function Declaration Entry
        """
        new_document = """

        Func WordDocument_{}()

            ; Creates a Word Document : {}

            Local $oWord = _Word_Create()

            ; Add a new empty document
            $oDoc = _Word_DocAdd($oWord)

            WinActivate("[CLASS:OpusApp]")
            WinWaitActive("[CLASS:OpusApp]")
            SendKeepActive("[CLASS:OpusApp]")

        """.format(self.csh.counter.current(), self.save_name)

        return textwrap.dedent(new_document)

    # --------------------------------------------------->
    # Typing Ouput

    def text_typing_block(self):
        """
        Takes the Typing Text Input
        """

        # first read the input text
        # this will change to be grabbed from the list created in the CMD console
        # the processing of each file can be pushed through the TypeWriter function
        
        # This uses the textwrap.indent to add in the indentation
        
        typing_text = '\n' + 'Send("'
        # now loop round the input_text
        # some funkyness here to treat the carriage returns in the file as enter commands
        # represents how someone would use the enter key when typing

        # self.typing_block is part of the init of the object and gets
        # populated by the console when the file is read
        # TODO - this will get pushed through the typing object

        for l in self.typing_block.splitlines():
            # check if this is an empty line -> ie an enter key
            if (len(l) == 0):
                typing_text += ("{ENTER}")
            else:
                typing_text += (l)
            # close off the Send
        typing_text += ('")')

        return textwrap.indent(typing_text, self.indent_space)


    def save_file(self):
        """
        Saves the file where it is specified including any path
        uses textwrap to strip the spaces and clean the code
        """

        command_save_file = """

        ; Reset the SendKeep Active
        SendKeepActive("")
        ; now save
        _Word_DocSaveAs($oDoc,'{}', $WdFormatDocumentDefault)
        _Word_DocClose($oDoc)

        """.format(self.save_name)
        
        # Invoke-OSD
        # for giggles, to keep the first tab in, removes all the extra space
        # and then adds one tab (4 spaces) back in to keep the code clean

        return textwrap.indent(textwrap.dedent(command_save_file), self.indent_space)

    
    # --------------------------------------------------->
    # Close AutoIT Function

    def close_word(self):
        """
        Closes the word appliation function declaration
        """

        end_func = """

            Send("!{F4}")

        EndFunc

        """

        return textwrap.dedent(end_func)


