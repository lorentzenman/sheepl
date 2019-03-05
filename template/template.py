"""
 This is a template to create Class base
 Provides the stub code for a task

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import os
import sys
import textwrap


class CreateTemplate(object):
    """
    Creates a template object with stub code
    """

    def __init__(self, name):
        """
        Takes the name from argparse and builds out a template for this
        """
        self.name = name
        self.indent_space = '    '

        output_file_name = name + ".py"
        with open(output_file_name, "w") as template_file:
            template_file.write(
                self.template_create_notes_header() +
                self.template_notes() +
                self.template_author_details() +
                self.template_modules() +
                self.template_class_cmd_declaration() +
                self.template_class_cmd_internals() +
                self.template_common_cmd_functions_new() +
                self.template_common_cmd_functions_cmd() +
                self.template_common_cmd_functions_complete() +
                self.template_helper_function_comment() +
                self.template_task_class_definition() +
                self.template_task_class_static_method_definition() +
                self.template_class_autoIT_block_definition() +
                self.template_class_autoIT_block_open() +
                self.template_class_autoIT_block_typing() +
                self.template_class_autoIT_block_close() +
                self.template_class_autoIT_create()
            )


    def template_create_notes_header(self):
        """
        Formatter for notes file at the top of the task
        """
        notes_header = """
        
        # #######################################################################
        #
        #  Task : {} Interaction
        #
        # #######################################################################
        
        """.format(self.name)

        return textwrap.dedent(notes_header)


    def template_notes(self):
        """
        Builds out the notes at the top of the file
        """
        
        class_notes = """
        \"""
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
        \"""
        """.format(self.name)

        return textwrap.dedent(class_notes)


    def template_author_details(self):
        """
        Creates the author details
        """

        author_notes = """
        __author__ = ""
        __license__ = "MIT"
        """

        return textwrap.dedent(author_notes)  


    def template_modules(self):
        """
        Imports common modules to be used across all templates
        """

        module_imports = """
        import cmd
        import sys
        import random
        import textwrap

        from utils.base.base_cmd_class import BaseCMD
        """

        return textwrap.dedent(module_imports)


    # #######################################################################
    # Template CMD Definition
    # #######################################################################


    def template_class_cmd_declaration(self):
        """
        Main Class Declaration
        """

        class_declaration = """

        # #######################################################################
        #  Task CMD Class Module Loaded into Main Sheepl Console
        # #######################################################################


        class TaskConsole(BaseCMD):
        """
        return textwrap.dedent(class_declaration)


    def template_class_cmd_internals(self):

        class_internals = """
        \"""
        Inherits from BaseCMD
            This parent class contains:
            : do_back               > return to main menu
            : do_discard            > discard current task
            : complete_task()       > completes the task and resets trackers
            : check_task_started    > checks to see task status
        \"""
        """
        
        class_internals += """
        def __init__(self, csh, cl):

            # Calling super to inherit from the BaseCMD Class __init__
            super(TaskConsole, self).__init__(csh, cl)

        """

        class_internals += """
            # Override the defined task name
            self.taskname = '{}'
            # Overrides Base Class Prompt Setup 
            self.baseprompt = cl.yellow('{} >: {} :> '.format(csh.name.lower()))
            self.prompt = self.baseprompt
            """.format(self.name, '{}', self.name.lower())

        class_internals += """
            # creating my own 
            self.introduction = \"""
            ----------------------------------
        """

        class_internals += self.indent_space + "[!] {} Interaction.".format(self.name)

        class_internals += """
            Type help or ? to list commands.
            ----------------------------------
            1: Start a new block using 'new'
            2: ######### > add in steps
            3: Complete the interaction using 'complete'
            \"""
            print(textwrap.dedent(self.introduction))
            
            # ----------------------------------- >
            #      Task Specific Variables
            # ----------------------------------- >

            # List to hold commands for current interaction
            # self.commands = []

            # Configures Subtasking
            # self.subtask_supported = True

            # empty subtask dictionary to hold assigned tasks
            # self.subtasks = \{\}
        """

        return textwrap.indent(textwrap.dedent(class_internals), self.indent_space)


    def template_common_cmd_functions_new(self):
        """
        Creates new common function
        """

        task_common_functions_new = """

        # --------------------------------------------------->
        #   Task CMD Functions
        # --------------------------------------------------->

        def do_new(self, arg):
            \""" 
            This command creates a new Word document
            \"""
            # Init tracking booleans
            # method from parent class BaseCMD
            # Inverse check to see if task has already started
            # Booleans are set in parent method
            
            # method from parent class BaseCMD
            if self.check_task_started() == False:
                print("[!] Starting : '{}_{}'".format(str(self.csh.counter.current())))
                # OCD Line break
                print()
                self.prompt = self.cl.blue("[*] {}_{}".format(str(self.csh.counter.current()))) + "{}" + self.baseprompt       
                """.format(self.name, '{}', self.name, '{}','\\n')

        return textwrap.indent(textwrap.dedent(task_common_functions_new), self.indent_space)


    def template_common_cmd_functions_cmd(self):
        """
        Common command loop
        """

        task_common_function_commands = """
        
        def do_cmd(self, command):
            \"""
            First checks to see if a new {} Block has been started
            if so allows the command to be issued and then runs some checks
            or prompts to start a new interaction using 'new'
            Specify the command to run in the shell
            \"""
            # Uncomment
            \"""
            if command:
                if self.taskstarted == True:   
                    self.commands.append(command)
                else:
                    if self.taskstarted == False:
                        print(self.cl.red("[!] <ERROR> You need to start a new {} Interaction."))
                        print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
                    print("[!] <ERROR> You need to supply the command for typing")
            pass
            \"""
        """.format(self.name, self.name)

        return textwrap.indent(textwrap.dedent(task_common_function_commands), self.indent_space)


    def template_common_cmd_functions_complete(self):
        """
        Creates complete common function
        """

        task_common_functions_complete = """
        
        def do_complete(self, arg):
            \"""
             
            This command calls the constructor on the AutoITBlock
            with all the specific arguments
            >> Check the AutoIT constructor requirements
        
            setup create_internetexplorer for ease and clarity
            pass in unique contructor arguments for AutoITBlock
        
            \"""

            # Call the static method in the task object
            if self.taskstarted:
                {}.create_autoIT_block(self.csh, 
                                    # add in other arguments
                                    # for object constructor
                                    # ---------------------> 
                                    ''
                                    # ---------------------> 
                                    )

            # now reset the tracking values and prompt
            self.complete_task()

        """.format(self.name)
        
        return textwrap.indent(textwrap.dedent(task_common_functions_complete), self.indent_space)


    def template_helper_function_comment(self):
        """
        Adds in the CMD util function comment space
        """

        helper_function_comment = """

        # --------------------------------------------------->
        #   CMD Util Functions
        # --------------------------------------------------->

        """

        return textwrap.indent(textwrap.dedent(helper_function_comment), self.indent_space)


    # #######################################################################
    # # #  Template Task Definition
    # #######################################################################
        

    def template_task_class_definition(self):
        """ 
        Creates the task subcode with inheritance
        """

        template_task_class_definition = """

        # #######################################################################
        #  {} Class Definition
        # #######################################################################


        class {}:

            def __init__(self, interactive, counter, csh, cl):
                \"""
                >> interactive, id, csh, cl all come form the baseclass

                By using super, we can still maintain the dynamic module import structures
                found in the sheepl console, but we can add custom functionality

                \"""
                # Calling super to inherit from the BaseTask __init__
                super({}, self).__init__(interactive, counter, csh, cl)

                # task specific arguments for object
                # otherwise you would need to mess around with the constructor


                # Check if this task requires an AutoIT Specifc UDF
                # this gets declared here and then pushed into the master
                # if not then this can be deleted
                # Sheepl AutoIT include header list as part of the 'csh' object

                # self.autoIT_include_statement = "#include <Word.au3>"

                # Check to make sure it's not already there, and if not add
                # if not self.autoIT_include_statement in csh.autoIT_UDF_includes:
                #     csh.autoIT_UDF_includes.append(self.autoIT_include_statement)
            
                if interactive:
                    # create the task based sub console
                    self.TaskConsole = TaskConsole(csh, cl)
                    self.TaskConsole.cmdloop()            
                


            # --------------------------------------------------->
            #   End {} Constructor
            # --------------------------------------------------->
        """.format(self.name, self.name, self.name, self.name)

        return textwrap.dedent(template_task_class_definition)


    def template_task_class_static_method_definition(self):
        """ 
        Creates the task subcode with inheritance
        """

        template_task_class_static_method_definition = """

            # --------------------------------------------------->
            #   {} Static Method
            # --------------------------------------------------->

            \"""
            These are all the elements that get passed into the 
            @static method as keyword arguments
            Essentially, this is everything that needs to be passed
            to create the InternetExplorer object

            Parse the 'kwargs' dictionary for the arguments
            \"""

            @staticmethod
            def create_autoIT_block(csh, **kwargs):
                \"""
                Creates the AutoIT Script Block
                Note :
                    Kwargs returns a dictionary
                    do these values can be referenced
                    by the keys directly
            
                This now creates an instance of the object with the correct
                counter tracker, and then appends as a task
                Note : add in additional constructor arguments as highlighted
                    which get passed in from the 'kwargs' dictionary

                \"""

                csh.add_task('{}_' + str(csh.counter.current()),
                                        {}AutoITBlock(
                                        csh,
                                        str(csh.counter.current()),
                                        # add in other arguments
                                        # for object constructor
                                        # ---------------------> 
                                        ''
                                        # ---------------------> 
                                        ).create()
                                    )

            # --------------------------------------------------->
            #   End {} Static Method
            # --------------------------------------------------->
            """.format(self.name, self.name, self.name, self.name)

        return textwrap.indent(textwrap.dedent(template_task_class_static_method_definition), self.indent_space) 


    # #######################################################################
    #  Template AutoITBlock Definition
    # #######################################################################


    def template_class_autoIT_block_definition(self):
        """
        Creates the AutoIT block code
        """

        autoIT_block_definition = """

        # #######################################################################
        #  {} AutoIT Block Definition
        # #######################################################################


        class {}AutoITBlock(object):
            \"""
            Creates an AutoIT Code Block based on the current counter
            then returns this to Task Console which pushes this upto the Sheepl Object
            with a call to create.
            String returns are pushed through (textwarp.dedent) to strip off indent tabs

            Build out your constructor based on what the object takes
            \"""

            def __init__(self, csh, counter):

                self.csh = csh
                self.counter = counter
                self.indent_space = '    '


            def func_dec(self):
                \"""
                Initial Entrypoint Definition for AutoIT function
                when using textwrap.dedent you need to add in the backslash
                to the start of the multiline
                \"""

                function_declaration = \"""\

        """.format(self.name, self.name)

        autoIT_block_definition += self.helper_create_func_declaration_header(self.name)

        autoIT_block_definition += """

                if self.csh.creating_subtasks == False:
                    function_declaration += "{}_{}()".format(str(self.counter))

                return textwrap.dedent(function_declaration)
        """.format(self.name, '{}')
        
        return textwrap.dedent(autoIT_block_definition)


    def template_class_autoIT_block_open(self):
        """
        Initialises the common operation for opening the program
        this is normally invoked via the 'run' command

        """

        open_program_call = """

        def open_{}(self):
            \"""
            Creates the AutoIT Function Declaration Entry
            \"""

            \"""
            # Note a weird bug that the enter needs to be 
            # passed as format string argument as escaping
            # is ignored on a multiline for some reason
            # if it gets sent as an individual line as in text_typing_block()
            # >> typing_text += "Send('exit{}')"
            # everything works. Strange, Invoke-OCD, and then stop caring
            # and push it through the format string.

            # Note > Send('yourprogram{}')
            # Example : Send('powershell{}')
            \"""

            _open_{} = \"""
            
            Func {}_{}()

                ; Creates a {} Interaction

                Send("#r")
                ; Wait 10 seconds for the Run dialogue window to appear.
                WinWaitActive("Run", "", 10)
                ; note this needs to be escaped
                ; <PROGRAM EXECUTION>
                Send('cmd{}') 
                ; Keep Window Infocus
                WinWaitActive('#', "", 10)
                SendKeepActive('#')

            \""".format(self.counter)

            return textwrap.dedent(_open_{})   
            """.format(
                    self.name.lower(),
                    '{ENTER}', '{ENTER}', '{ENTER}',
                    self.name.lower(), 
                    self.name, '{}',
                    self.name,
                    '{ENTER}',
                    self.name.lower()
                )

        return textwrap.indent(textwrap.dedent(open_program_call), self.indent_space)


    def template_class_autoIT_block_typing(self):
        """
        Creates the AutoIT typing block
        """

        autoIT_text_typing_block = """

        def text_typing_block(self):
            \"""
            Takes the Typing Text Input
            \"""
         
            typing_text = 'Send("")'
            # now loop round the input_text
            # represents how someone would use the enter key when typing
        

            for command in self.commands:
                # these are individual send commands so don't need to be wrapped in a block
                typing_text += 'Send("' + command + '{}")'
                command_delay = str(random.randint(2000, 20000))
                typing_text += 'sleep(" + command_delay + ")'
        
            # add in exit
            typing_text += 'Send("exit{}")'
            typing_text += "; Reset Focus"
            typing_text += 'SendKeepActive("")'

            return textwrap.indent(typing_text, self.indent_space)

            """.format(
                "{ENTER}",
                "{ENTER}"
            )

        return textwrap.indent(textwrap.dedent(autoIT_text_typing_block), self.indent_space)


    def template_class_autoIT_block_close(self):
        """
        Creates the AutoIT Close block
        """
        
        close_program_call = """
        def close_{}(self):     
            \"""
            Closes the {} application function declaration
            \"""

            end_func = \"""

            EndFunc

            \"""

            return textwrap.dedent(end_func)
            """.format(self.name, self.name)

        return textwrap.indent(textwrap.dedent(close_program_call), self.indent_space)


    def template_class_autoIT_create(self):
        """
        Creates the main call to the constructor function for the object
        make sure to pass in the constructor parameters based on what has been 
        defined in this task constructor
        """

        autoIT_create = """
            def create(self):
                \""" 
                Grabs all the output from the respective functions and builds the AutoIT output
                \"""

                # Add in the constructor calls

                autoIT_script = (self.func_dec() +
                                '' +
                                self.text_typing_block() +
                                ''
                                )

                return autoIT_script

            """

        return textwrap.indent(textwrap.dedent(autoIT_create), self.indent_space)


    # #######################################################################
    #  Template Helper Functions 
    # #######################################################################


    def helper_create_func_declaration_header(self, name):
        """
        Simple wrapper function to properly work out 
        the formatting size of the header
        keeps the code clean and my OCD in check
        """

        dash        = "-"
        space       = '        '
        left_bar    = "; < -------"
        right_bar   = "------- >"
        middle      = "; "
        indent      = '    '

        title_length = len(self.name + " Interaction")

        top_bar = left_bar + (dash * title_length) + right_bar
        middle_bar = middle + space + (self.name + " Interaction") + space 
        bottom_bar = left_bar + (dash * title_length) + right_bar


        # No idea why a) I thought this was a good idea, and b)
        # why you have to multiply the idents
        # ultimately though, the textwrap library strips all this
        # out so it's only needed for cleanliness to push this over
        # all this to make a dynamically expanding title box.

        return (
                (indent * 2) + top_bar + "\n" + 
                (indent * 4) + middle_bar + "\n" +
                (indent * 4) + bottom_bar
                )


   
