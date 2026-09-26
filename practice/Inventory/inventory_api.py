from fastapi import FastAPI,Query,HTTPException,Path
import json

app = FastAPI()

# Data Loading
def load_data():
    with open('inventory.json','r') as f:
        return json.load(f)

"""
Task 2: Range Filtering with Query Parameters
Goal: Create an endpoint GET /products/price-range.
Requirements:
Accept two optional float query parameters: min_price and max_price.
If min_price is provided, ensure it is >= 0.0$ using validation rules.
Return all products whose price falls within the specified range.
If min_price is greater than max_price, 
raise an HTTPException(status_code=400, detail="min_price cannot be greater than max_price")
"""    

@app.get('/products/price-range')
def FindProductsByPriceRange(
    min_price : float | None=Query(default=None,ge=0.0) ,
    max_price : float | None=None
):  
    
    if min_price is not None and max_price is not None:
        if min_price > max_price:
            raise HTTPException(
                status_code = 404,
                detail = "min_price cannot be greater than max_price"
            )
    products = list(load_data().values())

    # 3. Apply min_price filter if provided
    if min_price is not None:
        products = [p for p in products if p["price"] >= min_price]

    # 4. Apply max_price filter if provided
    if max_price is not None:
        products = [p for p in products if p["price"] <= max_price]

    return products





"""
Task 1: Basic Retrieval & Handling 404
"""
@app.get('/products/{product_id}')
def get_details(product_id:int = Path(...,description="Enter product_id greater than 0",gt=0)):
    data = load_data()
    product_id_str = str(product_id)
    if str(product_id_str) in data:
        return data[product_id_str]
    else:
        raise HTTPException(
            status_code = 404,
            detail = "Product not found."
        )

    

"""
Task 3: Search & Low Stock Alerts
Goal: Create an endpoint GET /products/search.

Requirements:

Accept a required query parameter keyword (e.g., "mouse" or "chair").

Accept an optional boolean parameter low_stock_only (default = False).

Return products where keyword is present in the name (case-insensitive).

If low_stock_only=True, return only matching items where stock < 20.
"""


@app.get('/search')
def SearchProductByName(name:str = Query(...,description="Enter product name."),low_stock_only:bool | None = Query(default=False,description="Filter by low stock status")):
    products = list(load_data().values())
    
    results = [p for p in products if name.lower() in p["name"].lower()]

    if low_stock_only:
        results = [p for p in results if p["stock"]<20]
    return results