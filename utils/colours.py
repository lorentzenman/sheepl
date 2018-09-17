class ColourText(object):

    text2colour = ""

    def __init__(self, colour_output):
        self.colour_output = colour_output


    def red(self,text2colour):

        if self.colour_output == True:
            redstart = "\033[0;31m"
            redend = "\033[0m"
            return redstart + text2colour + redend
        else:
            return text2colour

    def green(self, text2colour):

        if self.colour_output == True:
            greenstart = "\033[0;32m"
            greenend = "\033[0m"
            return greenstart + text2colour + greenend
        else:
            return text2colour

    def yellow(self, text2colour):

        if self.colour_output == True:
            yellowstart = "\033[0;33m"
            yellowend = "\033[0m"
            return yellowstart + text2colour + yellowend
        else:
            return text2colour

    def blue(self, text2colour):

        if self.colour_output == True:
            bluestart = "\033[0;34m"
            blueend = "\033[0m"
            return bluestart + text2colour + blueend
        else:
            return text2colour
