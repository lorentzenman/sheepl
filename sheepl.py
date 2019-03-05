#!/usr/bin/env python3

"""
The Core Sheepl Program
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"
__version__ = "2.0"


import sys
import logging
import json
import random
import signal
import os
import argparse

# Sheepl Class Imports
from utils.tasks import Tasks
from utils.colours import ColourText
from utils.console import ConsoleContext
from utils.console import SheeplConsole
from profiles.profile import Profile
from template.template import CreateTemplate



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

------------------------------------------------
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
#  Commandline Arguments
#######################################################################


def parse_arguments():
    # Below are the core arguments
    parser = argparse.ArgumentParser(description="Creating realistic user behaviour for tradecraft emulation.")
    main_parser = parser.add_argument_group('Main Program', 'Core Program Settings')
    main_parser.add_argument("--interactive", action="store_true", default=False, help="Launches an interactive console making it easier to create complex sequences")
    main_parser.add_argument("--loop", action="store_false", help="Loops the program based around the total_time, will create actions and then repeat", default=True)
    main_parser.add_argument("--no_colour", action="store_false", help="Colours the output in the terminal <boolean> : defaults to True", default=True)
    main_parser.add_argument("--no_tray", action="store_true", help="Removes compiled script tray icon", default=False)
    
    # Profiles Options
    profile_group = parser.add_argument_group('Profiles', 'Creates Sheepl files from JSON format files')    
    profile_group.add_argument("--profile", type=argparse.FileType('r', encoding='UTF-8'), help="Specifies a profile and will import commands based on the JSON file")

    # Template Engine
    template_engine = parser.add_argument_group('Template Engine', 'Used to create a "task" template with boiler plate code and CMD module')
    template_engine.add_argument("--template", help="Name of the template")
    template_engine.add_argument("--category", help="Path category for module : all base tasks start within 'tasks' automatically")


    # counts the supplied number of arguments and prints help if they are missing
    if len(sys.argv)==1:
        #parser.print_help()
        print("[≤≥] Creating realistic user behaviour for tradecraft emulation.")
        print("[>:] Either specify a profile file path for input or use interactive mode")
        print("[>:] Example 'python3 sheepl.py --interactive' mode")
        print("[oo] See 'python3 sheepl.py -h' for full list of switches")

        # OCD line break
        print()
        sys.exit(1)
    args = parser.parse_args()

    return args


def main():
    banner("2.0")
    # hr = "------------------------------------"
    # counter below needs to be added as part of the Sheepl Object
    # this should get automatically incremented either based on the
    # length of the task list or a counter tracker
    # Main Parser Setup
    args = parse_arguments()

    # create project root
    #ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


    # assign colour output
    colour_output = args.no_colour
    print("[!] Colour output is set to : {}".format(str(colour_output).upper()))
    cl = ColourText(colour_output)
    tasks = Tasks()

    # gets global header declarations for autoIT script
    # >> Global Calls

    # manual check for Interactive
    if args.interactive:
        interactive = True
        context = ConsoleContext()
        con = SheeplConsole(context, cl, tasks)
        con.cmdloop()
        

    # Check if creating template stub file and category.
    # this should be replaced with pathlib functions
    if args.template and not args.category:
        print(cl.red("[!] You must specify a category eg 'network'"))
        print("[>] If this path does not exist, then it will be created")
      
    elif args.template:      
        if not os.path.isdir('tasks/' + args.category.lower()):
            print(cl.yellow("[!] Couldn't find this category : " + args.category.lower()))
            print(cl.green("[!] Creating {} category path now.".format(args.category.lower())))
            os.mkdir('tasks/' + args.category.lower())
        else:
            print("[>] Category already Exists : " + cl.red("tasks/" + args.category.lower()))
            os.chdir('tasks/' + args.category.lower())
            if not os.path.isfile(args.template + '.py'):
                print("[!] Creating task template: {}".format(cl.green(args.template)))
                CreateTemplate(args.template)
        
            if os.path.isfile(args.template + '.py'):
                print(cl.red("[!] Task template already exists : " + args.template))
                # spam loop until yes or no is answered
                while 1:
                    replace_template = input("[?] Do you want to replace this file? <yes> <no> : ")
                    if replace_template.lower() == "yes" or replace_template.lower() == "no":
                        break
                if replace_template.lower() == "yes":
                    print("[!] Creating new task template : " + cl.green(args.template + '.py'))
                    CreateTemplate(args.template)
                else:
                    print(cl.green("[!] Leaving orginal template intact"))

    
    # create from JSON profile
    if args.profile:
        print("[!] Create a sheepl from the profile file : {}".format(cl.green(args.profile.name)))
        # Set Interactive to False
        interactive = False
        Profile(cl, args.profile.name, tasks)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
