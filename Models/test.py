from sqlalchemy import create_engine
import sqlalchemy_utils as sq
from sqlalchemy.orm import sessionmaker
from tables import Aspirants


username = "rod"
password = "r"
str1 = f'mysql://{username}:{password}@localhost:3306/VOTEAPP'  # Holds database info
engine = create_engine(str1)
DbSession = sessionmaker(bind=engine)
session = DbSession()
aspirants = session.query(Aspirants.First_Name, Aspirants.Middle_Name).filter(Aspirants.post_name == "President").all()

print(aspirants)
