def string_to_floats(string, delimiter=","):
    """Convert a string of delimiter-separated floats into a list of floats."""

    floats = string.split(delimiter)
    return [float(num) for num in floats]
