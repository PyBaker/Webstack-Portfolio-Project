from sqlalchemy import create_engine
import sqlalchemy_utils as sq


str1 = 'mysql://root:''@localhost:3306/testdb'  # Holds database info
engine = create_engine(str1)
if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))
