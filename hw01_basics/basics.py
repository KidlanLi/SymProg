"""
This exercise should (re-)introduce you to basic interactions
with Python built-in types, functions, and the format of the
exercises in this course. We'll have a look at numbers, strings,
lists, and regular expressions (=regex) in some simple exercises.

The instructions to a function are given in the comment section
within the function; the 'pass' statements are the slots that
are to be replaced with correct code.
You can do command-line test runs with this code by entering
> python3 -m doctest -v hw01_basics/basics.py <
(when you are in the src directory).


If you're stuck, try finding a solution online or ask your fellow
students. The internet is full of tips and tricks for almost every
coding problem, and the best coding uses collective brain power.

Happy coding!
"""


# ===BASICS AND NUMBERS====================================================


def hello_semester():
    """ Print the string 'Welcome to "Symbolische Programmierung" WS 22/23'.
    >>> hello_semester()
    Welcome to "Symbolische Programmierung" WS 22/23
    """
    print('Welcome to "Symbolische Programmierung" WS 22/23')


def modulo(x, y):
    """ Return the value x modulo y (i.e., do NOT print it).
    >>> modulo(5, 3)
    2
    >>> modulo(100, 24)
    4
    >>> modulo(70, 7)
    0
    """
    return x % y

def odd_number(x):
    """ Return True or False whether x is odd or not.
    >>> odd_number(15)
    True
    >>> odd_number(6)
    False
    >>> odd_number(-3)
    True
    """
    return x % 2 == 1

# ===STRING OPERATIONS====================================================

def happy_birthday(name, age):
    """ Print "Happy >age<th birthday, >name<!".
    >>> happy_birthday("Peter","17")
    Happy 17th birthday, Peter!
    """
    print("Happy " + age + "th birthday, " + name + "!")

def word_multiplier(word, n):
    """ Return a word multiplied n times.

    >>> word_multiplier("Cheese", 3)
    'CheeseCheeseCheese'
    >>> word_multiplier("Apple", 2)
    'AppleApple'
    >>> word_multiplier('Fish', 0)
    ''
    """
    return word * n

def reverse(word):
    """ Return the reverse of a word.
    >>> reverse("ABCDE")
    'EDCBA'
    >>> reverse("Info")
    'ofnI'
    >>> reverse("enoD lleW")
    'Well Done'
    >>> reverse("12345")
    '54321'
    """
    return word[::-1]

def every_nth(word, n):
    """ Return every nth letter of w word
    >>> every_nth("Ich",2)
    'Ih'
    >>> every_nth("Programmierung",5)
    'Par'
    >>> every_nth("Apfelstrudel",3)
    'Aetd'
    """
    return word[::n]

# ===LIST OPERATIONS====================================================
listOne = ["Germany", "Spain", "Italy", "Poland", "France"]
listTwo = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]
listThree = [5, 4, 8, 6]


def second_element(list_a):
    """ Return the second element of a list.
    >>> second_element(listOne)
    'Spain'
    >>> second_element(listTwo)
    2
    """
    return list_a[1]

def concatenate_lists(list_a, list_b):
    """ Return the concatenation of both lists.
    >>> concatenate_lists(listOne,listTwo)
    ['Germany', 'Spain', 'Italy', 'Poland', 'France', 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]
    >>> concatenate_lists([42,3],["Super","Duper"])
    [42, 3, 'Super', 'Duper']
    """
    return list_a + list_b

def swap_half(list_a):
    """ Swaps the first half of a list with the second half of the list.
    If the length of the list is odd, then the first half has one less element than the second half.
    >>> swap_half(["FirstHalf", "FirstHalf", "SecondHalf", "SecondHalf"])
    ['SecondHalf', 'SecondHalf', 'FirstHalf', 'FirstHalf']
    >>> swap_half(listOne)
    ['Italy', 'Poland', 'France', 'Germany', 'Spain']
    """
    return list_a[len(list_a)//2:]+list_a[:len(list_a)//2]

def replace_elements(list_a, replacement_indices, new_value):
    """ Replace the elements in list_a at the positions given in replacement_indices with new_value, and return the
    result.
    >>> replace_elements([1,2,3,4,5,6,7,8],[0,4,3],0)
    [0, 2, 3, 0, 0, 6, 7, 8]
    >>> replace_elements(listOne.copy(),[1,2,3],"North pole")
    ['Germany', 'North pole', 'North pole', 'North pole', 'France']
    """
    return list_a


def long_strings(string_list, max_length):
    """ Takes a list of strings, and returns a list of booleans. Each boolean indicates whether the length of the
     corresponding string is longer than max_length (True). If a string's length is max_length or shorter, the
     corresponding return value is false.
    >>> long_strings(listOne, 5)
    [True, False, False, True, True]
    >>> long_strings(["a", "bb", "", "ccc"], 1)
    [False, True, False, True]
    """
    return result_list

# ===LOOP OPERATIONS====================================================

def print_squares(list_a):
    """ Print the square values of each element in the list. You can use a for-loop for this problem.
    >>> print_squares(listThree)
    25
    16
    64
    36
    """
    for num in list_a:
        print(num ** 2)


def count_to_k(k):
    """ Print out the numbers counting from 0 to k, excluding k.
        If k is negative, count 'down' from 0, excluding 0.
        You can use a while-loop for this problem or the range(x,y,z) function.
    >>> count_to_k(3)
    0
    1
    2
    >>> count_to_k(-2)
    -1
    -2
    >>> count_to_k(0)
    """
    if k >= 0:
        for i in range(k):
            print(i)
    else:
        for i in range(-1, k - 1, -1):
            print(i)


# ===REGULAR EXPRESSIONS====================================================


def no_numbers(string):
    """ Return True or False whether string contains no numbers
    >>> no_numbers("Guten Tag!")
    True
    >>> no_numbers("42 ist eine tolle Zahl")
    False
    >>> no_numbers("jm584dmdk30")
    False
    >>> no_numbers("A B C D E F G H I J K L")
    True
    """
    return not any(i.isdigit() for i in string)


def contains_substring(substring, string):
    """ Return True or False whether a string contains a certain substring.
    >>> contains_substring("Apfel","Apfelkuchen")
    True
    >>> contains_substring("Apfel","APFEL")
    True
    >>> contains_substring("Sky","Skyrim")
    True
    >>> contains_substring("Gerald","The witcher")
    False
    >>> contains_substring("32","Hallo23")
    False
    >>> contains_substring("Salat","S a l a t")
    False
    """
    return substring.upper() in string.upper()

# =======================================================
