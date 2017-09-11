from flask import Flask, session, redirect, escape, url_for, request, render_template, flash, make_response, send_from_directory, jsonify
import mysql.connector
import jwt 
import datetime
from functools import wraps
from flask_jwt import JWT, jwt_required, current_identity
import sys

from db import Database
from recent_jobposting_class import RecentJob
from dynamic_form_class import Dynamicformdata
from jobseeker_register_class import JobseekerRegister
from registration_forms import RegistrationForms
from flask_paginate import Pagination, get_page_parameter
import json
import os
import datetime

app=Flask(__name__,template_folder='../templates',static_folder='static')
sys.path.insert(r'/var/www/youproject/libs')
#sys.path.insert='/var/www/youproject/libs'
data=Database()
cur,conn=data.connection()
form_data=Dynamicformdata()
js_obj=JobseekerRegister()
rf_obj=RegistrationForms()
recent_job = RecentJob()
keyword = ''

app.config['UPLOAD_FOLDER'] = '/var/www/yourproject/libs/resumes/'
app.config['SECRET_KEY'] = 'super-secret'

class onestop():

    def pro_token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            #print('insdie wraps')		
            token = session.get('token')
            if not token:
                print('Invalid Token')
                return render_template('providers/providers_login.html')
            try:
                tkn_data = jwt.decode(token, app.config['SECRET_KEY'])
                
            except:
                print('Oops Token expired')
                return render_template('providers/providers_login.html')
            return f(*args, **kwargs)
        return decorated


    @app.route('/providers')
    def providers():
        return render_template('providers/providers_intro.html')

		
    @app.route('/providers_profile')
    @pro_token_required
    def providers_profile():
        
        providername=session['v_providername']
        v_provider_id=session['v_provider_id']
        cur.execute("SELECT ProviderName, BusinessName, IDValue, Approved, FirstName, LastName, Phone, Address, Email, City, Zip, Website, HaveLicense, StateExempt, CorporateName, CreatedON, Password FROM trainingproviders WHERE ProviderID=%s" % v_provider_id)
        acinfo = cur.fetchone()
      
        cur.execute("SELECT SemesterYear FROM trainingsemesters WHERE ProviderID=%s group by SemesterYear order by SemesterYear asc" % v_provider_id);
        data={}
        years=cur.fetchall()
       
        for yr in years:
            cur.execute("SELECT  ts.SemesterID, ts.SemesterName, ts.SemesterYear, count(tcs.CourseSessionID) courses FROM trainingsemesters ts left join trainingcoursesessions tcs on ts.SemesterID = tcs.SemesterID WHERE ts.ProviderID=%s  and ts.SemesterYear=%s GROUP BY SemesterName ORDER BY Sequence ASC" %(v_provider_id, yr[0]))
            semyeardata = cur.fetchall()
            data[yr[0]]=semyeardata
       
        cur.execute("SELECT tc.CourseID, tc.CourseTitle, tc.CourseCode ,count(tcs.CourseSessionID ) offerings FROM trainingcourses tc left join trainingcoursesessions tcs on tc.CourseID = tcs.CourseID WHERE tc.ProviderID=%s group by tc.CourseID" % v_provider_id)
        cours = cur.fetchall()
                 
				
        cur.execute("SELECT * FROM trainingsemesters WHERE ProviderID=%s group by SemesterYear order by SemesterYear asc"% v_provider_id)
        select_semyears = cur.fetchall()
        select_semyears_count = cur.rowcount
        			
        cur.execute("SELECT * FROM trainingcourses WHERE ProviderID=%s" % v_provider_id)
        select_course = cur.fetchall()
        select_course_count = cur.rowcount
          
        if select_semyears_count > 0 and select_course_count > 0:
            hasCourseandSemester="Y"
        else:
            hasCourseandSemester="N"

        cur.execute("SELECT SemesterID, SemesterName, SemesterYear, Sequence FROM trainingsemesters WHERE ProviderID=%s order by SemesterYear asc" % v_provider_id)
        hasCouoffsem = cur.fetchall()
        hasCouoffsemCount = cur.rowcount
        sesData={}
        appData={}
        for semyear1 in hasCouoffsem:
            SemesterID = semyear1[0]
                        
            cur.execute('SELECT tcs.CourseSessionID,tcs.CourseID,tcs.SemesterID,tcs.CourseCost,tcs.StartDate ,tcs.EndDate,tcs.Approved,tcs.Section,tcs.Active,tc.CourseTitle FROM trainingcoursesessions tcs left join trainingcourses tc on tcs.CourseID=tc.CourseID where tcs.SemesterID=%s' %SemesterID)
            hasCouoffses = cur.fetchall()
            sesData[SemesterID]=hasCouoffses
            
            for fetchcouses5 in hasCouoffses:
                CourseSessionID = fetchcouses5[0]
                
                coursesessionid = CourseSessionID
                cur.execute("SELECT count(*) as noofapplicants from ita where CourseSessionID= %s" %coursesessionid)
                applicants = cur.fetchall()
                appData[coursesessionid]=applicants
				
                cur.execute("SELECT DayOfWeek FROM trainingcoursesessiondays where CourseSessionID=%s" %coursesessionid)
                
                getSes_Days = cur.fetchall()
                dayscount = cur.rowcount

                for getSes_Day in getSes_Days:
                    getSes_Day1 = getSes_Day[0]
           
                WeekDays = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

        cur.execute("select i.ApplicationID, i.ProfileID, tcs.CourseSessionID, tcs.StartDate, tcs.EndDate, tc.CourseTitle, p.first_name, p.last_name from ita i left join trainingcoursesessions tcs on i.CourseSessionID=tcs.CourseSessionID left join trainingcourses tc on tcs.CourseID=tc.CourseID left join profiles p on i.ProfileID = p.profile_id WHERE i.Approved=1 and tc.ProviderID=%s" % v_provider_id)

        approveditas = cur.fetchall()
			
        return render_template('providers/providers_profile.html', data=data, providername=providername, acinfo=acinfo, cours=cours, get_course5=select_course, hasCourseandSemester=hasCourseandSemester, hasCouoffsem=hasCouoffsem, hasCouoffsemCount=hasCouoffsemCount, SemesterID=SemesterID, hasCouoffses=hasCouoffses, appData=appData, getSes_Days=getSes_Days, dayscount=dayscount, WeekDays=WeekDays, sesData=sesData, approveditas=approveditas)

		
    @app.route('/providers_login',methods =["GET", "POST"])
    def providers_login():
	        	
        if request.method == "GET":
           return render_template('providers/providers_login.html')
        elif request.method == "POST":
            error = ''
            #print('Request Method is',request.method)    
            email_form = request.form['Email']
            password_form = request.form['Password']
            print('Your given email is ...',email_form)
            print('Your given password is ...',password_form)
            
	    #CHECKS IF USERNAME EXSIST
            
            cur.execute("SELECT ProviderID ,ProviderName , Email, Password FROM trainingproviders WHERE email='"+ email_form+"'")		
            row = cur.fetchone()

            if not row is None:
                print(email_form + '...YOU ARE LOGGED IN ...!!!')
                v_provider_id=row[0]
                print('ProviderID from DB :',v_provider_id)
                v_providername=row[1]
                print('ProviderName from DB :',v_providername)
                v_email=row[2]
                v_password=row[3]
                                           
                if password_form == v_password:
                    token = jwt.encode({'email' : v_email, 'password' : v_password, 'v_provider_id' : v_provider_id, 'Providername': v_providername, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=900)}, app.config['SECRET_KEY'], algorithm='HS256')
                    print('token created:',token)
                    tkn = json.dumps({'token' :  token.decode('UTF-8'),'email' : v_email, 'password' : v_password, 'v_provider_id' : v_provider_id, 'Providername': v_providername})
                    tkdcode = jwt.decode(token, app.config['SECRET_KEY'])
                    print('token decode:',tkdcode)
                    					
					
                    session['token']=token
                    session['v_providername']=v_providername
                    session['v_provider_id']=v_provider_id
					
                    return redirect(url_for('providers_profile'))
                return 'Invalid ID or password1'
            else:
                return 'Invalid ID or password2'
        else:
            print(email_form + '...USER DOESNOT EXISTS..!!!')
            return 'Invalid ID or password3'


    @app.route('/semdel',methods =["GET", "POST"])
    @pro_token_required
    def semdel():
        if request.method == "GET":
            return "Worng semdel Method"

        elif request.method == "POST":
            error = ''
            print('semdel request Method is',request.method)
            
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            print('provider_id semdel in',v_provider_id)
            SemesterID_form = request.form['SemesterID']
			
            cur.execute("DELETE from trainingsemesters WHERE SemesterID =%s" % (SemesterID_form))
            
            msg="Semester deleted."
            conn.commit()
        return redirect(url_for('providers_profile', msg=msg))
		

    @app.route('/semedit',methods =["GET", "POST"])
    @pro_token_required
    def semedit():
        if request.method == "GET":
            return "Worng semedit Method"

        elif request.method == "POST":
            error = ''
                        
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            SemesterName_form = request.form['SemesterName']
            SemesterID_form = request.form['SemesterID']

            if len(SemesterName_form)>0:
                cur.execute("UPDATE trainingsemesters SET SemesterName ='%s' WHERE  ProviderID =%s and SemesterID =%s" % (SemesterName_form,v_provider_id,SemesterID_form))
                msg="Semester Name updated."
            else:
                msg="Semester Name not updated."
	            
        return redirect(url_for('providers_profile', msg=msg))


    @app.route('/providersemadd',methods =["GET", "POST"])
    @pro_token_required
    def providersemadd():
        if request.method == "GET":
            return "Worng providersemadd Method"

        elif request.method == "POST":
            error = ''
            print('providersemadd request Method is',request.method)
            
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            print('provider_id providersemadd in',v_provider_id)
            SemesterYear_form = request.form['SemesterYear']
            SemesterName_form = request.form['SemesterName']
			
            cur.execute("select max(Sequence) from trainingsemesters where ProviderID=%s and SemesterYear=%s" % (v_provider_id,SemesterYear_form))
            v_sequence=cur.fetchone()
            n_seq=0
            n_seq=v_sequence[0]
            print('v_sequence[0]',v_sequence[0])
            if v_sequence[0] is None:
                n_seq=1
            else:
                n_seq=n_seq+1

            cur.execute("INSERT INTO trainingsemesters(ProviderID,SemesterName, SemesterYear,Sequence) VALUES(%s,%s,%s,%s)",(v_provider_id,SemesterName_form,SemesterYear_form,n_seq))
            print ('Insert query ->', cur)
            conn.commit()
            msg="Semester details have been updated."

        return redirect(url_for('providers_profile', msg=msg))
	
	
    @app.route('/providers_edit',methods =["GET", "POST"])
    @pro_token_required
    def providers_edit():

        if request.method == "GET":
            return "Worng providers_edit Method"

        elif request.method == "POST":
            error = ''
            print('providers_edit request Method is',request.method)
            email_form = request.form['Email']
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            print('provider_id providers_edit in',v_provider_id)
            ProviderName_form = request.form['ProviderName']
            BusinessName_form = request.form['BusinessName']
            CorporateName_form = request.form['CorporateName']
            IDValue_form = request.form['IDValue']
            FirstName_form = request.form['FirstName']
            LastName_form = request.form['LastName']
            Phone_form = request.form['Phone']
            Address_form = request.form['Address']
            Email_form = request.form['Email']
            City_form = request.form['City']
            Zip_form = request.form['Zip']
            Website_form = request.form['Website']
            HaveLicense_form = request.form['HaveLicense']
            StateExempt_form = request.form['StateExempt']
            CurrentPassword_form = request.form['CurrentPassword']
            NewPassword_form = request.form['NewPassword'].strip()
            ConfirmPassword_form = request.form['ConfirmPassword']

            print('NewPassword_form length:',len(NewPassword_form)) 
			
            if len(NewPassword_form) >0:
			    
                if NewPassword_form == ConfirmPassword_form:
                    print ('NewPassword_form and ConfirmPassword_form matches.')
                    msg="NewPassword_form and ConfirmPassword_form matches."
                    CurrentPassword_form = NewPassword_form
                else:
                    print ('Sorry!! New Password and Confirm Password did not match.')
                    msg="Sorry!! New Password and Confirm Password did not match"
            else:
                 print ('Password did not change')
                 msg="Password did not change"

            sqlCur="UPDATE  trainingproviders SET ProviderName='%s', Email='%s', Password='%s', Address='%s', City='%s', Zip='%s', BusinessName='%s', Website='%s', FirstName='%s', LastName='%s', HaveLicense='%s', StateExempt='%s', IDValue='%s' WHERE ProviderID =%s" %(ProviderName_form, Email_form, CurrentPassword_form, Address_form, City_form, Zip_form, BusinessName_form, Website_form, FirstName_form, LastName_form, HaveLicense_form, StateExempt_form, IDValue_form, v_provider_id)
            
            #print ('query ->', sqlCur)
            cur.execute(sqlCur)
            conn.commit()

        return redirect(url_for('providers_profile', msg=msg))
  
          
    @app.route('/pro_logout')
    def pro_logout():
        session.pop('v_providername', None)
        return redirect(url_for('providers'))
		
		
		
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            		
            token = session.get('token')
            if not token:
                
                print('Invalid Token')
                return render_template('login.html')
            try:
                tkn_data = jwt.decode(token, app.config['SECRET_KEY'])
                                
            except:
                print('Oops Token expired')
                return render_template('login.html')
		
            return f(*args, **kwargs)
        return decorated

    @app.route('/jobseeker/')
    def jobseeker_intro():
        recentjob=recent_job.recent_job()   
        return render_template('jobseeker/js_intro.html', recentjob=recentjob)
	
		
    @app.route('/jsprofile', methods=["GET", "POST"])
    @token_required
    def profile():
        return render_template('jobseeker/js_profile.html')
	    
    @app.route('/')
    def index():
        return render_template('index.html')
		
    @app.route('/emp')
    @token_required
    def emp():
        return render_template('emp.html')

    @app.route('/youth')
    @token_required
    def youth():
        return render_template('youth.html')

    @app.route('/job-seeker/jobseeker/')
    #@token_required
    def jobseeker():
        return render_template('jobseeker/js_intro.html')		
      
    @app.route('/login', methods=["GET", "POST"])
    def logintemp():
        if request.method == "GET":
           return render_template('jobseeker/login_page.html')
        elif request.method == "POST":
            error = ''           			
            email_form = request.form['Email']
            password_form = request.form['Password']           
            
	    #CHECKS IF USERNAME EXSIST
            
            cur.execute("SELECT profile_id ,first_name ,last_name ,email, password,registration_type FROM profiles WHERE email='"+ email_form+"'")			
            row = cur.fetchone()            
            if not row is None:                              
                v_profile_id=row[0]                
                v_first_name=row[1]                
                v_last_name=row[2]              
                v_email=row[3]               
                v_password=row[4]                
                v_registration_type=row[5]
                                         
                if password_form == v_password:
                    token = jwt.encode({'email' : v_email, 'password' : v_password, 'profile_id' : v_profile_id, 'first_name': v_first_name,'last_name': v_last_name, 'registration_type': v_registration_type, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=900)}, app.config['SECRET_KEY'], algorithm='HS256')                    
                    tkn = json.dumps({'token' :  token.decode('UTF-8'),'profile_id' : v_profile_id,'email' : v_email,'password' : v_password})
                    tdecode = jwt.decode(token, app.config['SECRET_KEY'])
					
                    session['token']=token
                    session['v_email']=v_email
                    session['v_profile_id']=v_profile_id
					
                    return redirect(url_for('jsprofile'))  
                return 'Invalid ID or password1'
            else:
                return 'Invalid ID or password2'
        else:
            print(email_form + '...USER DOESNOT EXISTS..!!!')
            return 'Invalid ID or password3'
          
    @app.route('/logout')
    def logout():
        session.pop('email', None)
        return redirect(url_for('index'))

    @app.route('/job-seeker/enrolledprograms', methods=["GET"])
    def enrolledprograms():
        return render_template('jobseeker/enrolledprograms.html')
		
    @app.route('/job-seeker/jsmanage', methods=["GET"])
    def jsmanage():
        return render_template('jobseeker/js_manage.html')

    @app.route('/job-seeker/profile_edit/', methods=["GET"])
    @token_required
    def jobseeker_profile_edit():
        return render_template('jobseeker/js_profile_edit.html')

    @app.route('/job-seeker/job-seeker/itastatus/', methods=["GET"])
    def itastatus():
        return render_template('jobseeker/itastatus.html')
		
    @app.route('/job-seeker/job_description/', methods=["GET"])
    @token_required
    def job_description():
        job_id=request.args.get('variable')     
        if job_id:
            job_description=form_data.job_description(job_id)
            return render_template('jobseeker/job_description.html', job_description=job_description)			

    @app.route('/job-seeker/jobsearch/', methods=["GET", "POST"])
    @token_required
    def jobsearch():
        token=session.get('token')
        if token:
            print("token is vaild")
            print("token -----> {}".format(token))
            job_details="View Details"
            print("job_details -----> {}".format(job_details))
            data=jwt.decode(token,app.secret_key)
            profile_id = data['v_profile_id']	    
        else:
            print("token is not vaild")
            print("token -----> {}".format(token))
            job_details="Login to View"
            print("job_details -----> {}".format(job_details))
        if request.method == "GET":
            sectors=form_data.sectors()
            page = 1
            perpage = 10
            keyword = ''
            args_page = request.args.get('page')
            if args_page:
                page  = args_page
            offset = (int(page) - 1) * perpage
            sector_state={'choice':''}
            jobs_limited = recent_job.recent_job(limit=10, offset=offset, keyword=keyword)
            jobs = recent_job.total_jobs(keyword=keyword)
            page = request.args.get(get_page_parameter(), type=int, default=1)
            pagination = Pagination(page=page, total=len(jobs), css_framework='foundation', record_name='jobs',per_page_parameter=perpage)
            return render_template('jobseeker/pagnation.html', jobs=jobs_limited, pagination=pagination, sectors=sectors, keyword=keyword, job_details=job_details, sector_state=sector_state)
        else:
            sectors_data=form_data.sectors()
            page = 1
            perpage = 10

            args_page = request.args.get('page')
            if args_page:
                page  = args_page
            offset = (int(page) - 1) * perpage
            keyword = ''
            keyword_searched = ''
            sector_searched = ''	    
            print("request.form ==", request.form)
            if request.form['keyword'] and request.form['keyword_footage']:
                keyword = request.form['keyword']
            elif request.form['keyword_footage'] and not request.form['keyword']:
                keyword = request.form['keyword_footage']
            elif request.form['keyword'] and not request.form['keyword_footage']:
                keyword = request.form['keyword']
            else:
                keyword = ''
            keyword_searched = keyword		
            sectors = ''
            if request.form['sector'] and request.form['sector_footage']:
                sectors = request.form['sector']
            elif request.form['sector_footage'] and not request.form['sector']:
                sectors = request.form['sector_footage']
            elif request.form['sector'] and not request.form['sector_footage']:
                sectors = request.form['sector']
            else:
                sectors = ''
            sector_searched = sectors				
            sector_state = {'choice':sectors}
            keyword_searched = keyword
            if keyword and sectors:
                keyword = (keyword, sectors)
            elif keyword and not sectors:
                keyword = (keyword, None)
            elif not keyword and sectors:
                keyword = (None, sectors)
            elif not keyword and not sectors:
                keyword = (None, None)
          
            print("!@#$%^",keyword)
            form_data.save_searches(q=keyword_searched,s=sector_searched,ProfileID=profile_id)
            recentjob=recent_job.recent_job()
            jobs_limited = recent_job.recent_job(limit=10, offset=offset, keyword=keyword)
            jobs = recent_job.total_jobs(keyword=keyword)
            page = request.args.get(get_page_parameter(), type=int, default=1)
            pagination = Pagination(page=page, total=len(jobs), css_framework='foundation', record_name='jobs',per_page_parameter=perpage)
            return render_template('jobseeker/pagnation.html', jobs=jobs_limited, pagination=pagination, sectors=sectors_data, keyword=keyword_searched,job_details=job_details,sector_state=sector_state)
					       
    @app.route('/job-seeker/jobsave/', methods=["GET"])
    @token_required
    def jobsave():
        jobid = request.args.get('jobid')    
        if session:
            token=session.get('token')
            if token:
                data=jwt.decode(token,app.secret_key)
                profile_id = data['v_profile_id']
            print ("inside jobsave")
            if profile_id:
                savejob=form_data.save_jobs(JobseekerID=v_profile_id,JobID=jobid)
                savedjobs=form_data.savedjobs(profile_id)	
                flash('This job has been successfully saved in your Saved Jobs area!')		
                return render_template('jobseeker/js_manage.html', savedjobs=savedjobs)
				
    @app.route('/job-seeker/jobapply/',methods=["GET", "POST"])
    @token_required
    def jobapply():
        job_id = request.args.get('job_id')  
        print (job_id)  
        job_id = "2409"
        if session:
            token=session.get('token')
            if token:
                data=jwt.decode(token,app.secret_key)
                profile_id = data['v_profile_id']
            print ("inside jobapply")
            if request.method == "GET":	    
                job_description=form_data.job_description(job_id)
                print ("inside jobapply get ###################")
                print (job_description)
                return render_template('jobseeker/job_apply.html',job_description=job_description)
            else:
                print ("inside jobapply post $$$$$$$$$$$$$$$$$$$")
                resume_id = request.form['resume']
                form_data.apply_job(job_id=job_id,resume_id=resume_id,jobseeker_profile_id=v_profile_id)
                job_description=form_data.job_description(job_id)
                saved_job_count = form_data.saved_job_count(JobseekerID=profile_id,JobID=job_id)	    
                return render_template('jobseeker/job_description.html', job_description=job_description,saved_job_count=saved_job_count)

    @app.route('/job-seeker/jsprofile/', methods=["GET", "POST"])
    @token_required
    def jsprofile():        
        if request.method == "POST":
            print ("inside jsprofile post")
            return render_template('js_profile.html')

        elif request.method == "GET":
            print ("inside jsresume post")
            #js_profile_id=session.get('v_profile_id')
            js_profile_id=session.get('v_profile_id')
            print("jsprofile_profile_id",js_profile_id)          
            cur.execute("SELECT first_name ,last_name,address_line1,address_line2,city,state,zip,email,phone,entity,one_stop_code,preferred_time,salary_expected,times_viewed FROM profiles,jobseekers WHERE profile_id= %s" % js_profile_id)
            user_details= cur.fetchone() 
            recent_searches = form_data.saved_searches(limit=10, js_profile_id=js_profile_id)
            saved_jobs =  form_data.saved_jobs(limit=10, js_profile_id = js_profile_id)
            print('saved_jobs: ',saved_jobs)
            applied_jobs = form_data.applied_jobs(limit=10, js_profile_id = js_profile_id)
            js_resumes = form_data.js_resumes(js_profile_id=js_profile_id)
            return render_template('jobseeker/js_profile.html', recent_searches=recent_searches, saved_jobs=saved_jobs, applied_jobs=applied_jobs,js_resumes=js_resumes,user=user_details)
			
    @app.route('/job-seeker/profile_edit/', methods=["GET","POST"])
    @token_required
    def profile_edit():
        xostates=form_data.states()
        counties=form_data.counties()
        entity=form_data.entity()
        preferredtimes=form_data.preferredtimes()
        salaryranges=form_data.salaryranges()
        securityquestions=form_data.securityquestions()
        sectors=form_data.sectors()      
        if session:
            token=session.get('token')
            if token:
                data=jwt.decode(token,app.secret_key)
                profile_id = data['v_profile_id']
            if request.method == "POST":
               return "Wrong profile_edit Method"
            elif request.method == "GET":
                edit_profile=form_data.edit_profile(profile_id)            
                print("edit_profile --> {}".format(edit_profile)) 
				
                xostates_state = {'choice':edit_profile[0][6]}
                print("xostates_state --> {}".format(xostates_state))
				
                country_state={'choice':edit_profile[0][7]} 
				
                entity_state={'choice':edit_profile[0][11]} 
				
                preferredtimes_state={'choice':edit_profile[0][13]}
                print( "preferredtimes_state --> {}".format(preferredtimes_state))
				
                salaryranges_state={'choice':edit_profile[0][14]}
                print("salaryranges_state --> {}".format(salaryranges_state))

                sector_state={'choice':edit_profile[0][15]}
                print("sector_state --> {}".format(sector_state))

                securityquestions1_state={'choice':edit_profile[0][16]}
                print("securityquestions1_state--> {}".format(securityquestions1_state))

                securityquestions2_state={'choice':edit_profile[0][18]}
                print("securityquestions2_state --> {}".format(securityquestions2_state))
                return render_template('jobseeker/js_profile_edit.html', edit_profile=edit_profile, xostates=xostates, counties=counties, entity=entity, preferredtimes=preferredtimes, salaryranges=salaryranges, securityquestions=securityquestions, sectors=sectors, xostates_state=xostates_state, country_state=country_state,entity_state=entity_state,preferredtimes_state=preferredtimes_state,salaryranges_state=salaryranges_state,securityquestions1_state=securityquestions1_state,securityquestions2_state=securityquestions2_state)			

				
    @app.route('/job-seeker/jsresume/', methods=["GET", "POST"])
    #@token_required    
    def resume():
        if request.method == "POST":
            print ("inside jsresume post")
            return render_template('resume_manage.html')

        elif request.method == "GET":   
            js_profile_id=session.get('v_profile_id')
            js_resumes = form_data.js_resumes(js_profile_id=js_profile_id)
            return render_template('jobseeker/resume_manage.html', js_resumes=js_resumes)

    @app.route('/job-seeker/addresume/', methods=["GET", "POST"])
    @token_required    
    def add_resume():
        if request.method == "POST":
            print ("inside addresume post")
            #js_profile_id = '23916'
            js_profile_id =('v_profile_id')
            file = request.files['file']
            resume_title = request.args.get('ResumeTitle')
            print ("resumeTitle")
            print (resume_title)
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(resume_path)
            print (resume_path)
            form_data.add_resume(resume_title=resume_title,resume_path=resume_path,jobseeker_profile_id=js_profile_id)
            return render_template('jobseeker/add_resume.html')
        elif request.method == "GET":
            print ("inside addresume get")
            return render_template('jobseeker/add_resume.html')

    @app.route('/job-seeker/updateresume/', methods=["GET", "POST"])
    @token_required     
    def updateresume():    
        if request.method == "POST":
            print ("inside updateresume post")
            #js_profile_id = profile_id
            js_profile_id =('v_profile_id')	    
            file = request.files['file']
            resume_title = request.args.get('ResumeTitle')
            resume_id = request.args.get('ResumeId')
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(resume_path)
            print (resume_path)
            form_data.update_resume(resume_id=resume_id,text_resume=resume_title,resume_path=resume_path)
            return render_template('jobseeker/add_resume.html')
        elif request.method == "GET":
            print ("inside updateresume get")
            #js_profile_id = profile_id
            js_profile_id =('v_profile_id')
            js_resumes = form_data.js_resumes(js_profile_id=js_profile_id)
            return render_template('jobseeker/update_resume.html', js_resumes=js_resumes)
			
    @app.route('/job-seeker/editresume/', methods=["GET", "POST"])
    @token_required  
    def editresume():    
        if request.method == "GET":
            print ("inside editresume get")
            #js_profile_id = profile_id
            js_profile_id =('v_profile_id')
            resumeid = request.args.get('resumeid')	    
            print ("resumeid*********************")
            print (resumeid)	    
            js_resumes = form_data.js_resumes(js_profile_id=js_profile_id)
            return render_template('jobseeker/edit_resume.html',resumeid=resumeid)	    
        elif request.method == "POST":
            print ("inside editresume post")
            #js_profile_id = profile_id
            js_profile_id =('v_profile_id')
            file = request.files['file']
            resume_title = request.form['ResumeTitle']
            resume_id = request.args.get('resumeid')
            print ("resumeid%%%%%%%%%%%%%%%%%%")
            print (resume_id)	    	    
            resume_path = os.path.join(appl.config['UPLOAD_FOLDER'], file.filename)
            file.save(resume_path)
            print (resume_path)
            form_data.update_resume(resume_id=resume_id,resume_title=resume_title,resume_path=resume_path)
            js_resumes = form_data.js_resumes(js_profile_id=js_profile_id)
            return render_template('jobseeker/resume_manage.html', js_resumes=js_resumes)

    @app.route('/job-seeker/deleteresume/', methods=["GET", "POST"])
    @token_required   
    def deleteresume():
        if request.method == "GET":
            print ("inside deleteresume get")
            #js_profile_id = profile_id
            js_profile_id =('v_profile_id')
            resumeid = request.args.get('resumeid')	    
            print ("resumeid*********************")
            print (resumeid)	    
            form_data.delete_resume(resume_id=resumeid)
            js_resumes = form_data.js_resumes(js_profile_id=js_profile_id)
            return render_template('jobseeker/resume_manage.html', js_resumes=js_resumes)			

    @app.route('/job-seeker/resumeshow/', methods=["GET", "POST"])
    def resumeshow():
        print ('inside resumeshow')
        #js_profile_id = '23916'
        js_profile_id =('v_profile_id')
        js_resumes = form_data.js_resumes(js_profile_id=js_profile_id)
        #print (js_resumes[len(js_resumes)-1][3])
        #print (js_resumes[3])
        resume_path = js_resumes[len(js_resumes)-1][3]
        print(resume_path)
        return send_from_directory(app.config['UPLOAD_FOLDER'], resume_path.split(appl.config['UPLOAD_FOLDER'])[1]) 
                
 
   #This class renders GET and POST for registration form
    @staticmethod
    @app.route('/job-seeker/jsregister/',methods=["GET","POST"])
    def jobseeker_registration():

        #Render static returns my_json_dump(str): json values

        if request.method == "POST":
            obj_last = rf_obj.register_user(request)
            if obj_last:
                print("Succesfully completed inserted into database -----> {}".format(obj_last))
                return 'Hurray! Registration is successful :)'
            else:
                print("Not succesfully completed, insertion failed -----> {}".format(obj_last))
                return None
                exit(1)
            
        elif request.method == "GET":
            xostates=form_data.states()
            counties=form_data.counties()
            Sectors=form_data.sectors()
            securityquestions=form_data.securityquestions()
            jobcenters=form_data.jobcenters()
            preferredtimes=form_data.preferredtimes()
            salaryranges=form_data.salaryranges()
            entity=form_data.entity()
            customer_partneragencies=form_data.customer_partneragencies()
            return render_template('views/agegroup1.html',state=xostates,county=counties,
                                   sectors=Sectors,securityquestion=securityquestions,
                                   jobcenter=jobcenters,preferredtime=preferredtimes,
                                   salary=salaryranges,Entity=entity,agencies=customer_partneragencies)

if __name__=="__main__":
    #main_obj=register()
    app.run(host='192.168.110.4', debug=True, port=80)
    #main_obj.render_static()

