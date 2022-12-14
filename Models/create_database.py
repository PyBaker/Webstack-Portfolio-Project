from sqlalchemy import create_engine
import sqlalchemy_utils as sq


username = 'rod'
password = 'r' 
database = 'VOTEAPP'
str1 = f'mysql://{username}:{password}@localhost:3306/{database}'  # Holds database info
engine = create_engine(str1)
if not sq.database_exists(engine.url):
    sq.create_database(engine.url)

print(sq.database_exists(engine.url))
