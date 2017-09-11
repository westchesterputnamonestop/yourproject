#employer page
from flask import Flask, session, redirect, escape, url_for, request, render_template, make_response, send_from_directory
import mysql.connector
import jwt 
import datetime
from functools import wraps
from db import Database
from dynamic_form_class import Dynamicformdata
from jobseeker_register_class import JobseekerRegister
from registration_forms import RegistrationForms
import json

app=Flask(__name__,template_folder='../templates',static_folder='static')
data=Database()
cur,conn=data.connection()
form_data=Dynamicformdata()
js_obj=JobseekerRegister()
rf_obj=RegistrationForms()

app = Flask(__name__,template_folder='../templates',static_folder='static')
conn = mysql.connector.connect(user='root', password='Armlock21@', host='localhost',database='wpos_dev')
cur = conn.cursor()

class onestop:

    @app.route('/emp_intro', methods=["GET","POST"])
    def empintro():
        #cur=conn.cursor()
        cur.execute("select DISTINCT e.sector_name,a.city, a.state,c.last_updated  from jobseekers a inner join jobseekers_jobs b on a.jobseeker_profile_id=b.jobseeker_profile_id inner join resumes c on b.resume_id=c.resume_id and b.jobseeker_profile_id=c.jobseeker_profile_id inner join jobs_sectors d on b.job_id=d.job_id inner join sectors e on d.sector_id=e.sector_id order by c.last_updated desc LIMIT 10")
        print("selected")
        empprofiledata=[]
        print("registered")
        a=cur.fetchall()
        return render_template('emp_intro.html',  a=a)
		
    @app.route('/view_resume', methods=["GET","POST"])
    def view_resume():
        #cur=conn.cursor()
        cur.execute("select DISTINCT e.sector_name,a.city, a.state,c.last_updated  from jobseekers a inner join jobseekers_jobs b on a.jobseeker_profile_id=b.jobseeker_profile_id inner join resumes c on b.resume_id=c.resume_id and b.jobseeker_profile_id=c.jobseeker_profile_id inner join jobs_sectors d on b.job_id=d.job_id inner join sectors e on d.sector_id=e.sector_id order by c.last_updated desc LIMIT 20")
        print("selected")
        empprofiledata=[]
        print("registered")
        a=cur.fetchall()
        return render_template('emp_viewresume.html',  a=a)
   
		
    @app.route('/jsintro/', methods=["GET", "POST"])
    def introduction():
        return render_template('js_intro.html')

    @app.route('/jsprofile', methods=["GET", "POST"])
    def profile():
        return render_template('views/js_profile.html')

    @app.route('/empProfiles', methods=["GET","POST"])
    def empProfiles():
        pid = request.form.get('Empprofileid')
        print("vinnu"+pid)
        val=pid
        cur=conn.cursor()
        cur.execute("select p.profile_id,p.first_name,p.last_name,p.email,p.password,p.security_question1,p.security_answer1,p.security_question2,p.security_answer2,p.registration_type,p.registeration_date,e.employer_profile_id,e.title,e.company_name,e.address_line1,e.address_line2,e.city,e.state,e.zip,e.phone,e.extension,e.phone2,e.fax,e.website_url,e.company_information,e.skills_training_wanted,e.county_id,e.createdon,e.EINNumber,e.Healthcare,e.Readytowork,e.isnewregistration,e.RTWStatus,e.isRTWEmployer,s.sector_id,s.profile_id  from employers e inner join profiles p on e.employer_profile_id=p.profile_id inner join sectors_profiles s on s.profile_id=p.profile_id where e.employer_profile_id=%s" % val)
        empprofiledata=[]
        for row in cur:
            print(row)
        #empprofiledata[]=cur.fetchall()
        #print(len(empprofiledata)) 
        #print (empprofiledata(cur))
        print (row[4])
        return render_template('emp_profile.html',my_ProfileID =row[0],my_first_name =row[1],my_last_name=row[2],my_email=row[3],my_password=row[4],my_security_question1=row[5],my_security_answer1=row[6],my_security_question2=row[7],my_security_answer2=row[8],my_registration_type=row[9],my_registeration_date=row[10],my_employer_profile_id=row[11],my_title=row[12],my_company_name=row[13],my_address_line1=row[14],my_address_line2=row[15],my_city=row[16],my_state=row[17],my_zip=row[18],my_phone=row[19],my_extension=row[20],my_phone2=row[21],my_fax=row[21],my_website_url=row[22],my_company_information=row[23],my_skills_training_wanted=row[24],my_county_id=row[25],my_createdon=row[26],my_EINNumber=row[27],my_Healthcare=row[28],my_Readytowork=row[29],my_isnewregistration=row[30],my_RTWStatus=row[31],my_isRTWEmployer=row[32],my_sector_id=row[33],my_profile_id=row[34], my_empprofiledata=row)
    #print(empprofiledata)
    
   
    @app.route('/profileid', methods=["GET","POST"])
    def profileid():
        cur=conn.cursor()
        cur.execute("SELECT DISTINCT(p.profile_id) FROM profiles as p, employers as e, sectors_profiles as s WHERE e.employer_profile_id = p.profile_id AND p.profile_id = s.profile_id")
        employers=[]
        #print(cur)
        for profile in cur:
            employers.append(profile[0])
        return render_template('emp_id.html',data = employers)
	
	
      
    @app.route('/')
    def index():
        return render_template('views/index.html')	
      
    @app.route('/login', methods =["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template('login.html')
        elif request.method == "POST":
            error = ''
            print('inside login')
            print('Request Method is',request.method)    
            email_form = request.form['Email']
            password_form = request.form['Password']
            print('Your given email is ...',email_form)
            print('Your given password is ...',password_form)
         
	    #CHECKS IF USERNAME EXSIST
            conn = mysql.connector.connect(user='root', password='Armlock21@', host='localhost',database='wpos_dev')
            cur = conn.cursor()
            cur.execute("SELECT profile_id ,first_name ,last_name ,email, password,registration_type FROM profiles WHERE email='"+ email_form+"'")
			
            o = cur.fetchone()
            print('Row count is',o)
            if not o is None:
                
                print(email_form + '...YOU ARE LOGGED IN ...!!!')
                v_profile_id=o[0]
                val=v_profile_id
                print('Your profile_id is :',v_profile_id)
                v_first_name=o[1]
                print('Your first_name is :',v_first_name)
                v_last_name=o[2]
                print('Your last_name is :',v_last_name)
                v_email=o[3]
                print('Your logged in..!!',v_email)
                v_password=o[4]
                print('Your password is :',v_password)
                v_registration_type=o[5]
                print('Your registration_type is :',v_registration_type)
                #global Job Seeker
                val=v_profile_id
            cur=conn.cursor()
            cur.execute("select p.profile_id,p.first_name,p.last_name,p.email,p.password,p.security_question1,p.security_answer1,p.security_question2,p.security_answer2,p.registration_type,p.registeration_date,e.employer_profile_id,e.title,e.company_name,e.address_line1,e.address_line2,e.city,e.state,e.zip,e.phone,e.extension,e.phone2,e.fax,e.website_url,e.company_information,e.skills_training_wanted,e.county_id,e.createdon,e.EINNumber,e.Healthcare,e.Readytowork,e.isnewregistration,e.RTWStatus,e.isRTWEmployer,s.sector_id,s.profile_id  from employers e inner join profiles p on e.employer_profile_id=p.profile_id inner join sectors_profiles s on s.profile_id=p.profile_id where e.employer_profile_id=%s" % val)
                empprofiledata=[]
                for row in cur:
                    print(row)
                #empprofiledata[]=cur.fetchall()
                #print(len(empprofiledata))
                #print (empprofiledata(cur))
                print (row[4])
            return render_template('emp_profile.html',my_ProfileID =row[0],my_first_name =row[1],my_last_name=row[2],my_email=row[3],my_password=row[4],my_security_question1=row[5],my_security_answer1=row[6],my_security_question2=row[7],my_security_answer2=row[8],my_registration_type=row[9],my_registeration_date=row[10],my_employer_profile_id=row[11],my_title=row[12],my_company_name=row[13],my_address_line1=row[14],my_address_line2=row[15],my_city=row[16],my_state=row[17],my_zip=row[18],my_phone=row[19],my_extension=row[20],my_phone2=row[21],my_fax=row[21],my_website_url=row[22],my_company_information=row[23],my_skills_training_wanted=row[25], my_empprofiledata=row)
    #print(empprofiledata)

               
                
                #if password_form == v_password:
                    #token = jwt.encode({'email' : v_email, 'pass' : v_password, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=180)}, app.config['SECRET_KEY'], algorithm='HS256')
                    #tkn = jsonify({'token' : token.decode('UTF-8')})
                    #print('token is:',tkn)
                 #   if v_registration_type == 'Job Seeker':
                  #      htm = 'jobseeker'
                  #  elif v_registration_type == 'Employer':
                   #     htm = 'emp'
                   # elif v_registration_type == 'InternStudent':
                       # htm = 'youth'
                   # return redirect(url_for(htm))
                    #return redirect(url_for(htm), tkn)
                    #return redirect(url_for(htm), jsonify({'token' : token.decode('UTF-8')}))
               # return 'Invalid ID or password1'
           # else:
            #    return 'Invalid ID or password2'

            				
				
		#return 'Enter Password'
        else:
            print(email_form + '...USER DOESNOT EXISTS..!!!')
            return 'Invalid ID or password3'
                
                        
                    
          
    @app.route('/logout')
    def logout():
        session.pop('email', None)
        return redirect(url_for('index'))


                
 
   

if __name__=="__main__":
    
    app.run(host='192.168.110.4', debug=True, port=80)
    

