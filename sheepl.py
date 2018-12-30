#!/usr/bin/env python3

import sys
import logging
import time
import random
import signal
#import xml.etree.ElementTree as etree

# Sheepl specific modules
from utils.args import parse_arguments
from utils.colours import ColourText


def banner(version):
    banner = """

███████╗██╗  ██╗███████╗███████╗██████╗ ██╗
██╔════╝██║  ██║██╔════╝██╔════╝██╔══██╗██║
███████╗███████║█████╗  █████╗  ██████╔╝██║
╚════██║██╔══██║██╔══╝  ██╔══╝  ██╔═══╝ ██║
███████║██║  ██║███████╗███████╗██║     ███████╗
╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚══════╝

version : %s
author  : @lorentzenman
team    : SpiderLabs

               /\___
    @@@@@@@@@@@  O  \\
 @@@@@@@@@@@@@@@____/--[ baaverlous ]
 @@@@@@@@@@@@@@@
    ||      ||
    ~~      ~~
[<] ------------------------------------------ [>]
    """ %version

    print(banner)


def signal_handler(sig, frame):
    """
    Catches Control + C
    """
    print("[!] You pressed Ctrl+C")
    print("[!] Exiting Sheepl")
    print("[<] ------------------------------------------ [>]")
    print("""
               /\___
    @@@@@@@@@@@  O  \\
 @@@@@@@@@@@@@@@____/--[ later ]
 @@@@@@@@@@@@@@@
    ||      ||
    ~~      ~~
---------------------------------------------
        """)
    sys.exit(0)



#######################################################################
#   Sheepl Class
#######################################################################

class Sheepl(object):
    """
    Creates a digital person and is ready to type the commands
    """
    tasks = {}
    #headers = .action_headers()


    def __init__(self, name, total_time, type, cl, loop):

        self.name = name
        self.total_time = total_time
        self.type = type
        self.cl = cl
        self.loop = loop

        #print("[*] Creating file : {}.au3".format(name.lower()))
        #file_name = name.lower() + '.au3'
        self.typing_speed = self.type_speed(type)


    def say_hello(self):
        """
        Grabs stupid hobbies from the lists
        """
        print(self.cl.yellow("[~] Hello, my name is {}".format(self.name)))
        h1, h2 = self.hobbies()
        print(self.cl.yellow("[~] I like {} and {}.".format(h1, h2)))


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

        tea_break = """
; < ----------------------------------- >
; <             Tea Break
; < ----------------------------------- >

; Nothing to do here but have a cuppa, it's a placeholder for a tea break
; creates an entry in the task list to then take a random slice of the
; timeslot which results in a random sleep action
        """

        return tea_break


    def type_speed(self, speed):
        """
        Global Typing Speed
        """
        #speed = '60'
        typing_speed = 'Opt("SendKeyDelay", {})\n'.format(speed)
        print("[^] Global Typing Speed set to : {}".format(speed) + 'ms delay')

        return typing_speed


    def add_task(self, task, output):
        """
        Add a task to the dictionary
        """
        self.tasks[task] = output
#> # DEBUG:
        #print(self.tasks)


    def list_tasks(self):
        """
        Prints the task list to the console
        """
        print(self.cl.green("[!] There are {} tasks in total".format(len(self.tasks.keys()))))
        for task, output in self.tasks.items():
            print("[>] The person will create {}".format(task))
            print("----> The output will be {}".format(output))


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

        task_list_output = """
; define global task list
Global $aTasks[{}] = {} """.format(total_tasks, ([t for t in task_names]))

        sleep_time_output = """
; creates Sleep Times array
Global $aSleepTimes[{}] = {}
; copies original array just encase the task list borks
$aRandTasks = $aTasks
        """.format(sleep_list_length, ([str(s) for s in sleep_time_list]))

        return task_list_output, sleep_time_output



    def write_file(self, file_name):
        """
        Takes the time added to the object and splits this into sections
        based on the length of the total tasks
        Appends the task output to the file
        """
        print("[>] Writing to file {}".format(self.cl.red(file_name)))
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

        dividers = sorted(random.sample(range(1, total_time), total_tasks - 1))
        sleep_time_list = [ a - b for a, b in zip(dividers + [total_time], [0] + dividers)]

        print("SLEEP TIMES ARE {}".format(sleep_time_list))


        with open(file_name, 'a') as of:
            """
            Queries task list, gets the key (assigned action) and then
            writes the output to the file
            also checks taks for specific headers first so that the are at the
            top of the file
            """
            # first loop for headers and writing typing speed
            #print("My typing speed is {}".format(typing_speed))
            #of.write(typing_speed)
            # for task in self.tasks.keys():
            #     print("[>] The tasks assigned to {} are : {}".format(self.name, task))
            #     # TODO get this from the headers dict so that this doesn't
            #     # need to be if'd
            #     if task == "word":
            #         # should be part of the word object
            #         of.write('#include <Word.au3>\n')

            of.write('#include <Word.au3>\n')
            of.write('#include <IE.au3>\n')
            of.write('#include <Array.au3>\n')
            of.write(self.typing_speed)


            task_list_output, sleep_time_output = self.autoIT_start(
                                                    total_tasks,
                                                    self.tasks.keys(),
                                                    len(sleep_time_list),
                                                    sleep_time_list)

            of.write(task_list_output)
            of.write(sleep_time_output)

            if self.loop == True:
                of.write("""
; this is the loop that works if they have loop switch in sheepl set
; this is the master loop - will got forever
While 1
   ; this needs to grab the last shuffled sleep entry from tasks
    _ArrayShuffle($aRandTasks)
	; clone the sleep array into this while loop
	$aRandSleepTimes = $aSleepTimes
	; shuffle this array so it's unique everytime
	_ArrayShuffle($aRandSleepTimes)

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

   Next

WEnd
""")


            else:
                of.write("""
	$aRandSleepTimes = $aSleepTimes
	; shuffle this array so it's unique everytime
	; it gets baked into the file
	_ArrayShuffle($aRandSleepTimes)

   ConsoleWrite("[!] Going round the loop" & @CRLF)
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

""")


            # now loop round for output
            for task_output in self.tasks.values():
                of.write(task_output)
                # now grab random sleep time from chopped up total task time
    #             sleep_time = sleep_time_list.pop()
    #             of.write("""
    # ; -------------------------------------------->
    # ; {} will now sleep for {} seconds
    #
    # sleep({})
    #
    # ; -------------------------------------------->
    #
    #         """.format(self.name, str(sleep_time / 1000), str(sleep_time)))


#######################################################################
#   Console Class
#######################################################################

class SheeplConsole(object):
    """
    Creates a person object
    """

    def __init__(self, cl):
        task_list = self.available_tasks()
        self.cl = cl
        self.menu(cl)
        self.task_list = task_list
        # call the launch console option
        self.launch_console(task_list, cl)


    def menu(self, cl):
#    """ Prints the main menu """
        console_banner = """
Sheepl Interactive Console
---------------------------------------------- [>]
[!] type 'help' or '?' for command list
"""

        print(cl.green(console_banner))


    def console_help(self):
        """ Console help functions """

        console_help_menu = """
> help or ?             : Prints this help menu
> create                : Creates a person
> list                  : Lists avaliable tasks
> exit or quit          : exit the console

"""
        print(console_help_menu)

    # stack overflow check ---- reference path
    def check_input(self, prompt, type_=None, min_=None, max_=None, range_=None):
        """
        Check the input value againt the expected type
        this will be either a string, an int, or a path
        """
        if min_ is not None and max_ is not None and max_ < min_:
            raise ValueError("min_ must be less than or equal to max_.")
        while True:
            ui = input(prompt)
            if type_ is not None:
                try:
                    ui = type_(ui)
                except ValueError:
                    print("Input type must be {0}.".format(type_.__name__))
                    continue
            if max_ is not None and ui > max_:
                print("Input must be less than or equal to {0}.".format(max_))
            elif min_ is not None and ui < min_:
                print("Input must be greater than or equal to {0}.".format(min_))
            elif range_ is not None and ui not in range_:
                if isinstance(range_, range):
                    template = "Input must be between {0.start} and {0.stop}."
                    print(template.format(range_))
                else:
                    template = "Input must be {0}."
                    if len(range_) == 1:
                        print(template.format(*range_))
                    else:
                        print(template.format(" or ".join((", ".join(map(str, range_[:-1])), str(range_[-1])))))
            else:
                return ui


    def path_input(self, prompt, type_=None):
          while True:
              ui = input(prompt)
              if type_ is not None:
                  try:
                      ui = type_(ui)
                  except ValueError:
                      print("Input type must be {0}.".format(type_.__name__))
                      continue

              else:
                  return ui


    def available_tasks(self):
        available_tasks_list = {
          'word'        : 'Create a Word File',
          'excel'       : 'Create an Excel Spreadsheet',
          'cmd'         : 'Interact with CMD Shell',
          'powershell'  : 'Interact with PowerShell',
          'rdp'         : 'Authenticate using RDP',
          'ie'          : 'Browse to a URL using Internet Explorer',
          'teabreak'    : "Grab a cuppa (random sleep time)",
        }

        return available_tasks_list


    def quit_program(self):
        """
        Exits the program
        """
        print("[<] ------------------------------------------ [>]")
        print("""                       /\___
            @@@@@@@@@@@  O  \\
         @@@@@@@@@@@@@@@____/--[ later ]
         @@@@@@@@@@@@@@@
            ||      ||
            ~~      ~~
        ---------------------------------------------
            """)
        print("[!] >>>           {}           <<< [!]".format(self.cl.red("Exiting Sheepl")))
        print("[<] ------------------------------------------ [>]")
        sys.exit(0)


    def check_add_more_tasks(self, cl):
        """
        quick helper to stop having to retype the same question
        """
        add_more_tasks = self.check_input(cl.green("Do you want to add another task? <yes> <no> "), str.lower, range_=('yes', 'no'))

        return add_more_tasks


    def check_add_more_commands(self, cl):
        """
        checks to see if more commands are required
        """
        add_more_commands = self.check_input(cl.green("Do you want to add another command? <enter> <no> "), str.lower, range_=(['', 'yes', 'no']))

        return add_more_commands


    def check_add_rdp_commands(self, cl):
        """
        checks to see if commands are required in the RDP session
        """
        send_to_rdp = self.check_input(cl.green("Do you want to issue commands to RDP? <yes> <no> "), str.lower, range_=(['yes', 'no']))

        return send_to_rdp


    def finished_task(self, csh, file_name, cl):
        """
        Sets the user creation to finished, writes the file and breaks loop
        """
        print("[:] Successfully created a person called {}".format(cl.green(csh.name)))
        print("[:] File has been saved as {}".format(cl.green(file_name)))
        finished = True
        csh.write_file(file_name)
        return finished


    def launch_console(self, task_list, cl):
        """
        Calls the initial console function
        """
        #output = None
        # ---- [ Console Loop ] ---- #
        # id_tracker
        id = 0
        hr_line = "---------------------------------------------- [>]"
        while True:
            print(hr_line)
            #self.console_help()
            # console input
            command = input(cl.green("#> "))
            # help function
            if command.startswith("help") or command.startswith("?"):
                self.console_help()

            elif command.startswith("exit") or command.startswith("quit"):
                self.quit_program()

            elif command.startswith("list"):
                print(cl.blue("[!] The following tasks are available : "))
                print(cl.yellow("[?] Assign these commands inside <create>\n"))
                for task, desc in task_list.items():
                    print("[>] [ {} ] :: {}".format(cl.green(task), desc))
                # add an empty line space
                print()

            elif command.startswith("create"):
                print(cl.yellow("OK, Let's create some sheepl"))
                name = input("#> Enter the sheps name : ")

                # check the input for spacing
                print("[?] How long would you like {} to take to complete tasks?".format(cl.green(name)))


                total_time = input("#> Enter the time (e.g. 45m or 6h) : ")
                # if not total_time.endswith("m") or not total_time.endswith("h"):
                #     print(cl.red("[!] You need to supply correct format"))
                #     print(cl.yellow("[?] needs to end in 'm' for minutes or 'h' for hours"))
                #     # bit dirty calling the input again but my while loops sucked - will fix
                #     total_time = input("#> Enter the time (e.g. 45m or 6h) : ")


                print("[?] How fast can {} type? <default is 40ms between key>".format(cl.green(name)))
                typing_speed = input("#> Enter the typing speed <40> : ")
                if len(typing_speed) == 0:
                    typing_speed = 40

                print(cl.yellow("Typing speed is {}".format(typing_speed)))

                loop_question = self.check_input(cl.green("[~] Do you want the tasks to loop? <yes> or <no> : "), str.lower, range_=('yes', 'no'))

                if loop_question == "yes":
                    loop = True
                else:
                    loop = False

                # Create Sheepl Object
                # this should just be a call and all this stuff should be inside init...then it
                # can be called with csh.
                csh = Sheepl(name, total_time, typing_speed, cl, loop)
                name = name.replace(' ', '_')
                print("[*] Creating file : {}.au3".format(name.lower()))
                file_name = name.lower() + '.au3'

                # Introduce them
                print("\n")
                csh.say_hello()
                print("\n")

                # adding first task as a tea break to create a random initial sleep_time
                # need to review this now as based on a shuffled array list,
                csh.add_task(str(id) + '_Teabreak', csh.tea_break_task())

                #####################################
                #  BEGIN Console
                #####################################

                print(cl.green("[!] Now choose some tasks for me from the list\n"))
                finished_user = False
                while finished_user != True:

                    with open(file_name, 'a') as of:

                        #############################################
                        ##  Check if a XML task file is used
                        #############################################
                        #
                        # load_task_file = self.check_input(cl.green("Do you want to load a tasks file? <yes> <no> "), str.lower, range_=('yes', 'no'))
                        # if load_task_file == "yes":
                        #     inputfile = input("[>] Enter the path to XML file")
                        #     print(cl.yellow("[*] Loading XML task file : {}".format(cl.red(inputfile)))
                        #     # now parse the input file
                        #     tree = etree.parse(inputfile)
                        #     root = tree.getroot()
                        #     for child in root:
                        #         print(child)

                        #############################################
                        ##  Interactive console mode
                        #############################################


                        # list all the current tasks
                        for task, desc in task_list.items():
                            print("[ {} ] :: {}".format(task, desc))
                        task = input(cl.green("[>] Enter a task: "))

                        if task not in task_list.keys():
                            print(cl.red("[!] I'm afraid I don't know that task, write it and teach me please"))
                            continue


                        #############################################
                        ##  Tea Break
                        #############################################

                        if task == 'teabreak':
                            # creates random sleep time slice
                            csh.add_task('TeaBreak_' + str(id), csh.tea_break_task())
                            id += 1
                            if self.check_add_more_tasks(cl) == 'yes':
                                continue
                            else:
                                self.finished_task(csh, file_name, cl)
                                break


                        #############################################
                        ##  Word
                        #############################################

                        if task == 'word':
                            # create word object
                            # all these questions could be placed into the init of the word document
                            input_file = input("Enter the input file : ")
                            print("[?] Now specify the output path and the Word filename e.g. 'c:\\users\\matt\\Desktop\\path.docx'")
                            output_file = input("Enter the output file : ")
                            # import the action
                            from actions.office.word import WordDocument

                            word_file = WordDocument(input_file, output_file, str(id))
                            csh.add_task('Word_' + str(id), word_file.create())
                            #of.write(word_file.create())
                            id += 1
                            if self.check_add_more_tasks(cl) == 'yes':
                                continue
                            else:
                                self.finished_task(csh, file_name, cl)
                                break

                        #############################################
                        ##  CMD
                        #############################################

                        if task == 'cmd':
                            # create list to hold commands
                            from actions.shell.cmd import CMDShell
                            commands = []
                            print(cl.yellow("[!] - Command Shell Interaction"))
                            add_commands = True
                            while add_commands:
                                command = input("[>] Enter the command to be executed > ")
                                commands.append(command)
                                if self.check_add_more_commands(cl) == 'no':
                                    add_commands = False
                                    break

                            cmd_shell = CMDShell(commands, str(id))
                            csh.add_task('CMD_' + str(id), cmd_shell.create())
                            for command in commands:
                                print('[-] - {} will type "{}" into the remote session'.format(cl.green("'" + csh.name + "'"), command))

                            id += 1

                            if self.check_add_more_tasks(cl) == 'yes':
                                continue
                            else:
                                self.finished_task(csh, file_name, cl)
                                break

                        #############################################
                        ##  PowerShell
                        #############################################

                        if task == 'powershell':
                            # create list to hold commands
                            from actions.shell.powershell import PowerShell
                            commands = []
                            print(cl.blue("[!] - PowerShell Interaction"))
                            add_commands = True
                            while add_commands:
                                command = input("Enter the command to be executed > ")
                                commands.append(command)
                                add_more_commands = self.check_input(cl.yellow("Do you want to add another command? {[enter] for yes or type 'no'} "), str.lower, range_=('', 'no'))
                                if add_more_commands == 'no':
                                    add_commands = False
                                    break

                            powershell = PowerShell(commands, str(id))
                            csh.add_task('Powershell_' + str(id), powershell.create())
                            #of.write(cmd_shell.create())
                            for command in commands:
                                print('[-] - They will type "{}" into the remote session'.format(command))

                            id += 1
                            if self.check_add_more_tasks(cl) == 'yes':
                                continue
                            else:
                                self.finished_task(csh, file_name, cl)
                                break

                        #############################################
                        ##  RDP
                        #############################################
                        if task == 'rdp':
                            from actions.network.remotedesktop import RDPConnection
                            print(cl.yellow("[!] - Remote Desktop Interaction"))
                            rdp = input("[!] Enter the target IP address > ")
                            rdp_user = input("[!] Enter the target User account e.g DOMAIN\\user > ")
                            rdp_password = input("[!] Enter the RDP password > ")

                            #current support is restricted to powershell, run and cmd atm
                            #need to port to easier way of returning the task object


                            # if self.check_add_rdp_commands(cl) == 'yes':
                            #     commands = []
                            #     print("[?] Ok. Currently <cmd> <powershell> and <run> are supported ")
                            #     task_command = input("Enter the task to be executed > ")
                            #     if task_command == 'cmd':
                            #         from actions.shell.cmd import CMDShell
                            #         commands = []
                            #         print(cl.yellow("[!] - Command Shell Interaction"))
                            #         add_commands = True
                            #         while add_commands:
                            #             command = input("[>] Enter the command to be executed > ")
                            #             commands.append(command)
                            #             if self.check_add_more_commands(cl) == 'no':
                            #                 add_commands = False
                            #                 break
                            #
                            # else:
                            #     commands = []

                            rdp_conn = RDPConnection(rdp , rdp_user , rdp_password, str(id))
                            csh.add_task('RDP_' + str(id), rdp_conn.create())
                            id += 1
                            if self.check_add_more_tasks(cl) == 'yes':
                                continue
                            else:
                                self.finished_task(csh, file_name, cl)
                                break

                        #############################################
                        ##  Internet Explorer
                        #############################################
                        if task == 'ie':
                            # create list to hold commands
                            from actions.browsing.ie import IEBrowser
                            id += 1
                            print(cl.yellow("[!] - Internet Explorer Interaction"))
                            command = input("[>] Enter the URL destination to be browsed > ")

                            ie = IEBrowser(command, str(id))
                            csh.add_task('IE_' + str(id), ie.create())
                            print('[-] - {} will browse to "{}" using Internet Explorer'.format(cl.green("'" + csh.name + "'"), command))


                            if self.check_add_more_tasks(cl) == 'yes':
                                continue
                            else:
                                self.finished_task(csh, file_name, cl)
                                break


                        #############################################
                        ##  MENU
                        #############################################
                        if task == 'menu':
                            print(cl.red("[!] Ok, I'm out."))
                            print("[!] Returning to the main menu.")
                            self.console_help()
                            #finished = True

            # unknown commands
            else:
                for task, desc in task_list.items():
                    if command == task:
                        print(cl.red("[!] You need to run tasks after running create"))
                print("[!] Unknown command - run help")





def main():
    banner("0.1")
    hr = "------------------------------------"
    # counter below needs to be added as part of the Sheepl Object
    # this should get automatically incremented either based on the
    # length of the task list or a counter tracker
    id = 1
    # Main Parser Setup
    args = parse_arguments()
#>> DEBUG
#    print(args)

    # assign colour output
    colour_output = args.colour
    print("[!] Colour output is set to : {}".format(str(colour_output).upper()))
    cl = ColourText(colour_output)

    # gets global header declarations for autoIT script
    # >> Global Calls

    # manual check for Name
    if not args.name and args.interactive:
        interactive = True
        console = SheeplConsole(cl)
    elif not args.name:
        print(cl.red("[!] You need to give this Sherson a name (--name <NAME>) - bah"))
        sys.exit(0)


    ## TODO: this needs to be pushed into a class from below to make S
    # Sheepl
    print("[:] - Creating the person called > {}".format(cl.green(args.name)))

    # first check for spaces
    file_name = args.name.replace(' ', '_').lower() + '.au3'
    # ------->
    # Parse time
    # goes through supplied arguments and creates tasks
    csh = Sheepl(args.name, args.total_time, args.type, cl, args.loop)
    csh.say_hello()

    # add the tea break task
    csh.add_task("tea_break", csh.tea_break_task())


    #############################################
    ##  Word
    #############################################

    if args.wordfile:
        from actions.office.word import WordDocument
        id += 1
        print("[!] - Word Interaction")
        print('[-] - Word output file is "{}" and user will type contents of "{}"'.format(args.wordfile, args.inputtext))
        word_file = WordDocument(args.inputtext , args.wordfile, str(id))
        csh.add_task('Word_' + str(id), word_file.create())


    #############################################
    ##  Excel
    #############################################

    # if args.wordfile:
    #     print("[!] - Excel Interaction")
    #     print("[!] - Adding Excel Header")
    #     print('[-] - Excel output file is "{}" and user will type contents of "{}"'.format(args.excelfile, args.inputcsv))
    #     # import word module
    #     from actions.office import excel
    #     # # TODO: get this from Headers
    #     # header = add_header('word', headers)
    #     # of.write(header + '\n')
    #     of.write('#include <Excel.au3>\n')
    #     of.write(excel.create_new_document())
    #     with open(args.inputtext) as st:
    #         poem = st.read()
    #         of.write(word.typing_block(poem) + '\n')
    #         of.write(word.save_file(args.wordfile))
    #     # # TODO: this will come from time variable based on some counting of some args
    #     # this will determine the wait time until the next the command
    #     # # TODO: break this out into a master function that decrements some cound and randomly
    #     # distributest the remaining time in milliseconds
    #     of.write('sleep(3000)' + '\n')


    #############################################
    ##  PowerShell
    #############################################

    if args.powershell:
        from actions.shell.powershell import PowerShell
        id += 1
        print(cl.green("[!] - Powershell Interaction"))
        print("[^] - Issuing the following powershell commands")
        ps_shell = PowerShell(args.pc, str(id))
        csh.add_task('Powershell_' + str(id), ps_shell.create())
        for command in args.pc:
            print('[-] - They will type "{}" into the PowerShell prompt'.format(command))


    #############################################
    ##  CMD
    #############################################

    if args.cmd:
        from actions.shell.cmd import CMDShell
        id += 1
        print(cl.green("[!] - Command Shell Interaction"))
        print("[!] - Issuing the following cmd commands")
        cmd_shell = CMDShell(args.cc, str(id))
        csh.add_task('CMD_' + str(id), cmd_shell.create())
        for command in args.cc:
            print('[-] - They will type "{}" into the CMD Shell'.format(command))


    #############################################
    ##  Internet Explorer
    #############################################

    if args.ie:
        from actions.browsing.ie import IEBrowser
        id += 1
        print(cl.green("[!] - Internet Explorer Interaction"))
        ie = IEBrowser(args.url, str(id))
        csh.add_task('IE_' + str(id), ie.create())
        print('[-] - They will browse to "{}" using Internet Explorer'.format(args.url))


    #############################################
    ##  RDP
    #############################################

    if args.rdp:
        from actions.network.remotedesktop import RDPConnection
        id += 1
        print(cl.green("[!] - Remote Desktop Interaction"))
        print(hr)
        print('[-] - The user "{}" will create a Remote Desktop Connection to "{}"'.format(args.rdp_user, args.rdp))
        if args.rdp_command:
            for command in args.rdp_command:
                print('[-] - They will type "{}" into the remote session'.format(command))
        rdp_conn = RDPConnection(args.rdp , args.rdp_user , args.rdp_password, str(id))
        csh.add_task('RDP_' + str(id), rdp_conn.create())


    #############################################
    ##  WRITE FILE
    #############################################

    print("[*] - Writing output file > {}\n".format(file_name))
    print(hr)
    csh.write_file(file_name)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
