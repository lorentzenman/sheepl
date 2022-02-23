"""
Class to create a counter object and allow this to be incremented
As this is an object, it can be instantiated in the Sheepl Object
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


class Counter(object):
    """
    __init__ declares a counter object at 0
    """

    def __init__(self):
        """
        Start the counter at 0
        """
        self.counter = 0


    def increment(self):
        """
        Increments the counter object
        """
        self.counter += 1
        return self.counter


    def current(self):
        """
        Prints the current counter value
        """
        return str(self.counter)


    
