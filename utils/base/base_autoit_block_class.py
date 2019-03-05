"""
Base class for AutoIT Blocks so that the core INIT functions are based.
Purely for inheritance

Allows the new AutoIT Block definition to expand the constructor

TODO Needs to expand and take in *args


"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


#######################################################################
#  Base AutoIT Block Definition
#######################################################################

class BaseAutoITBlock(object):
    """
    # Uniform Task Constructor Arguments
    : counter       > counter tracker
    : typing_block  > Typing block
    : indent_space  > Used to add indent to AutoIT code blocks
    """

    def __init__(self, counter, typing_block):

        self.counter = counter
        self.typing_block = typing_block
        self.indent_space = '  '

    