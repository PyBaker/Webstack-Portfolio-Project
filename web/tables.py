import enum
from xmlrpc.client import Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, LargeBinary, String, Boolean
from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
import uuid

username = "rod"
password = "r"
str1 = f'mysql://{username}:{password}@localhost:3306/VOTEAPP'  # Holds database info
engine = create_engine(str1)
Base = declarative_base()


class BaseModel():
    """Defines the to_dict method that returns a dictionary of each
    class's attributes to enable conversion to json objects on the APIs"""

    def to_dict(self):
        """returns dictionary of the instance's attributes"""

        my_dict = self.__dict__.copy()

        # remove sensitive information from my_dict
        if "Password" in my_dict:
            my_dict.pop('Password')
        if "Email" in my_dict:
            my_dict.pop("Email")
        if "id_no" in my_dict:
            my_dict.pop("id_no")

        my_dict.pop('_sa_instance_state')

        return my_dict



class myEnum(enum.Enum):
    """
    Defines enums to be used in the status
    fields
    """
    V = "Voted"
    NV = "Not Voted"


class RegisteredVoters(Base, BaseModel):
    """
    Defines a class RegisteredVoters
    """
    __tablename__ = "REGISTERED_VOTERS"
    reg_no = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    id_no = Column(Integer, primary_key=True, unique=True)
    First_Name = Column(String(256), nullable=False)
    Middle_Name = Column(String(256))
    Last_Name = Column(String(256))
    Location = Column(String(256))
    Password = Column(LargeBinary)
    Email = Column(String(256))
    DOR = Column(DateTime(timezone=True), server_default=func.now())


class Aspirants(Base, BaseModel):
    """
    Defines a class Aspirant's
    """
    __tablename__ = "ASPIRANTS"
    asp_no = Column(Integer, primary_key=True, autoincrement=True)
    id_no = Column(Integer, ForeignKey("REGISTERED_VOTERS.id_no"), primary_key=True)
    post_no = Column(Integer, ForeignKey("POST.post_no"), primary_key=True)
    post_name = Column(String(256), nullable=False)
    First_Name = Column(String(256), nullable=False)
    Middle_Name = Column(String(256))
    Last_Name = Column(String(256))
    photo = Column(String(256))
    Location = Column(String(256))
    Password = Column(LargeBinary)
    Email = Column(String(256))
    DOR = Column(DateTime(timezone=True), server_default=func.now())
    no_of_votes = Column(Integer, default=0)


class Post(Base, BaseModel):
    """
    Defines a class Post
    """
    __tablename__ = "POST"
    post_no = Column(Integer, primary_key=True, autoincrement=True)
    Post_Name = Column(String(256), nullable=False, unique=True)


class Admin(Base, BaseModel):
    """
    Defines a class Admin
    """
    __tablename__ = "ADMIN"
    id_no = Column(Integer, primary_key=True)
    First_Name = Column(String(256), nullable=False)
    Middle_Name = Column(String(256))
    Last_Name = Column(String(256))
    Location = Column(String(256))
    Password = Column(LargeBinary)
    Email = Column(String(256))
    DOR = Column(DateTime(timezone=True), server_default=func.now())

"""
class Votes(Base):
    
    __tablename__ = 'VOTES'
    vno = Column(Inhttps://github.com/PyBaker/Webstack-Portfolio-Project.gitteger, primary_key=True)
    asp_no = Column(Integer, ForeignKey("ASPIRANTS.asp_no"))
    pno = Column(Integer, ForeignKey("POST.pno"))
    seat_name = Column(String(256))
    First_Name = Column(String(256), nullable=False)
    Middle_Name = Column(String(256))
    Last_Name = Column(String(256))
    Location = Column(String(256))
    Votes_guarnered = Column(Integer)
    Percentage = Column(String(256))
"""


class Voters(Base, BaseModel):
    """
    Defines a class Voters that holds records
    for voters who have already logged into the
    system
    """
    __tablename__ = "VOTERS"
    id_no = Column(Integer, ForeignKey("REGISTERED_VOTERS.id_no"), primary_key=True)
    reg_no = Column(Integer, ForeignKey("REGISTERED_VOTERS.reg_no"), primary_key=True)
    president = Column(Boolean, default=False)
    senator = Column(Boolean, default=False)
    governor = Column(Boolean, default=False)
    mp = Column(Boolean, default=False)
    Status = Column(Enum(myEnum), default='NV')
    DOV = Column(DateTime(timezone=True), server_default=func.now())


# Deletes Tables Before Creating them
if __name__ == "__main__":
    """Create tables in the database"""
    Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)


"""
Improvements:
1. Encrypt passwords and obscure sensitive personal data
"""
