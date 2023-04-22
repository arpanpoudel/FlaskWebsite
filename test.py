from sqlalchemy import create_engine,text
db_string = "postgresql+psycopg2://bkrosywinjcmur:adb41bdf80128d0add3bb27166c52af7dba9e266a26bfb29e995c0a21287e747@ec2-3-217-146-37.compute-1.amazonaws.com:5432/d3do0ibhcg15e6"
engine = create_engine(db_string)

def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs limit 2;"))
    jobs = []
    for row in result.all():
      jobs.append(dict(row))
    return jobs                      
      
#print(load_jobs_from_db())  
with engine.connect() as conn:
    result = conn.execute(text("select * from students"))
    #print(result)

from sqlalchemy import create_engine, func, desc, Table, Column, Integer, String, MetaData,ForeignKeyConstraint
from sqlalchemy.orm import sessionmaker

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

# query the top 3 jobs with maximum number of applications
top_jobs = session.query(jobs, func.count(applications.columns.jobid).label('num_apps'))\
                  .join(applications, jobs.columns.jobid == applications.columns.jobid)\
                  .group_by(jobs.columns.jobid)\
                  .order_by(desc('num_apps'))\
                  .limit(3)\
                  .all()

# create a list of dictionaries representing the top jobs

job_list = []
for jobid,companyname,jobtitle,salary,department,_  in top_jobs:
    job_dict = {
        'jobid': jobid,
        'companyname': companyname,
        'jobtitle': jobtitle,
        'salary': salary,
        'desiredmajor': department,
        
    }
    job_list.append(job_dict)
print(job_list)