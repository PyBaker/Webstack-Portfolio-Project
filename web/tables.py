import enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, LargeBinary, String
from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.sql import func

Base = declarative_base()


class myEnum(enum.Enum):
    """
    Defines enums to be used in the status
    fiels
    """
    V = "Voted"
    NV = "Not Voted"


class RegisteredVoters(Base):
    """
    Defines a class RegisteredVoters
    """
    __tablename__ = "REGISTERED_VOTERS"
    reg_no = Column(Integer, primary_key=True, autoincrement=True)
    id_no = Column(Integer, primary_key=True, autoincrement=False)
    First_Name = Column(String(256), nullable=False)
    Middle_Name = Column(String(256))
    Last_Name = Column(String(256))
    Location = Column(String(256))
    Password = Column(LargeBinary)
    Email = Column(String(256))
    DOR = Column(DateTime(timezone=True), server_default=func.now())


class Aspirants(Base):
    """
    Defines a class Aspirant's
    """
    __tablename__ = "ASPIRANTS"
    asp_no = Column(Integer, primary_key=True)
    id_no = Column(Integer, ForeignKey("REGISTERED_VOTERS.id_no"))
    Post_Name = Column(Integer, ForeignKey("POST.Post_Name"))
    First_Name = Column(String(256), nullable=False)
    Middle_Name = Column(String(256))
    Last_Name = Column(String(256))
    Location = Column(String(256))
    Email = Column(String(256))
    DOR = Column(DateTime(timezone=True), server_default=func.now())


class Post(Base):
    """
    Defines a class Post
    """
    __tablename__ = "POST"
    pno = Column(Integer, primary_key=True)
    Post_Name = Column(String(256), nullable=False, unique=True)


class Admin(Base):
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


class Votes(Base):
    """
    Defines a class Votes
    """
    __tablename__ = "VOTES"
    vno = Column(Integer, primary_key=True)
    asp_no = Column(Integer, ForeignKey("ASPIRANTS.asp_no"))
    pno = Column(Integer, ForeignKey("POST.pno"))
    seat_name = Column(String(256))
    First_Name = Column(String(256), nullable=False)
    Middle_Name = Column(String(256))
    Last_Name = Column(String(256))
    Location = Column(String(256))
    Votes_guarnered = Column(Integer)
    Percentage = Column(String(256))


class Voters(Base):
    """
    Defines a class Voters that holds records
    for voters who have already logged into the
    system
    """
    __tablename__ = "VOTERS"
    id = Column(Integer, primary_key=True)
    reg_no = Column(Integer, ForeignKey("REGISTERED_VOTERS.reg_no"))
    Status = Column(Enum(myEnum), default='NV')
    DOV = Column(DateTime(timezone=True), server_default=func.now())

if __name__ == "__main__":
    str1 = 'mysql://root:''@localhost:3306/VOTEAPP'  # Holds database info
    engine = create_engine(str1)
    #creates database first
    #engine.connect().execute('CREATE DATABASE VOTEAPP;')

    # Deletes Tables Before Creating them
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
