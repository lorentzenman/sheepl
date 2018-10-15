"""
; < ----------------------------------- >
; <       Internet Interaction
; < ----------------------------------- >

"""

class IEBrowser(object):

    def __init__(self, destination_url, id):
        self.destination_url = destination_url
        self.id = id


    def func_dec(self):
        # this overides the function in the parent class
        function_declaration = """
; < ----------------------------------- >
; <          IE Interaction
; < ----------------------------------- >

"""
        return function_declaration


    def url(self, id, destination_url):
        url = """

Func IE_%s()

    Local $oIE = _IECreate("%s",1,1,1)
    Sleep(2000)
    WinWaitActive("Windows Internet Explorer")
    SendKeepActive("Windows Internet Explorer")
    WinSetState("Windows Internet Explorer","",@SW_MAXIMIZE)
    ; hardcoded sleep for now
    ; will convert to AutoIT random
    ; this is also where the IE interaction such as logging in etc will happen,
    ; spawning new tabs etc
    ; prob need a call out function to trigger a subroutine
    Sleep(10000)

        """ % (id, destination_url)
        return url


    def close_cmd(self):
        """
        Closes the IE appliation

        """
        end_func = """

    SendKeepActive("")
    _IEQuit($oIE)

    EndFunc
        """

        return end_func


    def create(self):
        """ creates the autoIT script """
        autoIT_script = (self.func_dec() +
        self.url(self.id, self.destination_url) +
        self.close_cmd()
        )

        return autoIT_script
