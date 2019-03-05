
# #######################################################################
#
#  Task : WordDocument Interaction
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
import textwrap

#from utils.typing import TypeWriter
from utils.base.base_cmd_class import BaseCMD


#######################################################################
#  Task CMD Class Module Loaded into Main Sheepl Console
#######################################################################


class TaskConsole(BaseCMD):
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
        super(TaskConsole, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'WordDocument'

        # Overrides Base Class Prompt Setup 
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
        print(textwrap.dedent(self.introduction))

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        # Create empty list to hold all input files
        self.input_files = []


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
                    self.input_file = inputf
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
        """
        Instantiates WordDocumentAutoITBlock() as an object, then passes the 
        word_document save name created in 'new' and then passes in the typing block
        created from input_file
        WordDocumentAutoITBlock(counter, typing_block, save_name)
        """

        # Call the static method in the task object
        if self.taskstarted:
            WordDocument.create_autoIT_block(self.csh, 
                                    # add in other arguments
                                    # for object constructor
                                    # ---------------------> 
                                    #input_file = self.input_file,
                                    save_name = self.save_name,
                                    input_file = self.input_file

                                    # ---------------------> 
                                    )

        # now reset the tracking values and prompt
        self.complete_task()


#######################################################################
#  WordDocument Class Definition
#######################################################################


class WordDocument:

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

        self.autoIT_include_statement = "#include <Word.au3>"
        
        # Check to make sure it's not already there, and if not add
        if not self.autoIT_include_statement in csh.autoIT_UDF_includes:
            csh.autoIT_UDF_includes.append(self.autoIT_include_statement)

        if csh.interactive == True:
            # create the task based sub console
            self.TaskConsole = TaskConsole(csh, cl)
            self.TaskConsole.cmdloop()  


    # --------------------------------------------------->
    #   End WordDocument Constructor
    # --------------------------------------------------->

    # --------------------------------------------------->
    #   WordDocument Static Method
    # --------------------------------------------------->

    """
    These are all the elements that get passed into the 
    @static method as keyword arguments
    Essentially, this is everything that needs to be passed
    to create the WordDocument object

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

        csh.add_task('WordDocument_' + str(csh.counter.current()),
                                WordDocumentAutoITBlock(
                                str(csh.counter.current()),
                                # add in other arguments
                                # for object constructor
                                # ---------------------> 
                                #kwargs["input_file"],
                                kwargs["save_name"],
                                kwargs["input_file"]
                                # ---------------------> 
                                ).create()
                            )


#######################################################################
#  WordDocument AutoIT Block Definition
#######################################################################


class WordDocumentAutoITBlock(object):
    """
    Creates an AutoIT Code Block based on the current counter
    then returns this to Task Console which pushes this upto the Sheepl Object
    with a call to create.
    String returns are pushed through (textwarp.dedent) to strip off indent tabs
    """

    def __init__(self, counter, save_name, input_file):

        self.counter = counter
        self.indent_space = '    '
        self.save_name = save_name
        self.input_file = input_file
        self.typing_block = ''
        with open(input_file) as f:
            self.typing_block += (f.read().strip())




    def func_dec(self):
        """
        Initial Entrypoint Definition for AutoIT function
        when using textwrap.dedent you need to add in the backslash
        to the start of the multiline
        """

        function_declaration = """\

        ; < ----------------------------------- >
        ; <         Word Interaction
        ; < ----------------------------------- >


        WordDocument_{}()

        """.format(self.counter)

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

        """.format(self.counter, self.save_name)

        return textwrap.dedent(new_document)


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


    def close_word(self):
        """
        Closes the word appliation function declaration
        """

        end_func = """

            Send("!{F4}")

        EndFunc

        """

        return textwrap.dedent(end_func)


    def create(self):
        """ 
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (self.func_dec() +
                        self.new_document() +
                        self.text_typing_block() +
                        self.save_file() +
                        self.close_word()
                        )

        return autoIT_script
