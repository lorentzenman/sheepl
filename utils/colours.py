"""
Takes text as an input, and then dependent on whether colour is on off,
wraps the text string in ANSI colour codes

>> to change the shade, modify the self.n_colour value, 
>> leave the end as 0m otherwise, all text will be that colour from invoked onwards

≤≥ New approach to defining the colours in the init is easier management
≤≥ Also leads to making sudo CSS classes based on declarative eg 
    > def warning(self, text2colour):
        ...
     
self.warning = '1;31;4m'
where the first part makes the text bold, (1), red (31) and then underlined (4m).


{oo} Ref : https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences

# bold red
redstart    = 31;0;1m
# bold grees
greenstart  = 32;0;1m
# normal yellow
yellowstart = 33;0;0m
# bold cyan blue
bluestart   = 36;0;1m

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


class ColourText(object):

    # init empty variable
    text2colour = ""

    def __init__(self, colour_output):
        self.colour_output = colour_output
        # create variables to hold colour values
        self.red_colour         = "1;31;1m"
        self.green_colour       = "0;32;1m"
        self.green_colour_ul    = "0;32;4m"
        self.yellow_colour      = "0;33;1m"
        self.blue_colour        = "0;36;1m"

    def red(self,text2colour):
        # red colour
        if self.colour_output == True:
            redstart = "\033[" + self.red_colour
            redend = "\033[0m"
            return redstart + text2colour + redend
        else:
            return text2colour


    def green(self, text2colour):
        # green colour
        if self.colour_output == True:
            greenstart = "\033[" + self.green_colour
            greenend = "\033[0m"
            return greenstart + text2colour + greenend
        else:
            return text2colour


    def green_ul(self, text2colour):
        # green colour
        if self.colour_output == True:
            greenstart = "\033[" + self.green_colour_ul
            greenend = "\033[0m"
            return greenstart + text2colour + greenend
        else:
            return text2colour


    def yellow(self, text2colour):
        # yellow colour
        if self.colour_output == True:
            yellowstart = "\033[" + self.yellow_colour
            yellowend = "\033[0m"
            return yellowstart + text2colour + yellowend
        else:
            return text2colour


    def blue(self, text2colour):
        # blue color
        if self.colour_output == True:
            bluestart = "\033[" + self.blue_colour
            blueend = "\033[0m"
            return bluestart + text2colour + blueend
        else:
            return text2colour
