from flask import Flask, session, redirect, escape, url_for, request, render_template, make_response, send_from_directory, jsonify
import mysql.connector
import jwt 
import datetime
from functools import wraps
from flask_jwt import JWT, jwt_required, current_identity
from db import Database
from recent_jobposting_class import RecentJob
from dynamic_form_class import Dynamicformdata
from jobseeker_register_class import JobseekerRegister
from registration_forms import RegistrationForms
from flask_paginate import Pagination, get_page_parameter
import json
import os

app=Flask(__name__,template_folder='../templates',static_folder='static')
data=Database()
cur,conn=data.connection()
form_data=Dynamicformdata()
js_obj=JobseekerRegister()
rf_obj=RegistrationForms()
recent_job = RecentJob()
keyword = ''
app.config['UPLOAD_FOLDER'] = '/var/www/yourproject/libs/resumes'
app.config['SECRET_KEY'] = 'super-secret'


class onestop():		
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            		
            token = session.get('token')
            if not token:
                
                print('Invalid Token')
                return render_template('jobseeker/login.html')
            try:
                tkn_data = jwt.decode(token, app.config['SECRET_KEY'])
                                
            except:
                print('Oops Token expired')
                return render_template('jobseeker/login.html')
		
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

    @app.route('/jobseeker')
    @token_required
    def jobseeker():
        return render_template('jobseeker/js_intro.html')		
      
    @app.route('/logintemp', methods=["GET", "POST"])
    def login_temp():
        if request.method == "GET":
           return render_template('jobseeker/login_page.html')
        elif request.method == "POST":
            error = ''
            print('Request Method is',request.method)
            print('email of form is',request.form['Email']) 			
            email_form = request.form['Email']
            password_form = request.form['Password']
            print('Your given email is ...',email_form)
            print('Your given password is ...',password_form)
            
	    #CHECKS IF USERNAME EXSIST
            
            cur.execute("SELECT profile_id ,first_name ,last_name ,email, password,registration_type FROM profiles WHERE email='"+ email_form+"'")
			
            row = cur.fetchone()
            print('Row count is',row)
            if not row is None:
                
                print(email_form + '...YOU ARE LOGGED IN ...!!!')
                v_profile_id=row[0]
                print('Your profile_id from DB :',v_profile_id)
                v_first_name=row[1]
                print('Your first_name from DB :',v_first_name)
                v_last_name=row[2]
                print('Your last_name from DB :',v_last_name)
                v_email=row[3]
                print('Your logged in..!!',v_email)
                v_password=row[4]
                print('Your password from DB :',v_password)
                v_registration_type=row[5]
                print('Your registration_type from DB :',v_registration_type)
                           
                if password_form == v_password:
                    token = jwt.encode({'email' : v_email, 'password' : v_password, 'profile_id' : v_profile_id, 'first_name': v_first_name,'last_name': v_last_name, 'registration_type': v_registration_type, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=900)}, app.config['SECRET_KEY'], algorithm='HS256')
                    print('token created:',token)
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

    @app.route('/enrolledprograms', methods=["GET"])
    def enrolledprograms():
        return render_template('jobseeker/enrolledprograms.html')
		
    @app.route('/jsmanage', methods=["GET"])
    def jsmanage():
        return render_template('jobseeker/js_manage.html')

    @app.route('/profile_edit/', methods=["GET"])
    #@token_required(method='profile_edit')
    def jobseeker_profile_edit():
        return render_template('jobseeker/js_profile_edit.html')

    @app.route('/itastatus/', methods=["GET"])
    def itastatus():
        return render_template('jobseeker/itastatus.html')
		
    @app.route('/job_description/', methods=["GET"])
    #@token_required(method='job_description')
    def job_description():
        job_id=request.args.get('variable')     
        if job_id:
            job_description=form_data.job_description(job_id)
            return render_template('jobseeker/job_description.html', job_description=job_description)

    @app.route('/job_description/job_save', methods=["GET"])
    @token_required
    def job_save():
        print("Came into job_save")
        job_id=request.args.get('variable')
        if session:
            print("Came into job_save and session is valid --> {}".format(session))
            token=session.get('token')
            if token:
                print("Came into job_save and session is valid and have tocket --> {}".format(token))
                data=jwt.decode(token,application.secret_key)
                print("Came into job_save and session is valid and have tocket and parsing data --> {}".format(data))
              # profile_id = data['v_profile_id']
                print(
                    "Came into job_save and session is valid and have tocket and parsing data and getting profile_id --> {}".format(profile_id))
                if job_id:
                    saved_job.saved_jobs(user_id=profile_id, job_id=job_id)
                    flash('You have saved job successfully')
                    job_description=form_data.job_description(job_id)
                    print("job_description ----> {}".format(job_description))
                    return render_template('jobseeker/job_description.html',job_description=job_description)
			


    @app.route('/jobsearch/', methods=["GET", "POST"])
    @token_required
    def jobsearch():
        token=session.get('token')
        if token:
            print("token is vaild")
            print("token -----> {}".format(token))
            job_details="View Details"
            print("job_details -----> {}".format(job_details))
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
            print("request.form ==", request.form)
            if request.form['keyword'] and request.form['keyword_footage']:
                keyword = request.form['keyword']
            elif request.form['keyword_footage'] and not request.form['keyword']:
                keyword = request.form['keyword_footage']
            elif request.form['keyword'] and not request.form['keyword_footage']:
                keyword = request.form['keyword']
            else:
                keyword = ''
            sectors = ''
            if request.form['sector'] and request.form['sector_footage']:
                sectors = request.form['sector']
            elif request.form['sector_footage'] and not request.form['sector']:
                sectors = request.form['sector_footage']
            elif request.form['sector'] and not request.form['sector_footage']:
                sectors = request.form['sector']
            else:
                sectors = ''
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
            jobs_limited = recent_job.recent_job(limit=10, offset=offset, keyword=keyword)
            jobs = recent_job.total_jobs(keyword=keyword)
            page = request.args.get(get_page_parameter(), type=int, default=1)
            pagination = Pagination(page=page, total=len(jobs), css_framework='foundation', record_name='jobs',per_page_parameter=perpage)

            return render_template('jobseeker/pagnation.html', jobs=jobs_limited, pagination=pagination, sectors=sectors_data, keyword=keyword_searched, job_details=job_details,sector_state=sector_state)
					       
			
    @app.route('/jsprofile/', methods=["GET", "POST"])
    @token_required
    def jsprofile():
        if session:
            token=session.get('token')
            if token:
                data=jwt.decode(token,app.secret_key)
                profile_id = data['v_profile_id']
        if request.method == "POST":
            print ("inside jsprofile post")
            return render_template('jobseeker/js_profile.html')

        elif request.method == "GET":
            if profile_id:
                js_profile_id=profile_id
            else:
                js_profile_id = ''
            cur.execute("SELECT first_name ,last_name,address_line1,address_line2,city,state,zip,email,phone,entity,one_stop_code,preferred_time,salary_expected,times_viewed,profile_id FROM profiles,jobseekers WHERE profile_id= %s" % js_profile_id)
            user_details= cur.fetchone()
            recent_searches = form_data.saved_searches(limit=10, js_profile_id=js_profile_id)
            saved_jobs =  form_data.saved_jobs(limit=10, js_profile_id=js_profile_id)
            applied_jobs = form_data.applied_jobs(limit=10, js_profile_id=js_profile_id)
            return render_template('jobseeker/js_profile.html', recent_searches=recent_searches, saved_jobs=saved_jobs, applied_jobs=applied_jobs, user=user_details)

    @app.route('/jsresume/', methods=["GET", "POST"])
    #@token_required    
    def resume():
        if request.method == "POST":
            print ("inside jsresume post")
            return render_template('resume_manage.html')

        elif request.method == "GET":   
            js_profile_id=session.get('v_profile_id')
            js_resumes = form_data.js_resumes(js_profile_id=js_profile_id)
            return render_template('jobseeker/resume_manage.html', js_resumes=js_resumes)



    @app.route('/addresume/', methods=["GET", "POST"])
    #@token_required    
    def add_resume():
        if request.method == "POST":
            print ("inside addresume post")
            #js_profile_id = request.args.get('js_profile_id')
           #js_profile_id = '23916'
            js_profile_id=session.get('v_profile_id')
            file = request.files['file']
            resume_title = request.args.get('ResumeTitle')
            print ("resumeTitle")
            print (resume_title)
            resume_path = os.path.join(application.config['UPLOAD_FOLDER'], file.filename)
            file.save(resume_path)
            print (resume_path)
            form_data.add_resume(text_resume=resume_title,resume_path=resume_path,jobseeker_profile_id=js_profile_id)
            return render_template('add_resume.html')
        elif request.method == "GET":
            print ("inside addresume get")
            return render_template('jobseeker/add_resume.html')

    @app.route('/resumeshow/', methods=["GET", "POST"])
    def resumeshow():
        print ('inside resumeshow')
        #s_profile_id = '23916'
        js_profile_id=session.get('v_profile_id')
        js_resumes = form_data.js_resumes(js_profile_id=js_profile_id)
        #print (js_resumes[len(js_resumes)-1][3])
        #print (js_resumes[3])
        resume_path = js_resumes[len(js_resumes)-1][3]
        print(resume_path)
        return send_from_directory(application.config['UPLOAD_FOLDER'], resume_path.split(application.config['UPLOAD_FOLDER'])[1])

    @app.route('/updateresume/', methods=["GET", "POST"])
    def update_resume():
        if request.method == "POST":
            print ("inside updateresume post")
            #js_profile_id = request.args.get('js_profile_id')
            #s_profile_id = '23916'
            js_profile_id=session.get('v_profile_id')
            file = request.files['file']
            resume_title = request.args.get('ResumeTitle')
            resume_id = request.args.get('ResumeId')
            resume_path = os.path.join(application.config['UPLOAD_FOLDER'], file.filename)
            file.save(resume_path)
            print (resume_path)
            form_data.update_resume(resume_id=resume_id,text_resume=resume_title,resume_path=resume_path)
            return render_template('jobseeker/add_resume.html')
        elif request.method == "GET":
            print ("inside updateresume get")
            return render_template('jobseeker/add_resume.html') 
                
 
   #This class renders GET and POST for registration form
    @staticmethod
    @app.route('/jsregister/',methods=["GET","POST"])
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
							
    @app.route('/profile_edit/', methods=["GET","POST"])
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
                data=jwt.decode(token,application.secret_key)
                profile_id = data['v_profile_id']
            if request.method == "POST":
               return "Worng profile_edit Method"
            elif request.method == "GET":
                edit_profile=form_data.edit_profile(profile_id)               
                print("edit_profile --> {}".format(edit_profile))
                print("**************************")
                xostates_state = {'choice':edit_profile[0][6]}
                print("xostates_state --> {}".format(xostates_state))
				
                country_state={'choice':edit_profile[0][7]}
                print("country_state--> {}".format(country_state))
				
                entity_state={'choice':edit_profile[0][11]}
                print("entity_state --> {}".format(entity_state))
				
                preferredtimes_state={'choice':edit_profile[0][13]}
                print("preferredtimes_state --> {}".format(preferredtimes_state))
				
                salaryranges_state={'choice':edit_profile[0][14]}
                print("salaryranges_state --> {}".format(salaryranges_state))
				
                securityquestions1_state={'choice':edit_profile[0][16]}
                print("securityquestions1_state--> {}".format(securityquestions1_state))
				
                securityquestions2_state={'choice':edit_profile[0][18]}
                print("securityquestions2_state --> {}".format(securityquestions2_state))
                return render_template('jobseeker/js_profile_edit.html', edit_profile=edit_profile, xostates=xostates, counties=counties, entity=entity, preferredtimes=preferredtimes, salaryranges=salaryranges, securityquestions=securityquestions, sectors=sectors, xostates_state=xostates_state, country_state=country_state,entity_state=entity_state,preferredtimes_state=preferredtimes_state,salaryranges_state=salaryranges_state,securityquestions1_state=securityquestions1_state,securityquestions2_state=securityquestions2_state)

if __name__=="__main__":
    #main_obj=register()
    app.run(host='192.168.110.4', debug=True, port=80)
    #main_obj.render_static()

