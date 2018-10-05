"""
Creates the autoIT stub code to be passed into the master compile

: Calls PowerShell via run command, and then proceeds to send commands - replicating Admin

"""
import random

class PowerShell(object):

    def __init__(self, commands, id):
        self.commands = commands
        self.id = id


    def func_dec(self):
        function_declaration = """
    ; < ----------------------------------- >
    ; <       PowerShell Interaction
    ; < ----------------------------------- >

    """
        return function_declaration


    def open_powershell(self, id):
        open_powershell = """

Func PowerShell_%s()
        Send("#r")
        ; Wait 10 seconds for the Run dialogue window to appear.
        WinWaitActive("Run", "", 10)
        Send("powershell{ENTER}")
        WinWaitActive("Windows PowerShell", "", 10)
        SendKeepActive("Windows PowerShell")

        """  %(id)

        return open_powershell


    def typing_block(self, commands):
        """
        Takes the Commands to type
        """
        typing_text = '\n'
        space = '    '
        for command in commands:
            # these are individual send commands so don't need to be
            # wrapped in a block
            # check to see if the command is an object pipeline command
            if ("{" in command or "?" in command or "$_" in command or "|" in command):
                # send in the raw keystroke option
                 typing_text += (space + 'Send("' + command + '", 1)\n')
                 typing_text += (space + 'Send("{ENTER}")\n')
            else:
                 typing_text += (space + 'Send("' + command + '{ENTER}")\n')
            # add in random delay between 2 seconds and 2 minutes
            command_delay = str(random.randint(2000, 12000))
            typing_text += (space + "sleep(" + command_delay + ")\n")

        # reset send focus

        return typing_text


    def close_powershell(self):
        """ exit powershell """

        close_powershell = """
        sleep(2000)
        Send("exit{ENTER}")
        EndFunc

        """
        return close_powershell


    def create(self):
        """ creates the autoIT script """
        autoIT_script = (self.func_dec() +
        self.open_powershell(self.id) +
        self.typing_block(self.commands) +
        self.close_powershell()
        )

        return autoIT_script
