"""Submodule.py is a submodule of testmodule."""

class Person:
    """Class to define Person."""

    def __init__(self, name, age): 
        """Recieve name and age.
    
        Parameters
        ----------
        name : str
            Human readable string describing the name.
        age : int
            Human readable integer.
    
        Attributes
        ----------
        msg : str
            Human readable string describing the exception.
        code : int
            Numeric error code.
    
        """
        self.name = name
        self.age = age

    def printname(self):
        """Print the name function.
    
        Returns
        -------
        name : str
            Human readable string.
            
        """
        print(self.name)


# p1 = Person("Baris", 26)
