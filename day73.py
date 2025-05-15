from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
# This is a comment explaining the purpose of the app
# The FastAPI app is created to handle HTTP requests and responses
# @app.get("/")
# def read_root():
#     return {"Message": "Hello World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}

class  Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items/")
def create_item(item: Item):
    return {"received": item}
# Bài 2: Tạo Route Get
@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}

@app.get("/subtract")
def subtract(a: int, b: int):
    return {"result": a-b}

@app.get("/multiply")
def multiply(a: int, b: int):
    return {"result": a*b}

@app.get("/divide")
def divide(a: int, b: int):
    if b == 0:
        return {"error": "Division by zero is not allowed"}
    return {"result": a / b}


# Bài 3: Tạo API POST
    # Khai bao mo hinh Input
class User(BaseModel):
    name: str
    age: int
    email: str
    # Dinh nghia Route POST
@app.post("/user")
def crete_user(user: User):
    is_audult = user.age >= 18
    return {
        "name": user.name,
        "age": user.age,
        "email": user.email,
        "is_audult": is_audult
    }

# Bài 4: Quản lý danh sách sản phẩm
# Get /products trả về danh sách sản phẩm
product_list = []

class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
# Get /products/{product_id} trả về thông tin sản phẩm theo id
@app.get("/products")
def get_products():
    return {"products": product_list}

# Post /products thêm sản phẩm mới
@app.post("/products")
def add_product(product: Product):
    product_list.append(product)
    return {"message": "Đã thêm sản phẩm mới", "product": product}
