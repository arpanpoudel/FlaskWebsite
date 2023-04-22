from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_required,current_user
from . import engine
views=Blueprint('views',__name__)
from .models import *
from sqlalchemy.orm import sessionmaker

@views.route('/')
@login_required
def home():
    jobs=load_jobs_from_db()
    return render_template("home.html",user=current_user,jobs=jobs)

@views.route('/add-student',methods=['GET', 'POST'])
def add_student():
    if  request.method == 'POST':
        studentId = request.form.get('studentId')
        studentName = request.form.get('studentName')
        major = request.form.get('major')
        try:
            studentId=int(studentId)
        except  Exception as e:
            flash('Student Id should be integer.', category='error')
            return render_template("addStudent.html", user=current_user)
        try:
            with engine.connect() as conn:
                conn.execute(f'Insert into students Values{studentId,studentName,major} ')
            flash('Student  Added!', category='success')
            return redirect(url_for('views.home'))
        except Exception as e:
            flash('Student already exists!', category='error')
            return render_template("addStudent.html", user=current_user)
        
    return render_template("addStudent.html",user=current_user)

@views.route('/search-student')
def search_student():
        # Get the selected major from the form (if any)
    selected_major = request.args.get('major', default='', type=str)
    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query the database for all students (or students with the selected major)
    if selected_major:
        query = f"SELECT * FROM students WHERE major = '{selected_major}'"
    else:
        query = "SELECT * FROM students"
    result = session.execute(query).fetchall()
    students = [dict(row) for row in result]
    print(students)

    # Render the search page template with the list of students and the selected major
    return render_template('searchStudent.html', students=students, selected_major=selected_major,user=current_user)

@views.route('/add-jobs',methods=['GET', 'POST'])
def add_jobs():
    if  request.method == 'POST':
        jobId = request.form.get('jobId')
        companyName = request.form.get('companyName')
        jobTitle = request.form.get('jobTitle')
        salary = request.form.get('salary')
        desiredMajor = request.form.get('desiredMajor')
        #print(jobID,companyName,jobTitle,salary,desiredMajor)
        try:
            jobId=int(jobId)
        except  Exception as e:
            flash('Job Id should be integer.', category='error')
            return render_template("addJobs.html", user=current_user)
        try:
            salary=float(salary)
        except  Exception as e:
            flash('Salary should be number.', category='error')
            return render_template("addJobs.html", user=current_user)
        
            
        with engine.connect() as conn:
            conn.execute(f'Insert into jobs Values{jobId,companyName,jobTitle,salary,desiredMajor} ')
        flash('Jobs  Added!', category='success')
        return redirect(url_for('views.home'))
    
    return render_template("addJobs.html", user=current_user)

@views.route('/search-jobs')
def search_jobs():
    # Get the selected major from the form (if any)
    selected_major = request.args.get('major', default='', type=str)

    # Query the database for all jobs (or jobs with the selected major)
    if selected_major:
        query = f"SELECT * FROM jobs WHERE desiredmajor = '{selected_major}'"
    else:
        query = "SELECT * FROM jobs"
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.execute(query).fetchall()
    jobs = [dict(row) for row in result]

    # Render the search page template with the list of jobs and the selected major
    return render_template('searchJobs.html', jobs=jobs, selected_major=selected_major,user=current_user)

@views.route('/add-application',methods=['GET', 'POST'])
def add_application():
    if  request.method == 'POST':
        jobId = int(request.form.get('jobId'))
        studentId = int(request.form.get('studentId'))
        #print(jobID,companyName,jobTitle,salary,desiredMajor)
        try:
            jobId=int(jobId)
        except  Exception as e:
            flash('Job Id should be integer.', category='error')
            return render_template("addApplication.html", user=current_user)
        try:
            studentId=float(studentId)
        except  Exception as e:
            flash('Salary should be number.', category='error')
            return render_template("addApplication.html", user=current_user)
        
        try:
            # Create a session to interact with the database
            Session = sessionmaker(bind=engine)
            session = Session()
            query = f"SELECT * FROM students WHERE studentId = {studentId}"
            result = session.execute(query).fetchone()
            if not result:
                flash(f'No student with ID: {studentId} in the record.', category='error')
                return render_template("addApplication.html", user=current_user)
                
            query = f"SELECT * FROM jobs WHERE jobId = {jobId}"
            result = session.execute(query).fetchone()
            if not result:
                flash(f'No Job with ID: {jobId} in the record.', category='error')
                return render_template("addApplication.html", user=current_user)
            
            with engine.connect() as conn:
                conn.execute(f'Insert into applications (jobid,studentid) Values{jobId,studentId} ')
            flash('Application  Added!', category='success')
            return redirect(url_for('views.home'))
        except Exception as e:
            print(e)
            return render_template("addApplication.html", user=current_user)
        
    return render_template("addApplication.html",user=current_user)

@views.route('/search-application',methods=['GET', 'POST'])
def search_application():
    # Get the selected major, student, or job from the form (if any)
    selected_major = request.args.get('major', default='', type=str)
    selected_student = request.args.get('student', default='', type=str)
    selected_job = request.args.get('job', default='', type=int)

    # Query the database for all applications (or applications with the selected major, student, or job)
    query = "SELECT students.studentname, jobs.companyname, jobs.salary, students.major FROM applications "
    query += "JOIN students ON applications.studentid = students.StudentId "
    query += "JOIN jobs ON applications.jobId = jobs.jobid "
    if selected_major:
        query += f"WHERE students.major = '{selected_major}' "
    elif selected_student:
        query += f"WHERE students.studentName = '{selected_student}' "
    elif selected_job:
        query += f"WHERE jobs.jobid = {selected_job} "
    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.execute(query).fetchall()
    applications = [dict(row) for row in result]

    # Render the view applications page template with the list of applications and the selected major, student, or job
    return render_template('searchApplication.html', applications=applications, selected_major=selected_major, selected_student=selected_student, selected_job=selected_job,user=current_user)