import argparse
import sys


def parse_arguments():
    parser = argparse.ArgumentParser(description="Sheepl uses predefined behaviours to create realistic digital people.")
    main_parser = parser.add_argument_group('Main Program', 'Core Program Settings')
    main_parser.add_argument("--interactive", action="store_true", default=False, help="Launches an interactive console making it easier to create complex sequences")
    main_parser.add_argument("--total_time", help="Specify time in minutes or hours for collective time routine of events : eg '20m or 5h' : defaults to 1h", default='1h')
    main_parser.add_argument("--name", help="The name of the person (spaces will be converted to underscore)")
    #main_parser.add_argument("--role", choices=('admin', 'responder', 'user', 'attacker'), help="Specified the role of the Sherson")
    main_parser.add_argument("--type", help="Specifies the key delay for typing", default=40)
    main_parser.add_argument("--loop", action="store_false", help="Loops the program based around the total_time, will create actions and then repeat", default=True)
    main_parser.add_argument("--colour", action="store_false", help="Colours the output in the terminal", default=True)
    #main_parser.add_argument("--no-tray", action="store_true", help="Removes compiled script tray icon", default=False)
    #main_parser.add_argument("--profile", help="Specifies a profile and will import commands based on the JSON file")

    # Word
    word_choice = parser.add_argument_group('Microsoft Word Interaction', 'Specifies input and output for sheepl to create Word documents')
    #word_choice.add_argument("--word", action="append", nargs=2,
    #                        metavar=('inputtext','wordfile'),help='Create a word file')

    word_choice.add_argument("-wf", "--wordfile", help="Name and path of the Word File to save after typing text")
    word_choice.add_argument("-it", "--inputtext", help="Specify path to input text for sheepl to type ie 'letter.txt'")

    # Excel
    excel_choice = parser.add_argument_group('Microsoft Excel Interaction', 'Specifies input and output for sheepl to create Excel documents')
    excel_choice.add_argument("-ef", "--excelfile", help="Name and path of the Excel File to save after typing text")
    excel_choice.add_argument("-ic", "--inputcsv", help="Specify path to input csv for sheepl to type ie 'figures.csv'")

    # Internet Explorer
    ie_choice = parser.add_argument_group('Internet Explorer Interaction', 'Specifies URL to browse')
    ie_choice.add_argument("--ie", action="store_true", help="Internet Explorer Browsing Destination")
    ie_choice.add_argument("-u", "--url", help="URL destinations", action="append")

    # Commands
    cmd_choice = parser.add_argument_group()
    cmd_choice.add_argument("--cmd", action="store_true", help="CMD Shell")
    cmd_choice.add_argument("--cc", help="Set of commands", action="append")
    #cmd_choice.add_argument("--cf", "--command_file", help="Specify path to file containing commands one per line", type=argparse.FileType('r'))

    # Powershell
    ps_choice = parser.add_argument_group('PowerShell Interaction', 'Uses PowerShell to issue commandlets')
    ps_choice.add_argument("--powershell", action="store_true", help="Powershell Interpreter")
    ps_choice.add_argument("--pc", help="Set of commands", action='append')
    #ps_choice.add_argument("--pf", "--powershell_file", help="Specify path to file containing PowerShell commands one per line", type=argparse.FileType('r'))

    # Remote Desktop
    rdp_choice = parser.add_argument_group('Remote Desktop Interaction', 'Specifies a target computer and credentials to connect')
    rdp_choice.add_argument("--rdp", help="Remote Desktop Target")
    rdp_choice.add_argument("--rdp_user", help="Remote Desktop User")
    # TODO: argparse has a password input field
    rdp_choice.add_argument("--rdp_password", help="Remote Desktop User Password")
    #rdp_choice.add_argument("--rdp_command", "-rdpc", help="Command to type in Remote Desktop Session", action="append")
    #rdp_choice.add_argument("--rdp_command_list", help="Specify path to file containing commands one per line", type=argparse.FileType('r'))

    # counts the supplied number of arguments and prints help if they are missing
    if len(sys.argv)==1:
        #parser.print_help()
        print("[>] Quick example : ")
        print('[>] python3 sheepl.py --name Peter --total_time=2h --wordfile "c:\\users\\matt\\Desktop\\matt.doc" --inputtext "content/if.txt" --cmd --cc "ipconfig /all" --cc "whoami"')
        print("[?] For an interactive console :: sheepl.py --interactive")
        print("[?] See sheepl.py --help")
        sys.exit(1)
    args = parser.parse_args()


    return args
