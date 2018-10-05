"""
; < ----------------------------------- >
; <         Word Interaction
; < ----------------------------------- >

Creates the autoIT stub code to be passed into the master compile

: Takes a supplied text file for the peep to type
: the master script will already define the typing speed as part of the master declarations

## TODO: add in more logic to text parsing, ie if there is a comma, add a space
        more human type interaction with the odd backspace for typos etc at random places

        wrap this in a function

"""

class WordDocument(object):

    def __init__(self, input_text, save_name, id):
        self.input_text = input_text
        self.save_name = save_name
        self.id = id


    def func_dec(self):
        # this overides the function in the parent class
        function_declaration = """
; < ----------------------------------- >
; <         Word Interaction
; < ----------------------------------- >

"""
        return function_declaration


    def new_document(self, id):
        new_document = """

Func Word_{}()

    Local $oWord = _Word_Create()

    ; Add a new empty document
    $oDoc = _Word_DocAdd($oWord)

    WinActivate("[CLASS:OpusApp]")
    WinWaitActive("[CLASS:OpusApp]")
    SendKeepActive("[CLASS:OpusApp]")

        """.format(id)
        return new_document


    def typing_block(self, input_text):
        """
        Takes the Typing Text Input
        """
        # first read the input text
        with open(input_text) as it:
            it = it.read()
        space = '    '
        typing_text = '\n' + space + 'Send("'
        # now loop round the input_text
        # some funkyness here to treat the carriage returns in the file as enter commands
        # represents how someone would use the enter key when typing

        for l in it.splitlines():
            # check if this is an empty line -> ie an enter key
            if (len(l) == 0):
                typing_text += ("{ENTER}")
            else:
                typing_text += (l)
            # close off the Send
        typing_text += ('")')

        return typing_text


    def save_file(self, save_name):
        """
        Saves the file where it is specified including any path
        """

        if not save_name.endswith(".docx"):
            save_name = save_name + ".docx"

            #    command_save_file = '_Word_DocSaveAs($oDoc, @TempDir & "\_{}")'.format(save_name)
        command_save_file = """
    ; Reset the SendKeep Active
    SendKeepActive("")
    ; now save
    _Word_DocSaveAs($oDoc,'{}', $WdFormatDocumentDefault)
    _Word_DocClose($oDoc)

        """.format(save_name)

        return command_save_file


    def close_word(self):
        """
        Closes the word appliation
        """
        end_func = """

    EndFunc

        """
        return end_func



    def create(self):
        """ creates the master word solution """
        #print(self.func_dec(self.id))
        #print(self.new_document(self.id))
        #print(self.typing_block(self.input_text))
        #print(self.save_file(self.save_name))
        autoIT_script = (self.func_dec() +
        self.new_document(self.id) +
        self.typing_block(self.input_text) +
        self.save_file(self.save_name) +
        self.close_word()
        )
        #
        return autoIT_script
