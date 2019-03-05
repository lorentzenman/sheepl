"""
Base class for Tasks so that the core INIT functions are based.
Purely for inheritance

Allows the new task to expand the constructor
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


#######################################################################
#  Base Task Class Definition
#######################################################################

class BaseTask:
    """
    # Uniform Task Constructor Arguments
    : interactive   > boolean value from --interactive switch 
    : counter       > counter tracker
    : csh           > Current Instantiated Sheepl Object
    : cl            > Colour Object
    : **kargs       > additional constructor keyword arguments
    """

    """
    Note about **kwds if this works
    """

    def __init__(self, interactive, counter, csh, cl, **kwds):

        # uniform variable declarations
        self.interactive = interactive
        ## look at the ID to see if this can be encapsulated into the 'csh' object
        self.counter = counter
        self.csh = csh
        self.cl = cl
        super().__init__(**kwds) 

        


        
    