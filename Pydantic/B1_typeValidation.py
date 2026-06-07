from pydantic import BaseModel

# Define the structure of a student record
class Student(BaseModel):
    name: str
    age: int


# Function to display student information
def display_student_info(student: Student):
    print("Name:", student.name)
    print("Age :", student.age)


# Student data received as a dictionary
student_data = {
    "name": "Ani",
    "age": "24" # pydantic will convert this str-->int , if mistakenly you passed str
}

# Create a Student object from the dictionary
student_record = Student(**student_data)  # ** unpacks the dictionary

# Display the student details
display_student_info(student_record)