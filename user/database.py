from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine


url="postgresql://postgres:soft@localhost:5432/users"
engine=create_engine(url)

session=sessionmaker(autocommit=False,autoflush=False,bind=engine)
base=declarative_base()
db=session()

def get_db():
    return db