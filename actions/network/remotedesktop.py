"""
; < ----------------------------------- >
; <      Remote Desktop Interaction
; < ----------------------------------- >

Creates the autoIT stub code to be passed into the master compile

: Calls MSTSC via run command, and then proceeds to send commands
: replicating Admin logging into RDP

"""
import random


class RDPConnection(object):

    def __init__(self, computer, username, password, id):
        self.computer = computer
        self.username = username
        self.password = password
        self.id = id


    def func_dec(self):
        function_declaration = """

; < ----------------------------------- >
; <      Remote Desktop Interaction
; < ----------------------------------- >

"""
        return function_declaration

    def open_rdp(self, computer, username, password, id):
        open_rdp = """

Func RDP_%s()
    Send("#r")
    ; Wait 10 seconds for the Run dialogue window to appear.
    WinWait("Run", "", 10)
    Send("mstsc{ENTER}")
    WinWaitActive("Remote Destop Connection", "", 10)
    ;SendKeepActive("[CLASS:OpusApp]") get the name of this class
    ; Send ALT 'o' to open the RDP options
    Send("!o")
    Sleep(2000)
    ;Send ALT 'c' to focus to computer
    Send("!c")
    Sleep(2000)
    """ %(id)

        rdp_computer = 'Send("' + computer + '{TAB}")\nSleep(2000)\n'
        rdp_username = 'Send("' + username + '{ENTER}")\nSleep(2000)\n'
        rdp_password = 'Send("' + password + '{ENTER}")\nSleep(30000)\n'
        rdp_trustprompt = 'Send("!y")\n'

        return open_rdp + rdp_computer + rdp_username + rdp_password + rdp_trustprompt



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
            command_delay = str(random.randint(2000, 10000))
            typing_text += (space + "sleep(" + command_delay + ")\n")

        return typing_text


    def close_rdp(self):
        """
        Closes the RDP connection
        """
        end_func = """

    SendKeepActive("")

    EndFunc
        """
        return end_func


    def create(self):
        """ creates the master RDP solution """

        autoIT_script = (self.func_dec() +
        self.open_rdp(self.computer, self.username, self.password, self.id) +
        self.close_rdp()
        )
        # self.typing_block(self.input_text) +
        # self.save_file(self.save_name))
        #
        return autoIT_script
