"""
; < ----------------------------------- >
; <          CMD Interaction
; < ----------------------------------- >


Creates the autoIT stub code to be passed into the master compile

: Takes a supplied list of commands, opens CMD, types with a delay
: between 2 seconds and 20 seconds between each command
: the master script will already define the typing speed as part of the declarations

"""

import random

class CMDShell(object):

    def __init__(self, commands, id):
        self.commands = commands
        self.id = id


    def func_dec(self, id):
        function_declaration = """
; < ----------------------------------- >
; <          CMD Interaction
; < ----------------------------------- >


CMD_%s()

Func CMD_%s()
""" % (id, id)

        return function_declaration


    def open_cmd(self):
        open_cmd = """

    Send("#r")
    ; Wait 10 seconds for the Run dialogue window to appear.
    WinWaitActive("Run", "", 10)
    Send("cmd{ENTER}")
    WinWaitActive("[CLASS:ConsoleWindowClass]", "", 10)
    SendKeepActive("[CLASS:ConsoleWindowClass]")

    """

        return open_cmd



    def typing_block(self, commands):
        """
        Takes the Commands to type
        """
        typing_text = '\n'
        space = '    '
        for command in commands:
            # these are individual send commands so don't need to be
            # wrapped in a block
            typing_text += (space + 'Send("' + command + '{ENTER}")\n')
            # add in random delay between 2 seconds and 20 seconds
            command_delay = str(random.randint(2000, 20000))
            typing_text += (space + "sleep(" + command_delay + ")\n")

        # reset send focus

        return typing_text


    def close_cmd(self):
        """
        Closes the CMD appliation

        """
        end_func = """

    Send('exit{ENTER}')
    SendKeepActive("")

    EndFunc
        """

        return end_func


    def create(self):
        """ creates the autoIT script """
        autoIT_script = (self.func_dec(self.id) +
        self.open_cmd() +
        self.typing_block(self.commands) +
        self.close_cmd()
        )

        return autoIT_script
