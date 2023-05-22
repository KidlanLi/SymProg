# This exercise contains 5 Tasks to practice comprehensions.
# With these, multiple-line for-loop constructions can be expressed in expressive one-liners.


def multiply_by(x, list1):
    """
    Multiplies each value in list1 by x and returns it as a new list.
    """
    return [e * x for e in list1]


def check_division(x, list1):
    """
    Takes a list and returns a list indicating whether or not each element in the original list can be divided by x.
    (e.g check\_division(3, [1,2,3]) -> [False, False, True])
    """
    return [e % x == 0 for e in list1]


def div_less(list1):
    """
    Return a new list only containing numbers that can`t be divided by any other number (except itself and 1)
    from the original list.
    """
    return {e for e in list1 if len([b for b in list1 if e % b == 0]) < 2}


def map_zip(list1, list2):
    """
    It should return a dictionary mapping the 'nth' element in list1 to the 'nth' element in list2.
    Make use of the 'zip()' function in your dictionary comprehension, that can handle lists of different sizes
    automatically.
    """
    return {e: f for e, f in zip(list1, list2)}


def word_to_length(list1):
    """
    Returns a dictionary mapping all words of the list with at least 3 characters to their number of characters.
    """
    return {e: len(e) for e in list1 if len(e) > 2}
