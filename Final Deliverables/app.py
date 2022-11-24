from flask import Flask,request,render_template,request,redirect,url_for,session,flash
from wtforms import Form, StringField, TextAreaField, PasswordField, validators,EmailField,SelectField


import ibm_db
import re

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
app.secret_key='a'

#connect db2
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=twv84281;PWD=aFksEohGLVdc6pYr",'','')

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/recruit_user')
def recruit_user():
    return render_template('recruit_user.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/job_details')
def job_details():
    return render_template('job-details.html')

@app.route('/signup_recruiter')
def signup_recruiter():
    return render_template('signup_recruiter.html')

@app.route('/signup_user')
def signup_user():
    return render_template('signup_user.html')

@app.route('/login_signup_user')
def login_signup_user():
    return render_template('login_signup_user.html')

@app.route('/login_signup_recruiter')
def login_signup_recruiter():
    return render_template('login_signup_recruiter.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/postjob')
def postjob():
    return render_template('postjob.html')


@app.route('/user_register',methods=['GET','POST'])
def user_register():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        sql="SELECT * FROM jobseekers WHERE email=?"
        st=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(st,1,email)
        ibm_db.execute(st)
        account=ibm_db.fetch_assoc(st)
        print(account)
        if account:
            msg="account already exixt"
            flash('Account is already exist, Try Login ','danger')
            print(msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg="invalid email"
            flash('Email format is Incorrect','danger')
            print(msg)
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg="shld contain oly alpha"
            flash('Username must contain only Alphabets and Numbers','danger')
            print(msg)
        else:
            insert_sql="INSERT INTO jobseekers VALUES(?,?,?)"
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,username)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.execute(prep_stmt)
            a = sendmail()



    return render_template('redirect_user.html')
def sendmail() :
    email_message = Mail(
    from_email='sangeethrajuniverse@gmail.com',
    to_emails= request.form.get('email'),
    subject='Job UP Email Verification',
    html_content='<h3>Thankyou for signing up with JOB UP</h3><br><p>This email is sent to verify the applicant. You are a registered user now.<br> </p><h2>Job UP, All In One Stop For Job.</h2>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(email_message)
        status = response.status_code
    except Exception as err:
        print(err.message)
        
    return True
    
@app.route('/recruiter_register',methods=['GET','POST'])
def recruiter_register():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        sql="SELECT * FROM recruiters WHERE email=?"
        st=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(st,1,email)
        ibm_db.execute(st)
        account=ibm_db.fetch_assoc(st)
        print(account)
        if account:
            msg="account already exixt"
            flash('Account is already exist, Try Login ','danger')
            print(msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg="invalid email"
            flash('Email format is Incorrect','danger')
            print(msg)
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg="shld contain oly alpha"
            flash('Username must contain only Alphabets and Numbers','danger')
            print(msg)
        else:
            insert_sql="INSERT INTO recruiters VALUES(?,?,?)"
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,username)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.execute(prep_stmt)
            a=sendmail()
    return render_template('redirect_recruiter.html')

@app.route('/user_login',methods=['GET','POST'])
def user_login():
    global userid
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM jobseekers WHERE email=? AND password=?"
        st=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(st,1,email)
        ibm_db.bind_param(st,2,password)
        ibm_db.execute(st)
        account=ibm_db.fetch_assoc(st)
        print(account)
        if account:
            session['logged_in']=True
            session['id']=account['USERNAME']
            userid=account["USERNAME"]
            session['username']=account['USERNAME']
            sql = "SELECT * FROM USERPROFILE WHERE email=?"
            st=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(st,1,email)
            ibm_db.execute(st)
            account=ibm_db.fetch_assoc(st)
            if(account):
                return redirect(url_for('setup_u',uname=userid))
            else:
                return render_template('setup_u.html')
        else:
            return render_template('login_signup_user.html')
    return render_template('login_signup_user.html')

@app.route('/recruiter_login',methods=['GET','POST'])
def recruiter_login():
    global userid
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM recruiters WHERE email=? AND password=?"
        st=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(st,1,email)
        ibm_db.bind_param(st,2,password)
        ibm_db.execute(st)
        account=ibm_db.fetch_assoc(st)
        print(account)
        if account:
            session['logged_in']=True
            session['id']=account['USERNAME']
            userid=account["USERNAME"]
            session['username']=account['USERNAME']
            return redirect(url_for('r_dashboard',uname=userid))
        else:
            return render_template('login_signup_recruiter.html')
    return render_template('login_signup_recruiter.html')

@app.route('/recruiter_dashboard',methods=['GET','POST'])
def recruiter_dashboard():
    if request.method == 'POST':
        compname=request.form['f_name']
        country=request.form['country']
        city=request.form['city']
        address=request.form['address']
        phone=request.form['phone']
        email=request.form['email']
        website=request.form['website']
        description=request.form['textarea']
        insert_sql="INSERT INTO RECRUITERPROFILE VALUES(?,?,?,?,?,?,?,?)"
        prep_stmt=ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt,1,compname)
        ibm_db.bind_param(prep_stmt,2,country)
        ibm_db.bind_param(prep_stmt,3,city)
        ibm_db.bind_param(prep_stmt,4,address)
        ibm_db.bind_param(prep_stmt,5,phone)
        ibm_db.bind_param(prep_stmt,6,email)
        ibm_db.bind_param(prep_stmt,7,website)
        ibm_db.bind_param(prep_stmt,8,description)
        ibm_db.execute(prep_stmt)
        return render_template("r_dashboard.html")
    return render_template("r_dashboard.html")


@app.route('/user_dashboard',methods=['GET','POST'])
def user_dashboard():
    if request.method == 'POST':
        fname=request.form['f_name']
        mname=request.form['m_name']
        lname=request.form['l_name']
        country=request.form['country']
        city=request.form['city']
        address=request.form['address']
        phone=request.form['phone']
        email=request.form['email']
        website=request.form['website']
        description=request.form['textarea']
        college=request.form['school_name']
        degree=request.form['degree']
        clg_desc=request.form['textarea1']
        job=request.form['title']
        fromm=request.form['date_from']
        to=request.form['date_to']
        job_desc=request.form['textarea2']
        insert_sql="INSERT INTO USERPROFILE VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        prep_stmt=ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt,1,fname)
        ibm_db.bind_param(prep_stmt,2,mname)
        ibm_db.bind_param(prep_stmt,3,lname)
        ibm_db.bind_param(prep_stmt,4,country)
        ibm_db.bind_param(prep_stmt,5,city)
        ibm_db.bind_param(prep_stmt,6,address)
        ibm_db.bind_param(prep_stmt,7,phone)
        ibm_db.bind_param(prep_stmt,8,email)
        ibm_db.bind_param(prep_stmt,9,website)
        ibm_db.bind_param(prep_stmt,10,description)
        ibm_db.bind_param(prep_stmt,11,college)
        ibm_db.bind_param(prep_stmt,12,degree)
        ibm_db.bind_param(prep_stmt,13,clg_desc)
        ibm_db.bind_param(prep_stmt,14,job)
        ibm_db.bind_param(prep_stmt,15,fromm)
        ibm_db.bind_param(prep_stmt,16,to)
        ibm_db.bind_param(prep_stmt,17,job_desc)
        ibm_db.execute(prep_stmt)
        return render_template("u_dashboard.html")
    return render_template("u_dashboard.html")

@app.route('/r_dashboard/<uname>')
def r_dashboard(uname):
    return render_template('r_dashboard.html',userName=uname)

@app.route('/u_dashboard/<uname>')
def u_dashboard(uname):
    return render_template('u_dashboard.html',userName=uname)


if __name__ == '__main__':
    app.run(debug=True)