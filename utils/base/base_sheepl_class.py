"""
 The base Sheepl Object Class

 Notes:
    The textwrap import is used to keep the AutoIT functions indented in code
    as this messes with the python code (back off OCD) when it's manually
    appearing to hang outside of the class declarations and also stops code collapse in IDEs.
    So when creating code specific to the AutoIT functions just use tabs to indent insitu
    and the textwarp library will strip all leading tabs from the beginning of the AutoIT block.
    Also uses textwrap.indent() to add indentation to commands or statements that should be
    inline from the initial function declaration

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import random
import textwrap
import importlib

# Sheepl Class Imports
from utils.tasks import Tasks
from utils.counter import Counter

#######################################################################
#   Sheepl Class
#######################################################################

class Sheepl(object):
    """
    Creates a digital person and is ready to type the commands
    """
    # this is the core Tasks dictionary
    # DEBUG >> check to see if this can be moved into INIT
    #tasks = {}
    #headers = .action_headers()


    def __init__(self, name, total_time, type_speed, loop, cl, interactive):

        self.name = name
        self.total_time = total_time
        self.loop = loop
        self.cl = cl
        # interactive switch
        self.interactive = interactive
        # boolean for JSON profile input
        self.json_parsing = False
        
        # needs to be a string for JSON
        self.icon = "True"
        self.birth = False

        # First create task Object
        self.available_tasks = Tasks()

        # Calls the Task object to return all the available lists
        #self.task_list = dict(self.available_tasks.locate_available_tasks().items())
        self.task_list = self.update_available_tasks()

        # empty task dictionary to hold assigned tasks
        self.tasks = {}

        # boolean to track subtask status and calling parent class
        self.creating_subtasks = False
        self.parent_task = ''
        
        # empty subtask dictionary to hold assigned tasks
        self.subtasks = {}

        # empty list to hold window kill list
        self.window_kill_list = []

        # set profile file path to an empty string
        self.profile_path = ''

        # Start counter instance that maps to tasks
        self.counter = Counter()

        # File setup
        self.output_base = "output/"
        self.file_name = name.replace(' ', '_')
        self.file_name = name.lower() + '.au3'
        self.file_name = self.output_base + self.file_name

        print("[>] Creating the file : {}".format(self.cl.red(self.file_name)))
        self.typing_speed = self._typing_speed(type_speed)

        # Whether the task list loops or runs once
        print("[>] Looping set to : {}".format(self.cl.red(str(self.loop))))

        # Display JSON Parsling
        print("[>] JSON Parsing : {}".format(self.cl.red(str(self.json_parsing))))

        # AutoIT Include Header List
        self.autoIT_include_statement = ''
        self.autoIT_UDF_includes = ['#include <Array.au3>', '#include <WinAPI.au3>']

        # OCD lines
        print()
        # say hello
        self.say_hello()
        print()


    def say_hello(self):
        """
        Grabs stupid hobbies from the lists
        """
        print(self.cl.blue("[~] Hello, my name is {}".format(self.name)))
        h1, h2 = self.hobbies()
        print(self.cl.blue("[~] I like {} and {}.".format(h1, h2)))


    def hobbies(self):
        """ Creates a random list of hobbies """
        hobbies1 = [
            "walks on the beach",
            "flower arranging",
            "decompiling PE files",
            "ironing my socks",
            "giving out opinions",
            "collecting fluff",
            "reading stuff about IT security"
        ]

        hobbies2 = [
            "dancing in clogs",
            "polishing oranges",
            "watching sunrises",
            "eating",
            "reading 20th century poetry",
            "ssh tunneling",
            "coding using python",
        ]
        return random.choice(hobbies1), random.choice(hobbies2)


    def tea_break_task(self):
        """
        Creates the initial delay at the start of the exercise as a small task
        Sheepl always start the day with a tea break
        """

        tea_break = """\
        ; < ----------------------------------- >
        ; <             Tea Break
        ; < ----------------------------------- >

        ; Nothing to do here but have a cuppa, it's a placeholder for a tea break
        ; creates an entry in the task list to then take a random slice of the
        ; timeslot which results in a random sleep action
                """

        return textwrap.dedent(tea_break)

    # --------------------------------------------------->
    #   Task Structures
    # --------------------------------------------------->


    def list_tasks(self):
        """
        Gets the relevant Task list from the dictionary
        """

        print(self.cl.green("\n[!] Sheepl can create the following tasks: \n"))
        for task in self.task_list.values():
             print("[*] {}".format(task))
        # OCD line break
        print()


    def generate_task(self, task):
        """
        Generates a task class
        """

        for module_import_path, module in (self.task_list.items()):
            if task == module:
                task_module = importlib.import_module(module_import_path)
                task_class_name = getattr(task_module, module)
                """
                Creates instance of the selected class
                all classes need to confirm to a structure
                """
                # task_instance = task_class_name(self.interactive, self.csh.counter.increment(), self.csh, self.cl)
                # task_class_name(self.csh, self.interactive, self.csh.counter.current(), self.cl)
                return task_class_name(self, self.cl)


    def add_task(self, task, output):
        """
        Add a task to the dictionary
        """
        # checks to see whether we are subtasking
        if self.creating_subtasks == False:
            self.tasks[task] = output
            #print(self.tasks)
        else:
            self.subtasks[task] = output
        # increment the counter value
        self.counter.increment()


    def update_available_tasks(self):
        """
        Updates the task list
        """
        self.task_list = dict(self.available_tasks.locate_available_tasks().items())

        return self.task_list


    # --------------------------------------------------->
    #   Typing Capabilty and Parsing
    # --------------------------------------------------->


    def _typing_speed(self, speed):
        """
        Global Typing Speed
        """
        #speed = '60'
        typing_speed = 'Opt("SendKeyDelay", {})\n'.format(speed)
        print("[^] Global Typing Speed set to : {}".format(speed) + 'ms delay')

        return typing_speed


    def autoIT_start(self, total_tasks, task_names, sleep_list_length, sleep_time_list):
        """
        Takes in the current tasks length, and the defined sleep times
        and builds the start of the autoIT file with global arrays
        support looping switch so on every loop the task list gets cloned to
        a new array that gets shuffled. This means that every loop the task list
        is randomised and the sleep times are randomised
        uses list comprehension to walk over the pushed in lists
        moar random to add to your random
        """

        task_list_output = """\
        ; define global task list
        Global $aTasks[{}] = {} """.format(total_tasks, ([t for t in task_names]))

        sleep_time_output = """\

        ; creates Sleep Times array
        Global $aSleepTimes[{}] = {}
        ; copies original array just encase the task list borks
        $aRandTasks = $aTasks
        """.format(sleep_list_length, ([str(s) for s in sleep_time_list]))

        return textwrap.dedent(task_list_output), textwrap.dedent(sleep_time_output)


    def _window_watcher(self):
        """
        For each task in the tasklist, functions that spawn a window that could
        be left behind, are added to this loop.
        Master function is a watcher that tracks all Window titles in array
        windows list is an array
        """
        # sort out the array for the list
        # print("Global $winKillList[" + str(len(windows_to_watch)) + "] = " + str(windows_to_watch))
        window_list = "Global $winKillList[" + str(len(self.window_kill_list)) + "] = " + str(self.window_kill_list) + "\n"

        window_func_declaration = """
        ; < ------------------------------------ >
        ;        Window watcher Function
        ; < ------------------------------------ >

        Func Window_Watcher()

        """

        windows_to_watch = """
        ; Retrieve a list of window handles.
        Local $aList = WinList()
        ; Loop through the array displaying only visable windows with a title.
        For $i = 1 To $aList[0][0]
            If $aList[$i][0] <> "" And BitAND(WinGetState($aList[$i][1]), 2) Then
        	    $winTitle = $aList[$i][0]
        	    $winCheck = _ArraySearch($winKillList, $winTitle)
        	    If $winCheck = 0 Then
        		    ConsoleWrite("[!] Found  -> " & $winTitle & @CRLF)
        		    WinKill($winTitle)
    		    EndIf
    	    EndIf
        Next
        """
        window_func_end = """
        EndFunc

        ; < ------------------------------------ >
        ;        End Window watcher Function
        ; < ------------------------------------ >
        """

        print("[>] Global Kill list created")
        print("[>] {}".format(window_list))
        # now build out the string correctly
        global_win_list =  textwrap.dedent(window_list) + textwrap.dedent(window_func_declaration) + textwrap.dedent(windows_to_watch) + textwrap.dedent(window_func_end)
        return global_win_list


    def autoIT_UDF_headers(self, autoIT_include_statement):
        """
        Add in headers based on dictionary object
        Takes in the autoIT_include_statement
        """
        if not self.autoIT_include_statement in self.autoIT_UDF_includes:
            self.autoIT_UDF_includes.append(self.autoIT_include_statement)


    def parse_time_values(self, total_time):
        """
        Takes the total time and then parses this out into
        milliseconds and seconds as needed
        """
        # sorts out time into milliseconds
        if 'm' in self.total_time:
            total_time = int(self.total_time.split('m')[0]) * (1000 * 60)
        elif 'h' in self.total_time:
            total_time = int(self.total_time.split('h')[0]) * (1000 * 60 * 60)
        else:
            # 1000 milliseconds to 1minute -> then to 1hour
            total_time = (1000 * 60 * 60)

        total_tasks = len(self.tasks.keys())
        print(self.cl.red("TOTAL TASKS ARE {}".format(total_tasks)))
        print(self.cl.red("TOTAL TIME IS {}".format(str(total_time))))

        # https://stackoverflow.com/questions/3589214/generate-multiple-random-numbers-to-equal-a-value-in-python

        # original code below. removed one from total_tasks to match the range
        # the goal is to have one more sleep time than the total task list so that there is an initial
        # random start time (each time if looped)
        # dividers = sorted(random.sample(range(1, total_time), total_tasks -1))
        # new code drops the decrement based on the total_tasks

        dividers = sorted(random.sample(range(1, total_time), total_tasks))
        sleep_time_list = [ a - b for a, b in zip(dividers + [total_time], [0] + dividers)]

        return sleep_time_list


    def task_loop(self):
        """
        Returns looped or non-looped version for tasking
        """
        autoit_looping = """
        ; this is the master loop - will got forever
        While 1
        ; this needs to grab the last shuffled sleep entry from tasks
            _ArrayShuffle($aRandTasks)
            ; clone the sleep array into this while loop
            $aRandSleepTimes = $aSleepTimes
            ; shuffle this array so it's unique everytime
            _ArrayShuffle($aRandSleepTimes)

            ; calling window cleanup
            ConsoleWrite("[*] Calling Window Cleanup" & @CRLF)
            Window_Watcher()

            ConsoleWrite("[!] Going round the loop" & @CRLF)
            For $i In $aRandTasks
                ; start with a sleep Value
                ; pops the last shuffled value from the sleep array and assigns
                Local $vSleepTime =_ArrayPop($aRandSleepTimes)
                ConsoleWrite("[!] I will now sleep for : " & $vSleepTime & @CRLF)
                ; Sets the sleep time
                Sleep($vSleepTime)
                ;ConsoleWrite($i & @CRLF)
                ; gets the current function from the shuffled array
                $curfunc = ($i & @CRLF)
                ConsoleWrite($curfunc)
                ; call the function from the shuffled array
                ; the magic call
                Call($i)
                ;Sleep($vSleepTime)

            Next
        WEnd

        """

        autoit_non_looping = """
        $aRandSleepTimes = $aSleepTimes
        ; shuffle this array so it's unique everytime
        ; it gets baked into the file
        _ArrayShuffle($aRandSleepTimes)

        For $i In $aTasks
            ; start with a sleep Value
            ; pops the last shuffled value from the sleep array and assigns
            Local $vSleepTime =_ArrayPop($aRandSleepTimes)
            ConsoleWrite("[!] I will now sleep for : " & $vSleepTime & @CRLF)
            ; Sets the sleep time
            Sleep($vSleepTime)
            ;ConsoleWrite($i & @CRLF)
            ; gets the current function from the shuffled array
            $curfunc = ($i & @CRLF)
            ConsoleWrite($curfunc)
            ; call the function from the shuffled array
            ; the magic call
            Call($i)

        Next

        """

        if self.loop == "True":
            return autoit_looping
        else:
            return autoit_non_looping


    # --------------------------------------------------->
    #   Start File Write Setup
    # --------------------------------------------------->


    def write_file(self, file_name):
        """
        Takes the time added to the object and splits this into sections
        based on the length of the total tasks
        Appends the task output to the file
        """

        print("[>] Writing to file {}".format(self.cl.red(self.file_name)))

        sleep_time_list = self.parse_time_values(self.total_time)
        print("SLEEP TIMES ARE {}".format(sleep_time_list))

        # creates the file write


        with open(file_name, 'w') as of:
            """
            Queries task list, gets the key (assigned action) and then
            writes the output to the file
            also checks taks for specific headers first so that the are at the
            top of the file
            """

            # need to always include the array library
            # as this is always used.
            #of.write('#include <Array.au3>\n')

            # Sort out no tray icon unless option is chosen
            if self.icon == "False":
                of.write("#NoTrayIcon\n")

            # add in other headers dependent on what has been assigned
            for include_header in self.autoIT_UDF_includes:
                of.write(include_header + '\n')

            # Loop through header declarations

            of.write(self.typing_speed)

            # Gets the length of the total task keys() and the values of the tasks (ie the output)
            # Grabs the total length of sleep

            task_list_output, sleep_time_output = self.autoIT_start(
                                                    len(self.tasks.keys()),
                                                    self.tasks.keys(),
                                                    len(sleep_time_list),
                                                    sleep_time_list)

            of.write(task_list_output)
            of.write(sleep_time_output)

            # write the Window Kill
            of.write(textwrap.dedent(self._window_watcher()))

            # setup the task looping - string returned by the function
            of.write(textwrap.dedent(self.task_loop()))

            # create the file
            # now loop round for output
            for task_output in self.tasks.values():
                of.write(task_output)
