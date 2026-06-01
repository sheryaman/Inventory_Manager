from fastapi import FastAPI , Depends ,  HTTPException
from sqlalchemy.orm import Session
from models import (engine , Base , get_session , get_product_by_name, 
                   add_product , add_categories , get_all_categories, 
                   get_all_products,delete_product,update_stock)
from pydantic import BaseModel , Field
Base.metadata.create_all(engine)

app = FastAPI()
class ProductResponse(BaseModel):
    id:int
    name:str
    price:float
    stock:int
    category:str
    model_config = {"from_attributes": True}
class ProductCreate(BaseModel):
    name: str
    price: float = Field(gt=0 , description="the number must be greater than zero")
    stock: int = Field(ge = 0 , description="The number must be greater or equals to zero")
    category_name: str
class CategoryCreate(BaseModel):
    name: str
class StockUpdate(BaseModel):
     new_stock: int

@app.get("/products",response_model= list[ProductResponse])
def read_products(session :Session = Depends(get_session)):
    return get_all_products(session)
@app.get("/products/{name}")
def read_product(name : str, session : Session =Depends(get_session)):
    product = get_product_by_name(name)
    if not product:
        raise HTTPException(status_code=404, detail="not found")
    return {"name" : product.name, "price": product.price, "stock" : product.stock}
@app.post("/products" ,status_code  = 201)
def create_product(product : ProductCreate , session : Session = Depends(get_session)):
    result = add_product(product.name,product.price,product.stock,product.category_name)
    if not result:
        raise HTTPException(status_code=400,detail="Category Doesn't exists")
    return {"message": f"{product.name} added successfully"}
@app.post("/categories",  status_code = 201)
def create_category(category: CategoryCreate  , session : Session = Depends(get_session)):
    result = add_categories(category.name)
    return {"message": f"Category '{category.name}' added"}
@app.put("/products/{name}/stock")
def change_stock(name : str , data : StockUpdate):
      result = update_stock(name,data.new_stock)
      if not result:
          raise HTTPException(status_code=404 , detail="it couldn't update  the product")
      return {"message": f"Stock updated for {name}"}
@app.delete("/products/{name}")
def remove_product(name : str):
    result = delete_product(name)
    if not result:
        raise HTTPException(status_code=404,detail="product no found")
    return {"message": f"{name} deleted"}

