''' SQLAlchemy Model of scrapped data to store '''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    image = Column(String)
    link = Column(String)
    detail = Column(String)
    seller = Column(String)
    seller_items = Column(String)
    date = Column(String)
    price = Column(String)

    def __repr__(self):
        return "<Product(title='{}', image='{}', link='{}', detail='{}', seller='{}', seller_items='{}', date={}, price='{}'"\
            .format(self.title, self.image, self.link, self.detail, self.seller, self.seller_items, self.date, self.price)

