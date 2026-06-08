from pydantic import BaseModel
from typing import List,Dict,Optional

# Define the structure of a student record
class Student(BaseModel):
    name: str
    age: int
    skills: List[str] #Typing List used to specify the type of the values too
    contact: Dict[str,str]
    married : bool = False # Default value is false
    hobbies: Optional[List[str]] = None #Optional is used , if user doesnt pass any value it will consider None


# Function to display student information
def display_student_info(student: Student):
    print("Name:", student.name)
    print("Age :", student.age)
    print("skills:", student.skills)
    print("contact :", student.contact)
    print("married:", student.married)
    print("hobbies :", student.hobbies) 


# Student data received as a dictionary
student_data = {
    "name": "Ani",
    "age": "24", # pydantic will convert this str-->int , if mistakenly you passes str
    "skills" : ['python','fastAPI'],
    "contact":{'email':"ani@gmail.com",'ph':'18837438'}
    #married value is not sent
    #Hobbies also not sent
}

# Create a Student object from the dictionary
student_record = Student(**student_data)  # ** unpacks the dictionary

# Display the student details
display_student_info(student_record)