from flask import Flask, session, redirect, escape, url_for, flash, request, render_template, make_response, send_from_directory, jsonify
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
import datetime

app = Flask(__name__,template_folder='../templates',static_folder='../static')
app.config['SECRET_KEY'] = 'super-secret'
app.config['UPLOAD_FOLDER'] = '/var/www/yourproject/libs/resumes/'
data = Database()
cur, conn = data.connection()
form_data=Dynamicformdata()
js_obj=JobseekerRegister()
rf_obj=RegistrationForms()
recent_job = RecentJob()
keyword = ''

class onestop():

    def pro_token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            		
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


    @app.route('/providers/providers_reg',methods =["GET", "POST"])
    def providers_reg():
        if request.method == "GET":
            return render_template('providers/providers_reg.html')

        elif request.method == "POST":
            error = ''
            print('providers_reg request Method is',request.method)
            ProviderName_form = request.form['ProviderName']
            Email_form = request.form['Email']
            Phone_form = request.form['Phone']
            Address_form = request.form['Address']
            City_form = request.form['City']
            State_form = request.form['State']
            Zip_form = request.form['Zip']
            Website_form = request.form['Website']
            BusinessName_form = request.form['BusinessName']
            CorporateName_form = request.form['CorporateName']
            IDType_form = request.form['IDType']
            IDValue_form = request.form['IDValue']
            HaveLicense_form = request.form['HaveLicense']
            StateExempt_form = request.form['StateExempt']
            FirstName_form = request.form['FirstName']
            LastName_form = request.form['LastName']
            DesiredPassword_form = request.form['DesiredPassword']
            ConfirmPassword_form = request.form['ConfirmPassword']

            if DesiredPassword_form == ConfirmPassword_form:
                Password_form = ConfirmPassword_form
            else:
                msg = 'DesiredPassword and ConfirmPassword are not same.'

            
            cur.execute("INSERT INTO trainingproviders (ProviderName,Email,Password,Phone,Address,City,Zip,BusinessName,CorporateName,Website,FirstName,LastName,IDType,IDValue,HaveLicense,StateExempt) VALUES('%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(ProviderName_form,Email_form,Password_form,Phone_form,Address_form,City_form,Zip_form,BusinessName_form,CorporateName_form,Website_form,FirstName_form,LastName_form,IDType_form,IDValue_form,HaveLicense_form,StateExempt_form))
			
            conn.commit()
            msg="Thanks for registering."

            cur.execute("select ProviderID from trainingproviders where Email='"+ Email_form+"'")
            provider_id = cur.fetchone()
            print('provider_id',provider_id)
            
            session['email_form']=Email_form, 
            session['password_form']=Password_form, 
            session['providername']=ProviderName_form,
            session['v_provider_id']=provider_id,
        
        return redirect(url_for('reg_providers_profile', msg=msg))
		
		
    @app.route('/reg_providers_profile')
    @pro_token_required
    def reg_providers_profile():
        
        providername=session['v_providername']
        v_provider_id=session['v_provider_id']
        cur.execute("SELECT ProviderName, BusinessName, IDValue, Approved, FirstName, LastName, Phone, Address, Email, City, Zip, Website, HaveLicense, StateExempt, CorporateName, CreatedON, Password FROM trainingproviders WHERE ProviderID=%s" % v_provider_id)
        acinfo = cur.fetchone()
      
        cur.execute("SELECT SemesterYear FROM trainingsemesters WHERE ProviderID=%s group by SemesterYear order by SemesterYear asc" % v_provider_id)
        data={}
        years=cur.fetchall()
        semCnt={}
        for yr in years:
            cur.execute("SELECT  ts.SemesterID, ts.SemesterName, ts.SemesterYear, count(tcs.CourseSessionID) courses, ts.Sequence FROM trainingsemesters ts left join trainingcoursesessions tcs on ts.SemesterID = tcs.SemesterID WHERE ts.ProviderID=%s  and ts.SemesterYear=%s GROUP BY SemesterName ORDER BY Sequence ASC" %(v_provider_id, yr[0]))
            semyeardata = cur.fetchall()
            data[yr[0]]=semyeardata
            semCnt[yr[0]]=cur.rowcount
       
        cur.execute("SELECT tc.CourseID, tc.CourseTitle, tc.CourseCode ,count(tcs.CourseSessionID ) offerings FROM trainingcourses tc left join trainingcoursesessions tcs on tc.CourseID = tcs.CourseID WHERE tc.ProviderID=%s group by tc.CourseID" % v_provider_id)
        cours = cur.fetchall()
                 
				
        cur.execute("SELECT * FROM trainingsemesters WHERE ProviderID=%s group by SemesterYear order by SemesterYear asc"% v_provider_id)
        select_semyears = cur.fetchall()
        select_semyears_count = cur.rowcount

        cur.execute("SELECT SemesterID,SemesterName,SemesterYear FROM trainingsemesters WHERE ProviderID=%s order by SemesterYear desc" % v_provider_id)
        selsem = cur.fetchall()

        cur.execute("SELECT CourseID,CourseCode,CourseTitle FROM trainingcourses WHERE ProviderID=%s" % v_provider_id)
        selcrs = cur.fetchall()

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
        sesDys={}
        dysCnt={}
        SemesterID=-1
        hasCouoffses=-1
        WeekDays = []
        for semyear1 in hasCouoffsem:
            SemesterID = semyear1[0]
            
            cur.execute("SELECT tcs.CourseSessionID,tcs.CourseID,tcs.SemesterID,concat('$',tcs.CourseCost),date(tcs.StartDate) ,date(tcs.EndDate),tcs.Approved,tcs.Section,tcs.Active, tc.CourseTitle, tc.CourseCode FROM trainingcoursesessions tcs left join trainingcourses tc on tcs.CourseID=tc.CourseID where tcs.SemesterID=%s" %SemesterID)
            hasCouoffses = cur.fetchall()
            sesData[SemesterID]=hasCouoffses
            
            for fetchcouses in hasCouoffses:
                CourseSessionID = fetchcouses[0]
                
                coursesessionid = CourseSessionID
                cur.execute("SELECT count(*) as noofapplicants from ita where CourseSessionID= %s" %coursesessionid)
                applicants = cur.fetchall()
                appData[coursesessionid]=applicants
				
                cur.execute("SELECT DayOfWeek FROM trainingcoursesessiondays where CourseSessionID=%s" %coursesessionid)
                 
                sesDys[coursesessionid]= cur.fetchall()
                dysCnt[coursesessionid] = cur.rowcount
                                
                WeekDays = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]


        cur.execute("select i.ApplicationID, i.ProfileID, tcs.CourseSessionID, date(tcs.StartDate), date(tcs.EndDate), tc.CourseTitle, p.first_name, p.last_name from ita i left join trainingcoursesessions tcs on i.CourseSessionID=tcs.CourseSessionID left join trainingcourses tc on tcs.CourseID=tc.CourseID left join profiles p on i.ProfileID = p.profile_id WHERE i.Approved=1 and tc.ProviderID=%s" % v_provider_id)

        approveditas = cur.fetchall()
        
			
        return render_template('providers/providers_profile.html', data=data, semCnt=semCnt, providername=providername, acinfo=acinfo, cours=cours, get_course=select_course, hasCourseandSemester=hasCourseandSemester, hasCouoffsem=hasCouoffsem, hasCouoffsemCount=hasCouoffsemCount, SemesterID=SemesterID, hasCouoffses=hasCouoffses, appData=appData, selsem=selsem, selcrs=selcrs, sesDys=sesDys, dysCnt=dysCnt, WeekDays=WeekDays, sesData=sesData, approveditas=approveditas)

	

    @app.route('/providers/cors_offer_del',methods =["GET", "POST"])
    @pro_token_required
    def cors_offer_del():
        if request.method == "GET":
            return "Worng cors_offer_del Method"

        elif request.method == "POST":
            error = ''
            print('cors_offer_del request Method is',request.method)
            
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            
            CourseID_form = request.form['Course']
                        
            cur.execute("Delete From trainingcourses WHERE CourseID =%s" % (CourseID_form))
            conn.commit()
            print("Deleted code and title")
            msg="Code and title deleted suceesfully."
			
        return redirect(url_for('providers_profile', msg=msg))

		
    @app.route('/providers/cors_offer_edit',methods =["GET", "POST"])
    @pro_token_required
    def cors_offer_edit():
        if request.method == "GET":
            return "Worng cors_offer_edit Method"

        elif request.method == "POST":
            error = ''
            print('cors_offer_edit request Method is',request.method)
            
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            Course_form = request.form['Course']
            cousesid_form = request.form['cousesid']
            Section_form = request.form['Section']
            StartDate_form = request.form['StartDate']
            EndDate_form = request.form['EndDate']
            CourseCost_form = request.form['CourseCost']
            Active_form = request.form['Active']
            DayOfWeek_form = request.form['DayOfWeek[]']
                        
            cur.execute("update trainingcoursesessions  set CourseID=%s, CourseCost='%s', StartDate=TIMESTAMP('%s'), EndDate=TIMESTAMP('%s'), Section='%s', Active='%s' where CourseSessionID=%s" %(Course_form, CourseCost_form.replace('$','',1), StartDate_form, EndDate_form, Section_form, Active_form, cousesid_form))

            cur.execute("delete from trainingcoursesessiondays  where CourseSessionID = %s" %(cousesid_form))
            cur.execute("insert into trainingcoursesessiondays SET CourseSessionID=%s, DayOfWeek=%s" %(cousesid_form, DayOfWeek_form))
            conn.commit()
            msg="Code and title updated suceesfully."
                        
        return redirect(url_for('providers_profile', msg=msg))
		
		
    @app.route('/providers/cors_offer_add',methods =["GET", "POST"])
    @pro_token_required
    def cors_offer_add():
        if request.method == "GET":
            return "Worng cors_offer_add Method"

        elif request.method == "POST":
            error = ''
            msg = ''
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            print('provider_id cors_offer_add in',v_provider_id)
            
            Semester_form = request.form['Semester']
            Course_form = request.form['Course']
            Section_form = request.form['Section']
            StartDate_form = request.form['StartDate']
            EndDate_form = request.form['EndDate']
            CourseCost_form = request.form['CourseCost']
            Active_form = request.form['Active']
            DayOfWeek_form = request.form.getlist('DayOfWeek')
            
            cur.execute(("INSERT INTO trainingcoursesessions  SET SemesterID=%s, CourseID=%s, CourseCost =%s ,StartDate=TIMESTAMP('%s'),EndDate =TIMESTAMP('%s'),Approved = 0,Section =%s,Active =%s") % (Semester_form,Course_form,CourseCost_form,StartDate_form,EndDate_form,Section_form,Active_form))
    
            cur.execute(("SELECT tcs.CourseSessionID FROM trainingcoursesessions tcs left join trainingcourses tc on tcs.CourseID=tc.CourseID WHERE tc.ProviderID=%s and tcs.CourseID=%s and tcs.SemesterID=%s")%(v_provider_id,Course_form,Semester_form))
            corsesid=cur.fetchone()
                        
            cur.execute("DELETE FROM trainingcoursesessiondays WHERE CourseSessionID =%s"%(corsesid[0]))
            
            for dy in DayOfWeek_form:
                
                cur.execute("INSERT INTO trainingcoursesessiondays SET CourseSessionID =%s, DayOfWeek =%s"%(corsesid[0],dy))
                conn.commit()
                msg="Course Offerings details added suceesfully."
                        
        return redirect(url_for('providers_profile', msg=msg))

		
    @app.route('/providers/moveupanddown',methods =["GET", "POST"])
    @pro_token_required
    def moveupanddown():
        if request.method == "GET":
            return "Worng moveupanddown Method"

        elif request.method == "POST":
            error = ''
            msg = ''
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            flag_form = request.form['flag']
            SemesterID_form = request.form['SemesterID']

            cur.execute("SELECT SemesterYear, Sequence, SemesterID FROM trainingsemesters  WHERE  SemesterID =%s" %(SemesterID_form))
            curRow = cur.fetchone()
            
            if curRow is not None :
                if flag_form == 'up':
                    cur.execute("SELECT SemesterYear, Sequence, SemesterID FROM trainingsemesters  WHERE  Sequence<%s AND SemesterYear=%s  order by Sequence DESC" %(curRow[1],curRow[0]))
                else:
                    cur.execute("SELECT SemesterYear, Sequence, SemesterID FROM trainingsemesters  WHERE  Sequence>%s AND SemesterYear=%s order by Sequence ASC" %(curRow[1],curRow[0]))
   
                tgtRow=cur.fetchone()

                cur.execute("UPDATE trainingsemesters SET Sequence=%s WHERE  SemesterID =%s" %(curRow[1],tgtRow[2]))
                cur.execute("UPDATE trainingsemesters SET Sequence=%s WHERE  SemesterID =%s" %(tgtRow[1],curRow[2]))
                conn.commit()
                msg="Suceesfully moveupanddown"
            
        return redirect(url_for('providers_profile', msg=msg))


    @app.route('/providers/code_title_del',methods =["GET", "POST"])
    @pro_token_required
    def code_title_del():
        if request.method == "GET":
            return "Worng code_title_del Method"

        elif request.method == "POST":
            error = ''
            print('code_title_del request Method is',request.method)
            
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            print('provider_id code_title_del in',v_provider_id)
            CourseID_form = request.form['CourseID']
                        
            cur.execute("Delete From trainingcourses WHERE CourseID =%s" % (CourseID_form))
            conn.commit()
            msg="Code and title deleted suceesfully."
                        
        return redirect(url_for('providers_profile', msg=msg))
		

    @app.route('/providers/code_title_edit',methods =["GET", "POST"])
    @pro_token_required
    def code_title_edit():
        if request.method == "GET":
            return "Worng code_title_edit Method"

        elif request.method == "POST":
            error = ''
            msg = ''
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            CourseCode_form = request.form['CourseCode']
            CourseTitle_form = request.form['CourseTitle']
            CourseID_form = request.form['CourseID']
            
            if len(CourseTitle_form)>0:
                cur.execute("UPDATE trainingcourses SET ProviderID =%s, CourseCode =%s, CourseTitle = '%s' WHERE  CourseID =%s" %(v_provider_id,CourseCode_form,CourseTitle_form,CourseID_form))
                conn.commit()
                msg="Code and title updated suceesfully."
            else:
                msg="You must provide the course title"
            
        return redirect(url_for('providers_profile', msg=msg))


    @app.route('/providers/code_title_add',methods =["GET", "POST"])
    @pro_token_required
    def code_title_add():
        if request.method == "GET":
            return "Worng code_title_add Method"

        elif request.method == "POST":
            error = ''
            print('code_title_add request Method is',request.method)
            msg = ''
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            CourseCode_form = request.form['CourseCode']
            CourseTitle_form = request.form['CourseTitle']
            

            if len(CourseTitle_form)>0:
                cur.execute("INSERT INTO trainingcourses SET ProviderID =%s, CourseCode =%s, CourseTitle = '%s'" % (v_provider_id,CourseCode_form,CourseTitle_form))
                conn.commit()
				
                msg="Code and title added suceesfully."
            else:
                msg="You must provide the course title"
            
        return redirect(url_for('providers_profile', msg=msg))
		
		
    @app.route('/providers/semdel',methods =["GET", "POST"])
    @pro_token_required
    def semdel():
        if request.method == "GET":
            return "Worng semdel Method"

        elif request.method == "POST":
            error = ''
            msg = ''
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            SemesterID_form = request.form['SemesterID']
            
            cur.execute("DELETE from trainingsemesters WHERE SemesterID =%s" % (SemesterID_form))
            conn.commit()
            
            msg="Semester deleted."
            
        return redirect(url_for('providers_profile', msg=msg))
		

    @app.route('/providers/semedit',methods =["GET", "POST"])
    @pro_token_required
    def semedit():
        if request.method == "GET":
            return "Worng semedit Method"

        elif request.method == "POST":
            error = ''
            msg = ''           
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            SemesterName_form = request.form['SemesterName']
            SemesterID_form = request.form['SemesterID']

            if len(SemesterName_form)>0:
                cur.execute("UPDATE trainingsemesters SET SemesterName ='%s' WHERE  ProviderID =%s and SemesterID =%s" % (SemesterName_form,v_provider_id,SemesterID_form))
                conn.commit()
                msg="Semester Name updated."
            else:
                msg="Semester Name not updated."
			
            
        return redirect(url_for('providers_profile', msg=msg))
		

    @app.route('/providers/providersemadd',methods =["GET", "POST"])
    @pro_token_required
    def providersemadd():
        if request.method == "GET":
            return "Worng providersemadd Method"

        elif request.method == "POST":
            error = ''
            print('providersemadd request Method is',request.method)
            msg = ''
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            SemesterYear_form = request.form['SemesterYear']
            SemesterName_form = request.form['SemesterName']
			
            cur.execute("select max(Sequence) from trainingsemesters where ProviderID=%s and SemesterYear=%s" % (v_provider_id,SemesterYear_form))
            v_sequence=cur.fetchone()
            n_seq=0
            n_seq=v_sequence[0]
            if v_sequence[0] is None:
                n_seq=1
            else:
                n_seq=n_seq+1
            
            if len(SemesterName_form)>0:
                cur.execute("INSERT INTO trainingsemesters(ProviderID,SemesterName, SemesterYear,Sequence) VALUES(%s,%s,%s,%s)",(v_provider_id,SemesterName_form,SemesterYear_form,n_seq))
                conn.commit()
                msg="Semester details have been updated."
            else:
                print("Semester details have not been updated.")
                msg="Semester details have not updated."

        return redirect(url_for('providers_profile', msg=msg))
	
	
    @app.route('/providers/providers_edit',methods =["GET", "POST"])
    @pro_token_required
    def providers_edit():

        if request.method == "GET":
            return "Worng providers_edit Method"

        elif request.method == "POST":
            error = ''
            email_form = request.form['Email']
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
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

            
            if len(NewPassword_form) >0:
			    
                if NewPassword_form == ConfirmPassword_form:
                    msg="NewPassword_form and ConfirmPassword_form matches."
                    CurrentPassword_form = NewPassword_form
                else:
                    msg="Sorry!! New Password and Confirm Password did not match"
            else:
                 msg="Password did not change"
                            

            sqlCur="UPDATE  trainingproviders SET ProviderName='%s', Email='%s', Password='%s', Address='%s', City='%s', Zip='%s', BusinessName='%s', Website='%s', FirstName='%s', LastName='%s', Phone='%s', HaveLicense='%s', StateExempt='%s', IDValue='%s' WHERE ProviderID =%s" %(ProviderName_form, Email_form, CurrentPassword_form, Address_form, City_form, Zip_form, BusinessName_form, Website_form, FirstName_form, LastName_form, Phone_form, HaveLicense_form, StateExempt_form, IDValue_form, v_provider_id)
            
            cur.execute(sqlCur)
            conn.commit()


        return redirect(url_for('providers_profile', msg=msg))
        

	
	
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
      
        cur.execute("SELECT SemesterYear FROM trainingsemesters WHERE ProviderID=%s group by SemesterYear order by SemesterYear asc" % v_provider_id)
        data={}
        years=cur.fetchall()
        semCnt={}
        for yr in years:
            cur.execute("SELECT  ts.SemesterID, ts.SemesterName, ts.SemesterYear, count(tcs.CourseSessionID) courses, ts.Sequence FROM trainingsemesters ts left join trainingcoursesessions tcs on ts.SemesterID = tcs.SemesterID WHERE ts.ProviderID=%s  and ts.SemesterYear=%s GROUP BY SemesterName ORDER BY Sequence ASC" %(v_provider_id, yr[0]))
            semyeardata = cur.fetchall()
            data[yr[0]]=semyeardata
            semCnt[yr[0]]=cur.rowcount
       
        cur.execute("SELECT tc.CourseID, tc.CourseTitle, tc.CourseCode ,count(tcs.CourseSessionID ) offerings FROM trainingcourses tc left join trainingcoursesessions tcs on tc.CourseID = tcs.CourseID WHERE tc.ProviderID=%s group by tc.CourseID" % v_provider_id)
        cours = cur.fetchall()
                 
				
        cur.execute("SELECT * FROM trainingsemesters WHERE ProviderID=%s group by SemesterYear order by SemesterYear asc"% v_provider_id)
        select_semyears = cur.fetchall()
        select_semyears_count = cur.rowcount

        cur.execute("SELECT SemesterID,SemesterName,SemesterYear FROM trainingsemesters WHERE ProviderID=%s order by SemesterYear desc" % v_provider_id)
        selsem = cur.fetchall()

        cur.execute("SELECT CourseID,CourseCode,CourseTitle FROM trainingcourses WHERE ProviderID=%s" % v_provider_id)
        selcrs = cur.fetchall()

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
        sesDys={}
        dysCnt={}
        SemesterID=-1
        hasCouoffses=-1
        WeekDays = []
        for semyear1 in hasCouoffsem:
            SemesterID = semyear1[0]
            
            cur.execute("SELECT tcs.CourseSessionID,tcs.CourseID,tcs.SemesterID,concat('$',tcs.CourseCost),date(tcs.StartDate) ,date(tcs.EndDate),tcs.Approved,tcs.Section,tcs.Active, tc.CourseTitle, tc.CourseCode FROM trainingcoursesessions tcs left join trainingcourses tc on tcs.CourseID=tc.CourseID where tcs.SemesterID=%s" %SemesterID)
            hasCouoffses = cur.fetchall()
            sesData[SemesterID]=hasCouoffses
            
            for fetchcouses in hasCouoffses:
                CourseSessionID = fetchcouses[0]
                
                coursesessionid = CourseSessionID
                cur.execute("SELECT count(*) as noofapplicants from ita where CourseSessionID= %s" %coursesessionid)
                applicants = cur.fetchall()
                appData[coursesessionid]=applicants
				
                cur.execute("SELECT DayOfWeek FROM trainingcoursesessiondays where CourseSessionID=%s" %coursesessionid)
                 
                sesDys[coursesessionid]= cur.fetchall()
                dysCnt[coursesessionid] = cur.rowcount
                                
                WeekDays = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]


        cur.execute("select i.ApplicationID, i.ProfileID, tcs.CourseSessionID, date(tcs.StartDate), date(tcs.EndDate), tc.CourseTitle, p.first_name, p.last_name from ita i left join trainingcoursesessions tcs on i.CourseSessionID=tcs.CourseSessionID left join trainingcourses tc on tcs.CourseID=tc.CourseID left join profiles p on i.ProfileID = p.profile_id WHERE i.Approved=1 and tc.ProviderID=%s" % v_provider_id)

        approveditas = cur.fetchall()
        
			
        return render_template('providers/providers_profile.html', data=data, semCnt=semCnt, providername=providername, acinfo=acinfo, cours=cours, get_course=select_course, hasCourseandSemester=hasCourseandSemester, hasCouoffsem=hasCouoffsem, hasCouoffsemCount=hasCouoffsemCount, SemesterID=SemesterID, hasCouoffses=hasCouoffses, appData=appData, selsem=selsem, selcrs=selcrs, sesDys=sesDys, dysCnt=dysCnt, WeekDays=WeekDays, sesData=sesData, approveditas=approveditas)

		
    @app.route('/providers_login',methods =["GET", "POST"])
    def providers_login():
	        	
        if request.method == "GET":
           return render_template('providers/providers_login.html')
        elif request.method == "POST":
            error = ''
            
            email_form = request.form['Email']
            password_form = request.form['Password']
                        
	    #CHECKS IF USERNAME EXSIST
            
            cur.execute("SELECT ProviderID ,ProviderName , Email, Password FROM trainingproviders WHERE email='"+ email_form+"'")		
            row = cur.fetchone()

            if not row is None:
                v_provider_id=row[0]
                v_providername=row[1]
                v_email=row[2]
                v_password=row[3]
                                           
                if password_form == v_password:
                    token = jwt.encode({'email' : v_email, 'password' : v_password, 'v_provider_id' : v_provider_id, 'Providername': v_providername, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=1800)}, app.config['SECRET_KEY'], algorithm='HS256')
                    
                    tkn = json.dumps({'token' :  token.decode('UTF-8'),'email' : v_email, 'password' : v_password, 'v_provider_id' : v_provider_id, 'Providername': v_providername})
                    tkdcode = jwt.decode(token, app.config['SECRET_KEY'])
                                        					
					
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

    @app.route('/jobseeker')
    @token_required
    def jobseeker():
        return render_template('jobseeker/js_intro.html')		
      
    @app.route('/login', methods=["GET", "POST"])
    def logintemp():
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
                
                v_profile_id=row[0]
                v_first_name=row[1]
                v_last_name=row[2]
                v_email=row[3]
                v_password=row[4]
                v_registration_type=row[5]
                print('Your registration_type from DB :',v_registration_type)
                           
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
			
    '''
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
                profile_id = data['user_id']
                print(
                    "Came into job_save and session is valid and have tocket and parsing data and getting profile_id --> {}".format(profile_id))
                if job_id:
                    saved_job.saved_jobs(user_id=profile_id, job_id=job_id)
                    flash('You have saved job successfully')
                    job_description=form_data.job_description(job_id)
                    print("job_description ----> {}".format(job_description))
                    return render_template('job_description.html',job_description=job_description)
	'''				


    @app.route('/jobsearch/', methods=["GET", "POST"])
    @token_required
    def jobsearch():
        token=session.get('token')
        if token:
            print("token is vaild")
            print("token -----> {}".format(token))
            job_details="View Details"
            print("job_details -----> {}".format(job_details))
            data=jwt.decode(token,app.secret_key)
            profile_id = data['user_id']	    
        else:
            print("token is not vaild")
            print("token -----> {}".format(token))
            job_details="Login to View"
            print("job_details -----> {}".format(job_details))
        if request.method == "GET":
            print ("inside jobsearch get!!!")
            #sectors=form_data.sectors()
            page = 1
            perpage = 10
            keyword = ''
            args_page = request.args.get('page')
            keyword = request.args.get('keyword')	  
            sectors = request.args.get('sector')	
	    
            if args_page:
                page  = args_page
            offset = (int(page) - 1) * perpage
            sector_state = {'choice':sectors}
            if keyword and sectors:
                keyword = (keyword, sectors)
            elif keyword and not sectors:
                keyword = (keyword, None)
            elif not keyword and sectors:
                keyword = (None, sectors)
            elif not keyword and not sectors:
                keyword = (None, None)

            print("!@#$%^",keyword)
            #form_data.save_searches(q=keyword_searched,s=sector_searched,ProfileID=profile_id)
            jobs_limited = recent_job.recent_job(limit=10, offset=offset, keyword=keyword)
            jobs = recent_job.total_jobs(keyword=keyword)
            page = request.args.get(get_page_parameter(), type=int, default=1)
            pagination = Pagination(page=page, total=len(jobs), css_framework='foundation', record_name='jobs',per_page_parameter=perpage)

            return render_template('jobseeker/pagnation.html', jobs=jobs_limited, pagination=pagination, sectors=sectors, keyword=keyword,job_details=job_details,sector_state=sector_state)
            '''
            jobs_limited = recent_job.recent_job(limit=10, offset=offset, keyword=keyword)
            jobs = recent_job.total_jobs(keyword=keyword)
            page = request.args.get(get_page_parameter(), type=int, default=1)
            pagination = Pagination(page=page, total=len(jobs), css_framework='foundation', record_name='jobs',per_page_parameter=perpage)
            return render_template('pagnation.html', jobs=jobs_limited, pagination=pagination,  keyword=keyword, job_details=job_details, sector_state=sector_state)
            '''
        else:
            print ("inside jobsearch post")
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
            print ("keyword_searched")
            print (keyword_searched)
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
            flash('No records found')
            if keyword and sectors:
                keyword = (keyword, sectors)
            elif keyword and not sectors:
                keyword = (keyword, None)
            elif not keyword and sectors:
                keyword = (None, sectors)
            elif not keyword and not sectors:
                keyword = (None, None)

            print("!@#$%^",keyword)
            #form_data.save_searches(q=keyword_searched,s=sector_searched,ProfileID=profile_id)
            jobs_limited = recent_job.recent_job(limit=10, offset=offset, keyword=keyword)
            jobs = recent_job.total_jobs(keyword=keyword)
            page = request.args.get(get_page_parameter(), type=int, default=1)
            pagination = Pagination(page=page, total=len(jobs), css_framework='foundation', record_name='jobs',per_page_parameter=perpage)
            return render_template('jobseeker/pagnation.html', jobs=jobs_limited, pagination=pagination, sectors=sectors_data, keyword=keyword_searched,job_details=job_details,sector_state=sector_state)
					       
    @app.route('/jobsave/', methods=["GET"])
    @token_required
    def jobsave():
        if session:
            token=session.get('token')
            if token:
                data=jwt.decode(token,app.secret_key)
                profile_id = data['v_profile_id']
            print("getting into jobdescription")
            if profile_id:
                savedjobs=form_data.savedjobs(profile_id)
                return render_template('jobseeker/js_manage.html', savedjobs=savedjobs)
				
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
                profile_id = data['user_id']
                print(
                    "Came into job_save and session is valid and have tocket and parsing data and getting profile_id --> {}".format(profile_id))
                if job_id:
                    saved_job.saved_jobs(user_id=profile_id, job_id=job_id)
                    flash('You have saved job successfully')
                    job_description=form_data.job_description(job_id)
                    print("job_description ----> {}".format(job_description))
                    return render_template('jobseeker/job_description.html',job_description=job_description)
				
    @app.route('/jobremove/', methods=["GET"])
    @token_required
    def jobremove():
        jobid = request.args.get('jobid')    
        if session:
            token=session.get('token')
            if token:
                data=jwt.decode(token,application.secret_key)
                profile_id = data['user_id']
            print ("inside jobremove")
            if profile_id:
                removejob=form_data.remove_jobs(JobseekerID=profile_id,JobID=jobid)
                savedjobs=form_data.savedjobs(profile_id)
                flash('This job has been successfully removed job from Saved Jobs area!')		
                return render_template('jobseeker/js_manage.html', savedjobs=savedjobs)
				
    @app.route('/jobapply/', methods=["GET"])
    @token_required
    def jobapply():
        jobid = request.args.get('jobid')    
        if session:
            token=session.get('token')
            if token:
                data=jwt.decode(token,application.secret_key)
                profile_id = data['user_id']
            print ("inside jobapply")
            if request.method == "GET":	    
                return render_template('jobseeker/job_apply.html',job_description=job_description)

    @app.route('/jsprofile/', methods=["GET", "POST"])
    @token_required
    def jsprofile():        
        if request.method == "POST":
            print ("inside jsprofile post")
            return render_template('js_profile.html')

        elif request.method == "GET":
            print ("inside jsresume post")
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

    @app.route('/resumeshow/', methods=["GET", "POST"])
    def resumeshow():
        print ('inside resumeshow')
        #js_profile_id = '23916'
        js_profile_id =('v_profile_id')
        js_resumes = form_data.js_resumes(js_profile_id=js_profile_id)
        resume_path = js_resumes[len(js_resumes)-1][3]
        print(resume_path)
        return send_from_directory(application.config['UPLOAD_FOLDER'], resume_path.split(application.config['UPLOAD_FOLDER'])[1]) 
                
 
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

if __name__=="__main__":
    #main_obj=register()
    app.run(host='192.168.110.4', debug=True, port=80)
    #main_obj.render_static()

