from config import DATABASE_URL
from sqlalchemy import create_engine
from models import Product, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

#Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def saveProduct(data):
    with session_scope() as session:
        for record in data:
            product = Product(**record)
            session.add(product)
        
if __name__ == '__main__':
    recreate_database()

