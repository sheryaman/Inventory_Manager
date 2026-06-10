from typing import List
from sqlalchemy import create_engine,ForeignKey
from sqlalchemy.orm import DeclarativeBase , Session , relationship , Mapped , mapped_column , sessionmaker
from dotenv import load_dotenv
import os 

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True , autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False,unique=True)
    products: Mapped[List["Product"]] = relationship("Product" , back_populates="category")
class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True , autoincrement=True)
    name : Mapped[str] = mapped_column(nullable=False,unique=True)
    price: Mapped[float] = mapped_column(nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False)
    category_id : Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship("Category",back_populates="products")
load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocalUser = sessionmaker(bind=engine)
def get_session():
    session = SessionLocalUser()
    try:
        yield session
    finally:
        session.close()

def add_categories(name):
    with Session(engine) as session:
        category = Category(name=name)
        session.add(category)
        session.commit()
        return True
def add_product(name,price,stock,category_name):
    with Session(engine) as session:
        category = session.query(Category)\
        .filter(Category.name == category_name)\
        .first()
        if not category:
            return False
        product = Product(name=name,price=price,stock=stock,category=category)
        session.add(product)
        session.commit()
        return True
def get_all_products(session):
        product = session.query(Product).all()
        return [(p.id , p.name , p.price , p.stock,p.category.name) for p in product]
def  get_all_categories():
    with Session(engine) as session:
        return session.query(Category).all()
def get_product_by_name(name):
    with Session(engine) as session:
        return session.query(Product)\
        .filter(Product.name == name)\
        .first()
def update_stock(name , new_stock):
    with Session(engine) as session:
        product = session.query(Product)\
        .filter(Product.name == name)\
        .first()
        if product:
            product.stock = new_stock
            session.commit()
            return True
        return False
def delete_product(name):
    with Session(engine) as session:
        product = session.query(Product)\
        .filter(Product.name == name)\
        .first()
        if product:
            session.delete(product)
            session.commit()
            return True
        return False
    


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Connected to PostgreSQL successfully")
    session = next(get_session())
    products = get_all_products(session)
    for p in products:
        print(p)
    session.close()