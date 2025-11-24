# Project realisation file

# Class for custom exceptions
class MyException(Exception):
    pass

# Manager class for students and their grades
class GradeManager:

    # Global grade manager parameters
    max_average = 0.0
    min_average = float('inf')
    overall_average = 0.0

    def __init__(self):
        self.students = []

    # Add student with empty grade list method
    def addStudent(self, name):
        if any(student['name'] == name for student in self.students):
            raise MyException("Student already exists")

        self.students.append({"name" : name, "grades" : []})

    # Student's existence verification
    def verifyExistence(self, name):
        if not self.__findStudent(name):
            return False
        return True

    # Get student from the list
    def __findStudent(self, name):
        for student in self.students:
            if student['name'] == name:
                return student
        return None

    # Add grades list to a concrete student grade list, add their average grade to statistics
    def addGrade(self, name, grade):
        student = self.__findStudent(name)
        if not student:
            raise MyException("Student does not exist")

        if not grade:
            raise MyException("Grade cannot be empty")

        student["grades"].extend(grade)

        try:
            average_grade=self.__countStudentAverage(grade)
        except MyException:
            raise MyException("Grade list is empty")

        if average_grade>self.max_average:
            self.max_average=average_grade
        if average_grade<self.min_average:
            self.min_average=average_grade

        self.__updateOverallAverage()

    # Count student average grade method
    def __countStudentAverage(self, grade):
        if not grade :
            raise MyException("Grade list is empty")
        return sum(grade)/len(grade)

    # Update overall average grade method
    def __updateOverallAverage(self):
        if not self.students:
            self.overall_average = 0.0
            return

        total = 0
        count = 0
        for student in self.students:
            if student['grades']:
                total += sum(student['grades']) / len(student['grades'])
                count += 1

        self.overall_average = total / count if count > 0 else 0.0

    # Get grade manager statistics method
    def showReport(self):
        if not self.students:
            raise MyException("No students for statistics")

        print("---Student Report---")

        for student in self.students:
            try:
                average=self.__countStudentAverage(student['grades'])
            except MyException:
                print(f"{student['name']}'s average grade is N/A.")
                continue
            print(f"{student['name']}'s average grade is {round(average, 1)}")

        print("--------------------")
        print(f"Max Average: {self.max_average}")
        print(f"Min Average: {self.min_average}")
        print(f"Overall Average: {self.overall_average}")

    # Find top performer method
    def findTopPerformer(self):

        if not self.students:
            print("No students added yet.")
            return

        def get_average(student):
            grades = student['grades']
            if not grades:
                return -1
            return sum(grades) / len(grades)

        try:
            top_student = max(self.students,
                              key=lambda student: get_average(student))

            top_average = get_average(top_student)

            if top_average == -1:
                print("No students with grades available.")
            else:
                print(f"Top performer: {top_student['name']} with average grade {top_average:.2f}")

        except ValueError:
            print("No students with grades available.")


def printMenu():
    print("--- Student grade analyzer ---")
    print("1. Add a new student")
    print("2. Add grades for a student")
    print("3. Generate a full report")
    print("4. Find the top student")
    print("5. Exit program")

def getMenuOption():
    option_str=input("Enter your choice: ")
    while not option_str.isdigit() or int(option_str) not in range(1,6):
        print("Invalid input. Enter a number from 1 to 5")
        option_str = input("Enter your choice: ")
    return int(option_str)

# Get new student name from user
def getName():
    option_str=input("Enter student name: ")
    while not option_str.isalpha() or len(option_str) < 1:
        print("Invalid input. A name should consist of letters")
        option_str = input("Enter student name: ")
    return option_str.title()

# Get grades list for user
def getGrades():
    grades = []
    while True:
        option_str = input("Enter a grade (or 'done' to finish): ")
        if option_str.lower() == "done":
            return grades
        elif not option_str.isdigit() or int(option_str) not in range(1,101):
            print("Invalid input. Enter a number in range 1-100 or 'done' to finish")
            continue
        grades.append(int(option_str))

# Realisation of project main logic
def main():
    grade_manager = GradeManager()

    while True:
        printMenu()
        menu_option=getMenuOption()

        if menu_option == 1:
            name = getName()
            try:
               grade_manager.addStudent(name)
            except MyException:
                print(f"Student {name} already exists")
            except Exception:
                print("Error, please try again")

        elif menu_option == 2:
            name = getName()
            if not grade_manager.verifyExistence(name):
                print(f"No student {name} was found")
                continue
            grades_to_add = getGrades()
            try:
                grade_manager.addGrade(name, grades_to_add)
            except MyException:
                print(f"The grade list is empty or no student {name} was found")
            except Exception:
                print("Error, please try again")

        elif menu_option == 3:
            try:
                grade_manager.showReport()
            except MyException:
                print("No students added yet.")
            except Exception:
                print("Error, please try again")

        elif menu_option == 4:
            grade_manager.findTopPerformer()

        else:
            break

main()