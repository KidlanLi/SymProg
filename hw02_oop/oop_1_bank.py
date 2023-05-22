"""Exercise 1: (5 points)

a) Using the slides & the script, put together a file containing the
   complete Account class.  Each method must have a documentation
   string at the beginning which describes what the method is doing.
   (1 point)

b) Create a main application where you create a number of accounts.
   Play around with depositing / withdrawing money.  Change the
   account holder of an account using a setter method.  (1 point)

c) Change the withdraw function such that the minimum balance allowed
   is -1000.  (1 point)

d) Write a function apply_interest(self) which applies an interest
   rate of 1.5% to the current balance and call it on your objects.
   (1 point)

e) Implement the __str__ magic method and use it to print accounts.
   (1 point)
"""
import re

class Account:
    """ Here has to be a documentation string that describes
    which data objects this class is designed for.
    You have to remove the pass statement and then write some
    code for the class. """

    interest_rate = 0.015  # rate of 1.5%


    # CONSTRUCTOR
    def __init__(self, num, person):
        '''Initializes an account with attributes.'''
        self.balance = 0
        self.number = num
        self.holder = person


    # METHODS
    def deposit(self, amount):
        '''Adds money to the account balance'''
        self.balance += amount


    def withdraw(self, amount):
        '''Allows to deduce money from the account until the balance reaches -1000.
        Returns the amount of money withdrawn.'''
        if self.balance - amount < -1000:
            amount = 1000 + self.balance
        self.balance -= amount
        return amount


    def apply_interest(self):
        '''Applies the interest rate to the account balance'''
        if self.balance >= 0:
            self.balance *= (1 + Account.interest_rate)


    def set_holder(self, person):
        '''setter method:
        Allows an account to change the attribute holder'''
        if (not type(person) == str):
            raise TypeError
        if not re.match("\w+( \w+)*", person.strip()):
            raise TypeError
        self.holder = person


    def __str__(self):
        '''magic method:
        Returns the description of an account'''
        res = "*** Account Info ***\n"
        res += "Account ID: " + str(self.number) + "\n"
        res += "Account holder: " + self.holder + "\n"
        res += "Balance: " + str(self.balance) + "\n"
        return res

if __name__ == "__main__":
    print("Welcome to the Python Bank!")
    print("")
    lisAccount = Account(1, "Zonggen")
    lisAccount.deposit(300)
    lisAccount.apply_interest()
    print(lisAccount)
    cash1 = lisAccount.withdraw(1500)
    print("The money " + lisAccount.holder + " gets:", cash1)
    print(lisAccount)
    zhengsAccount = Account(2, "Xiyue")
    print(zhengsAccount)
    cash2 = zhengsAccount.withdraw(500)
    print("The money " + zhengsAccount.holder + " gets:", cash2)
    zhengsAccount.apply_interest()
    zhengsAccount.set_holder("Elias")
    print(tobisAccount)
