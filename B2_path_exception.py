from fastapi import FastAPI,Path,HTTPException
import json

app = FastAPI()

def load_data():
    with open('students.json','r') as f:
        data = json.load(f)
    return data    

# Defining endpoint
@app.get("/")
def hello():
    return {'message':'Student management System API.'}


@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/students/{student_id}')
# ... means all path parameters are required,gt=greater than ,lt= less than
def view(student_id:str = Path(...,description='ID of the student in the DB',example="1")):
    data = load_data()
    if student_id in data:
        return data[student_id]
    raise HTTPException(status_code=404,detail="Student not found")