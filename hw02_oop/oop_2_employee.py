"""Exercise 2: (5 points)

a) Write the complete code for the Employee class (including
   constructor, __str__, ...). (2 points)

b) Create a main application, create a few employee objects and show
   how you can manipulate them using the methods. (1 point)

c) Create a department dictionary (dictionary of strings to lists/sets
   of employees) with at least two departments (e.g. "accounting",
   "sales", ...) with each at least two employees. Print for each
   employee in the dictionary "<department> <employee name>".
   (2 points)

"""


class Employee:
    ''' a class representing an employee '''
    levels = {1: 'employee', 2: 'team leader', 3: 'supervisor', 4: 'manager'}
    promotion_payraise = 0.25

    # Constructor
    def __init__(self, name, gender, address, level, salary):
        '''Initializes an employee instance with attributes.'''
        self.name = name
        self.gender = gender
        self.address = address
        self.level = level
        self.salary = salary

    # Methods
    def set_address(self, address):
        '''setter method:
        Allows instances of employee to change the attribute address'''
        self.address = address

    def promotion(self):
        '''Promotes an employee to a higher job level and increases the salary accordingly. '''
        self.level += 1
        self.salary *= (1 + Employee.promotion_payraise)
        print("Congratulations, " + self.name + "! You are promoted to " + str(
            Employee.levels[self.level]) + ". Your salary is increased to " + str(self.salary) + ".")

    def __str__(self):
        '''magic method:
        Returns the description of an employee'''
        res = "*** Employee Infomation ***\n"
        res += "Name: " + self.name + "\n"
        res += "Gender: " + self.gender + "\n"
        res += "Address: " + self.address + "\n"
        res += "Level: " + str(self.level) + "\n"
        res += "Salary: " + str(self.salary) + "\n"
        return res


if __name__ == "__main__":
    print("Employee application")
    employee1 = Employee('John H. Watson', 'male', '221B Baker Street', 3, 5000)
    print(employee1)
    employee2 = Employee('Sherlock Holmes', 'male', 'London', 1, 3500)
    print(employee2)
    employee2.set_address('221 Baker Street')
    print(employee2)
    employee3 = Employee('Irene Adler', 'female', 'London', 2, 6200)
    print(employee3)
    employee3.promotion()
    print(employee3)
    employee4 = Employee('Zonggen Li', 'male', 'Tsingtauer Straße', 4, 3230)
    employee5 = Employee('Xiyue Zheng', 'female', 'Ludwigstraße', 2, 4560)
    employee6 = Employee('Zijia Shen', 'male', 'Maximilianstraße', 4, 7290)

    # create a department dictionary
    department = {'sales': [employee3, employee6], 'accounting': [employee2, employee4], 'IT': [employee1, employee5]}

    # Print all employees according to department
    print('*** Future Technology GmbH ***')
    for (dep, empList) in department.items():
        for emp in empList:
            print('<' + dep + '>', '<employee ' + emp.name + '>')
