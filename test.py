from sqlalchemy import create_engine,text
from sqlalchemy.dialects.postgresql import insert
from website.models import students,Student
from sqlalchemy.orm import sessionmaker
db_string = "postgresql+psycopg2://bkrosywinjcmur:adb41bdf80128d0add3bb27166c52af7dba9e266a26bfb29e995c0a21287e747@ec2-3-217-146-37.compute-1.amazonaws.com:5432/d3do0ibhcg15e6"
engine = create_engine(db_string)

def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs limit 2;"))
    jobs = []
    for row in result.all():
      jobs.append(dict(row))
    return jobs                      
      
Session = sessionmaker(bind=engine)
new_student=Student(studentid=22,studentname='Susan',major='CSCE')
with Session() as session:
    session.add(new_student)
    session.commit()

      
with engine.connect() as conn:
    result=conn.execute(text("select * from students"))
    for row in result.all():
        print(row)
    
