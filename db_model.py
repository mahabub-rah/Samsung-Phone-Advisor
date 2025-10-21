from final_scrape import all_specs
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#make the db file
db_url = "postgresql+psycopg2://postgres:root@localhost:5432/samsung_db"
Base = declarative_base()
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind =engine)
session = SessionLocal



#make db model
class SmartphoneSpecs(Base):
    __tablename__ = 'smartphone_specs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(255), nullable=False)
    battery = Column(String(50))
    rear_camera = Column(String)
    ram = Column(String(50))
    storage = Column(String(50))
    price = Column(Integer)




# integration with db
Base.metadata.create_all(bind=engine)

def insert():
    db = session()
    for i, item in enumerate(all_specs):
        product = SmartphoneSpecs(**item)
        db.add(product)
        print(f"Added {i+1}: {item.get('model_name')}")
    db.commit()
    db.close()

# Call the function
if __name__ == "__main__":
    insert()