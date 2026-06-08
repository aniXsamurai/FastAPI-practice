#----Notes----
# 1.EmailStr needs an external library : pip install "pydantic[email]"
# 2.we can add meta data using the combination of Annotated and Field
# 3. Field (Strict = True): To block auto type conversion like: age -> input:'23',raise error 


from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional,Annotated

# Define the structure of a student record
class Student(BaseModel):
    name: str = Field(max_length=50)
    age: int = Field(gt=15,lt=30)
    email : EmailStr   # Insead of regex or other complex code 
    linkedin: AnyUrl   # It will validate the data provied it a link
    skills: List[str]  #Typing List used to specify the type of the values too
    contact: Dict[str,str] = Field(max_length=2)
    married : Annotated[bool,Field(default=False,description="Student is married or not.")]  # Default value is false
    hobbies: Optional[List[str]] = None  #Optional is used , if user doesnt pass any value it will consider None


# Function to display student information
def display_student_info(student: Student):
    print("Name:", student.name)
    print("Age :", student.age)
    print("skills:", student.skills)
    print("contact :", student.contact)
    print("married:", student.married)
    print("hobbies :", student.hobbies) 
    print("Email :", student.email) 
    print("linkedin :", student.linkedin) 


# Student data received as a dictionary
student_data = {
    "name": "Ani",
    "age": "24", # pydantic will convert this str-->int , if mistakenly you passes str
    "skills" : ['python','fastAPI'],
    "contact":{'email':"ani@gmail.com",'ph':'18837438'},
    #married value is not sent
    #Hobbies also not sent
    #Throws error if format is wrong 
    "linkedin":'https://linkedin.com/in/aniruddha-garai',
    "email":'ani@gmail.com' 
}

# Create a Student object from the dictionary
student_record = Student(**student_data)  # ** unpacks the dictionary

# Display the student details
#display_student_info(student_record)

#we can use model_dump() to print record instead printing all separately
print(student_record.model_dump())