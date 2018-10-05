"""
; < ----------------------------------- >
; <          RUN Interaction
; < ----------------------------------- >


Creates the autoIT stub code to be passed into the master compile

: Takes a supplied list of commands, opens RUN,
: the master script will already define the typing speed as part of the declarations

"""

import random

class RunCommand(object):

    def __init__(self, commands, id):
        self.commands = commands
        self.id = id


    def func_dec(self):
        function_declaration = """
; < ----------------------------------- >
; <          CMD Interaction
; < ----------------------------------- >


"""
        return function_declaration


    def open_run(self, id, command):
        open_cmd = """

Func %s_RUN()
    Send("#r")
    ; Wait 10 seconds for the Run dialogue window to appear.
    WinWaitActive("Run", "", 10)
    Send("{ENTER}")

    """ %(id, command)

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
            # add in random delay between 2 seconds and 10 seconds
            command_delay = str(random.randint(2000, 10000))
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
        autoIT_script = (self.func_dec() +
        self.open_cmd(self.id) +
        self.typing_block(self.commands) +
        self.close_cmd()
        )

        return autoIT_script
