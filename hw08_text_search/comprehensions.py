# This exercise contains 5 Tasks to practice comprehensions.
# With these, multiple-line for-loop constructions can be expressed in expressive one-liners.


def multiply_by(x, list1):
    """
    Multiplies each value in list1 by x and returns it as a new list.
    """
    return [ele * x for ele in list1]  # TODO: replace


def check_division(x, list1):
    """
    Takes a list and returns a list indicating whether or not each element in the original list can be exactly divided (without remainder) by x.
    (e.g check\_division(3, [1,2,3]) -> [False, False, True])
    """
    return [ele % x == 0 for ele in list1]  # TODO: replace


def div_less(set1):
    """
    Return a new set only containing numbers that can`t be divided by any other number (except itself and 1)
    from the original set.
    """
    return set(ele1 for ele1 in set1 if all(ele1 % ele2 != 0 for ele2 in set1 if ele2 != ele1))  # TODO: replace


def map_zip(list1, list2):
    """
    It should return a dictionary mapping the 'nth' element in list1 to the 'nth' element in list2.
    Make use of the 'zip()' function in your dictionary comprehension, that can handle lists of different sizes
    automatically.
    """
    return {ele1: ele2 for (ele1,ele2) in zip(list1, list2)}  # TODO: replace


def word_to_length(list1):
    """
    Returns a dictionary mapping all words with at least 3 characters to their number of characters.
    """
    return {word: len(word) for word in list1 if len(word) >= 3}  # TODO: replace
