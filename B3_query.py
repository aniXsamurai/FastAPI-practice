from fastapi import FastAPI,Path,Query,HTTPException
import json
app = FastAPI()

def load_data():
    with open('students.json','r') as f:
        data = json.load(f)
    return data 

@app.get('/')
def load():
    data = load_data()
    return data

@app.get('/students/{student_id}')
def get_details(student_id:str = Path(...,description='enter student_id')):
    data = load_data()
    if student_id in data:
        return data[student_id]

 #'...' means required 
 # sorting end point  
@app.get('/sort')
def sort_data(sort_by:str = 
              Query(...,description='sort by age,fees_paid or attendence'),
              order:str = Query('asc')):
    valid_fields = ['age','fees_paid' , 'attendence']

    # validating user query
    if sort_by not in valid_fields:
        # 400 : bad request
        raise HTTPException(status_code=400,detail=f'Invaid field ! please select form:{valid_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f'Invaid field ! please select form: asc,desc')
    
    choice = True if order == 'desc' else False

    #performing ops
    data = load_data()

    sorted_data = sorted(
        data.values(),
        key = lambda x:x.get(sort_by,0),
        reverse=choice)
    return sorted_data

# Filters
@app.get('/filter')
def filters(course:str | None = None,
            city:str | None = None,
            is_placed:bool | None = None ):
    
    results = list(load_data().values())
    if course:
        results = [data for data in results
                   if data["course"].lower() == course.lower()]
    if city:
        results = [data for data in results
                   if data["city"].lower() == city.lower()]
    if is_placed:
        results = [data for data in results
                   if data["is_placed"] == is_placed]        
    return results
    
