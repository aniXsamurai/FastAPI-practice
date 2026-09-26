"""
=============================================================================
FastAPI Tutorial: Student Management System API
=============================================================================
This combined script demonstrates core FastAPI concepts:
1. Basic API setup & root endpoints
2. File reading helper functions
3. Path Parameters with validation & metadata
4. Proper Error Handling using HTTPException
5. Query Parameters (required, default values, optional filters)
6. Sorting and filtering collections
=============================================================================
"""

import json
from fastapi import FastAPI, Path, Query, HTTPException

# Initialize the FastAPI application
app = FastAPI(
    title="Student Management System API",
    description="A step-by-step tutorial API demonstrating FastAPI fundamentals.",
    version="1.0.0"
)


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------
def load_data() -> dict:
    """
    Helper function to load student records from a JSON file.
    """
    try:
        with open('students.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500, 
            detail="Database file 'students.json' not found."
        )


# ---------------------------------------------------------------------------
# 1. Basic Endpoints
# ---------------------------------------------------------------------------
@app.get("/")
def home():
    """
    Root endpoint: Returns a welcome message.
    """
    return {'message': 'Student Management System API.'}


@app.get('/view')
def view_all_students():
    """
    Endpoint to fetch all student data at once.
    """
    data = load_data()
    return data


# ---------------------------------------------------------------------------
# 2. Path Parameters with Metadata, Validation, & Exception Handling
# ---------------------------------------------------------------------------
@app.get('/students/{student_id}')
def get_student_by_id(
    # '...' (Ellipsis) indicates that the parameter is strictly required.
    # 'gt' (greater than) and 'lt' (less than) enforce numeric ranges in API docs/validation.
    student_id: int = Path(
        ..., 
        description='ID of the student in the DB (must be between 1 and 10)', 
        example=1, 
        gt=0, 
        lt=11
    )
):
    """
    Retrieve a specific student by ID using Path Parameters.
    Uses HTTPException to return proper HTTP 404 status codes if not found.
    """
    data = load_data()
    str_id = str(student_id)
    
    if str_id in data:
        return data[str_id]
    
    # Raise formal HTTP 404 instead of returning a custom error dictionary
    raise HTTPException(status_code=404, detail="Student not found")


# ---------------------------------------------------------------------------
# 3. Query Parameters: Required vs Optional with Validation
# ---------------------------------------------------------------------------
@app.get('/sort')
def sort_students(
    # '...' makes 'sort_by' a required query parameter
    sort_by: str = Query(
        ..., 
        description='Sort field: age, fees_paid, or attendence'
    ),
    # Default value provided: 'order' defaults to 'asc' if omitted by user
    order: str = Query('asc', description='Sort order: asc or desc')
):
    """
    Sort student records by field and direction using required/optional Query Parameters.
    """
    valid_fields = ['age', 'fees_paid', 'attendence']

    # Validate requested sort field
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400, 
            detail=f'Invalid field! Please select from: {valid_fields}'
        )
    
    # Validate sort ordering direction
    if order not in ['asc', 'desc']:
        raise HTTPException(
            status_code=400, 
            detail='Invalid order! Please select from: asc, desc'
        )
    
    is_descending = True if order == 'desc' else False

    data = load_data()
    
    # Perform in-memory sorting over dictionary values
    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=is_descending
    )
    
    return sorted_data


# ---------------------------------------------------------------------------
# 4. Query Parameters: Filtering with Optional Parameters
# ---------------------------------------------------------------------------
@app.get('/filter')
def filter_students(
    # Setting default to None makes these query parameters fully optional
    course: str | None = None,
    city: str | None = None,
    is_placed: bool | None = None
):
    """
    Filter students using optional Query Parameters.
    Multiple filters can be combined (e.g., /filter?city=NewYork&is_placed=true).
    """
    results = list(load_data().values())
    
    if course:
        results = [
            student for student in results 
            if student.get("course", "").lower() == course.lower()
        ]
    if city:
        results = [
            student for student in results 
            if student.get("city", "").lower() == city.lower()
        ]
    if is_placed is not None:
        results = [
            student for student in results 
            if student.get("is_placed") == is_placed
        ]
        
    return results