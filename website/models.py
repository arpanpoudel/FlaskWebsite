from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import engine
from sqlalchemy import create_engine,text,Column, Integer, ForeignKey,String,Float, func, desc, Table, Column, Integer, String, MetaData,ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

# # Define a class for the students table
# class students(Base):
#     __tablename__ = 'students'
#     studentId = Column(Integer, primary_key=True)
#     studentName = Column(String(255))
#     Major = Column(String(50))
#     applications = relationship('Application', back_populates='student')

# # Define a class for the jobs table
# class jobs(Base):
#     __tablename__ = 'jobs'
#     jobId = Column(Integer, primary_key=True)
#     CompanyName = Column(String(255))
#     JobTitle = Column(String(255))
#     Salary = Column(Float)
#     DesiredMajor = Column(String(50))
#     applications = relationship('Application', back_populates='job')

# # Define a class for the applications table
# class application(Base):
#     __tablename__ = 'Applications'
#     ApplicationId = Column(Integer, primary_key=True)
#     StudentId = Column(Integer, ForeignKey('students.StudentId'))
#     JobId = Column(Integer, ForeignKey('jobs.JobId'))
#     student = relationship('Student', back_populates='applications')
#     job = relationship('Job', back_populates='applications')
    
# Create the tables in the database
#Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
metadata=MetaData()
# define the tables
students = Table('students', metadata,
    Column('studentid', Integer, primary_key=True),
    Column('studentname', String),
    Column('major', String)
)

jobs = Table('jobs', metadata,
    Column('jobid', Integer, primary_key=True),
    Column('companyname', String),
    Column('jobtitle', String),
    Column('salary', Integer),
    Column('desiredmajor', String)
)

applications = Table('applications', metadata,
    Column('applicationId', Integer, primary_key=True),
    Column('studentid', Integer),
    Column('jobid', Integer),
    ForeignKeyConstraint(['studentid'], ['students.studentid']),
    ForeignKeyConstraint(['jobid'], ['jobs.jobid'])
)

def load_jobs_from_db():
  with engine.connect() as conn:
    top_jobs = session.query(jobs, func.count(applications.columns.jobid).label('num_apps'))\
                  .join(applications, jobs.columns.jobid == applications.columns.jobid)\
                  .group_by(jobs.columns.jobid)\
                  .order_by(desc('num_apps'))\
                  .limit(3)\
                  .all()
  results = [dict(row) for row in top_jobs]

  return results                      
      