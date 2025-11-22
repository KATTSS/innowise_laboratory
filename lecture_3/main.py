# Project realisation file
from csv import excel


# Class for custom exceptions
class MyException(Exception):
    pass

# Manager class for students and their grades
class GradeManager:
    # Global grade manager parameters
    max_average = 0.0
    min_average = 0.0
    overall_average = 0.0


    def __init__(self):
        self.students = []

    # Add student with empty grade list method
    def addStudent(self, name):
        if any(student['name'] == name for student in self.students):
            raise MyException("Student already exists")

        self.students.append({"name" : name, "grades" : []})

    # Add grades list to a concrete student grade list, add their average grade to statistics
    def addGrade(self, name, grade):

        if name not in self.students:
            raise MyException("Student does not exist")

        if not grade:
            raise MyException("Grade cannot be empty")

        for i, student in enumerate(self.students):
            if student['name'] == name:
                student_index = i
                break

        for i in grade:
            self.students[student_index]["grades"].append(i)
        average_grade=self.__countStudentAverage(grade)

        if average_grade>self.max_average:
            self.max_average=average_grade
        elif average_grade<self.min_average:
            self.min_average=average_grade
        self.__addToOverallAverage(average_grade)

    # Count student average grade method
    def __countStudentAverage(self, grade):
        if not grade :
            raise MyException("Grade list is empty")
        return sum(grade)/len(grade)

    # Update overall average grade method
    def __addToOverallAverage(self, grade):
        self.overall_average+=grade
        self.overall_average/=2

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
            print(f"{student['name']}'s average grade is {average}")
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