"""A public module."""

def echo():
    """Echo the input.
    
    Returns
    -------
    Prompt with typed input.
    
    """
    num = int(input("Enter a number: "))
    return print(num, " ", type(num))
