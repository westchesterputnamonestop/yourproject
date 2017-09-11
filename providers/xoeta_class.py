 #project westchesterputnamonestop Training providers
 #author: Sailaja
 #Date: 08-31-2017
 #Description of providers: Providers introduction, registration and Profile.

from flask import Flask, session, redirect, escape, url_for, request, render_template, make_response, send_from_directory, jsonify
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import sys
from db import Database
from flask_jwt import JWT, jwt_required, current_identity 
import jwt
import datetime
from functools import wraps


app = Flask(__name__)
#app = Flask(__name__,template_folder='../templates',static_folder='static')
app.config['SECRET_KEY'] = 'super-secret'
data = Database()
cur, conn = data.connection()


class providers_login():

    def pro_token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            #print('insdie wraps')		
            token = session.get('token')
            if not token:
                print('Invalid Token')
                return render_template('providers_login.html')
            try:
                tkn_data = jwt.decode(token, app.config['SECRET_KEY'])
                
            except:
                print('Token expired')
                return render_template('providers_login.html')
            return f(*args, **kwargs)
        return decorated


    @app.route('/providers/providers_reg',methods =["GET", "POST"])
    def providers_reg():
        if request.method == "GET":
            return render_template('providers_reg.html')

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
            msg="Thanks for registering Providers."

            cur.execute("select ProviderID from trainingproviders where Email='"+ Email_form+"'")
            cur_provider_id = cur.fetchone()
            v_provider_id = cur_provider_id[0]
            print('provider_id',v_provider_id)
            
            session['email_form']=Email_form, 
            session['password_form']=Password_form, 
            session['providername']=ProviderName_form,
            session['v_provider_id']=v_provider_id,

            emails = []
			#cur.execute("SELECT xop.UserID, xop.FirstName, xop.LastName, xop.Email FROM xousers AS xop, xouseraccess AS xoa WHERE xop.UserID = xoa.UserID AND xoa.AccessID = '11' ORDER BY xop.UserID")
            cur.execute("SELECT xop.Email FROM xousers AS xop, xouseraccess AS xoa WHERE xop.UserID = xoa.UserID AND xoa.AccessID = '11' And xop.UserID=32")
            email_cur = cur.fetchone()
            print('email',email_cur[0])

            if email_cur[0] != '':
                emails = email_cur[0]
                print("emails",emails)
            else:
                msg = 'No emails'

            #ademail = ','.join(emails)
            
            #msg['Subject'] = 'A candidate has created new Eligible Training Provider account in Onestop site.'
            #trnUrl="http://ostest.westchestergov.com/user/eta/index.php?id=training_providers.php?tpid="+v_provider_id
            #provlink='<a href="'+trnUrl+'">'+trnUrl+'</a>'
            me = ''
            you = ''
            provlink= ''
            msg = MIMEMultipart('alternative')
            msg['WPOS ETA Admin<info@westchesterputnamonestop.com>'] = me
            msg[email_cur] = you
            html = """<table>
            <tr>
            <td>A new user got registered as Eligable Training Provider , to see and approve the new ETA
            click on below link</td>
            </tr>
            <tr>
            <td>"""+provlink+"""</td>
            </tr>
            <tr><td>&nbsp;</td></tr>
            <tr><td>&nbsp;</td></tr>
            <tr><td>&nbsp;</td></tr>
            </table>"""
            
            msg.attach(MIMEText(html, 'html'))			
            #s = smtplib.SMTP('localhost')
            #server.login('username', 'password')
            #server = smtplib.SMTP(SERVER)
            #server.sendmail(FROM, TO, message)
            #s.sendmail = mail(me,you,msg.as_string())
            #s.quit()

		
			
        return redirect(url_for('providers_profile', msg=msg,Email_form=Email_form,Password_form=Password_form,ProviderName_form=ProviderName_form,v_provider_id=v_provider_id))


    @app.route('/reg_providers_profile')
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
        
			
        return render_template('providers_profile.html', data=data, semCnt=semCnt, providername=providername, acinfo=acinfo, cours=cours, get_course=select_course, hasCourseandSemester=hasCourseandSemester, hasCouoffsem=hasCouoffsem, hasCouoffsemCount=hasCouoffsemCount, SemesterID=SemesterID, hasCouoffses=hasCouoffses, appData=appData, selsem=selsem, selcrs=selcrs, sesDys=sesDys, dysCnt=dysCnt, WeekDays=WeekDays, sesData=sesData, approveditas=approveditas)
		
		
    @app.route('/providers/ita_download',methods =["GET", "POST"])
    @pro_token_required
    def ita_download():
        if request.method == "GET":
            return "Worng ita_download method."

        elif request.method == "POST":
            error = ''
            print('ita_download request Method is',request.method)
            
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            print('provider_id ita_download in',v_provider_id)
            CourseID_form = request.form['Course']
            print('CourseID ita_download in',CourseID_form)
            
            cur.execute("select i.ApplicationID, i.ProfileID, tcs.CourseSessionID, tcs.StartDate, tcs.EndDate, tc.CourseTitle, p.first_name, p.last_name from ita i left join trainingcoursesessions tcs on i.CourseSessionID=tcs.CourseSessionID left join trainingcourses tc on tcs.CourseID=tc.CourseID left join profiles p on i.ProfileID = p.profile_id WHERE i.Approved=1 and tc.ProviderID=%s" %(v_provider_id))
            conn.commit()
            #print("download complete")
            msg="download complete."
			
        return redirect(url_for('providers_profile', msg=msg)) 
		

    @app.route('/cors_offer_del',methods =["GET", "POST"])
    @pro_token_required
    def cors_offer_del():
        if request.method == "GET":
            return "Worng cors_offer_del Method"

        elif request.method == "POST":
            error = ''
            print('cors_offer_del request Method is',request.method)
            
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            #print('provider_id cors_offer_del in',v_provider_id)
            CourseID_form = request.form['Course']
            print('CourseID cors_offer_del in',CourseID_form)
            
            cur.execute("Delete From trainingcoursesessions WHERE CourseSessionID =%s" % (CourseID_form))
            conn.commit()
            print("Deleted code and title")
            msg="Code and title deleted suceesfully."
			
        return redirect(url_for('providers_profile', msg=msg))

		
    @app.route('/cors_offer_edit',methods =["GET", "POST"])
    @pro_token_required
    def cors_offer_edit():
        if request.method == "GET":
            return "Worng cors_offer_edit Method"

        elif request.method == "POST":
            error = ''
            print('cors_offer_edit request Method is',request.method)
            
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            #print('provider_id cors_offer_edit in',v_provider_id)
            Course_form = request.form['Course']
            #print('Course_form::::',Course_form)
            cousesid_form = request.form['cousesid']
            #print('cousesid_form::::',cousesid_form)
            Section_form = request.form['Section']
            #print('Section_form::::',Section_form)
            StartDate_form = request.form['StartDate']
            #print('StartDate_form::::',StartDate_form)
            EndDate_form = request.form['EndDate']
            #print('EndDate_form::::',EndDate_form)
            CourseCost_form = request.form['CourseCost']
            #print('CourseCost_form::::',CourseCost_form)
            Active_form = request.form['Active']
            #print('Active_form',Active_form)
            DayOfWeek_form = request.form.getlist('DayOfWeek')
            
            
            #if len(Course_form)>0:
            cur.execute("update trainingcoursesessions  set CourseID=%s, CourseCost='%s', StartDate=TIMESTAMP('%s'), EndDate=TIMESTAMP('%s'), Section='%s', Active='%s' where CourseSessionID=%s" %(Course_form, CourseCost_form.replace('$','',1), StartDate_form, EndDate_form, Section_form, Active_form, cousesid_form))
            conn.commit()
            #if len(DayOfWeek_form)>0:
            cur.execute("delete from trainingcoursesessiondays  where CourseSessionID = %s" %(cousesid_form))
            cur.execute("insert into trainingcoursesessiondays SET CourseSessionID=%s, DayOfWeek=%s" %(cousesid_form, DayOfWeek_form))
            conn.commit()
            msg="Code and title updated suceesfully."
            
            
        return redirect(url_for('providers_profile', msg=msg))
		
		
    @app.route('/cors_offer_add',methods =["GET", "POST"])
    @pro_token_required
    def cors_offer_add():
        if request.method == "GET":
            return "Worng cors_offer_add Method"

        elif request.method == "POST":
            error = ''
            print('cors_offer_add request Method is',request.method)
            
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            print('provider_id cors_offer_add in',v_provider_id)
            msg = ''
            Semester_form = request.form['Semester']
            #print('Semester_form',Semester_form)
            Course_form = request.form['Course']
            #print('Course_form',Course_form)
            Section_form = request.form['Section']
            #print('Section_form',Section_form)
            StartDate_form = request.form['StartDate']
            #print('StartDate_form',StartDate_form)
            EndDate_form = request.form['EndDate']
            #print('EndDate_form',EndDate_form)
            CourseCost_form = request.form['CourseCost']
            #print('CourseCost_form',CourseCost_form)
            Active_form = request.form['Active']
            print('Active_form',Active_form)
            DayOfWeek_form = request.form.getlist('DayOfWeek')
            print('DayOfWeek_form',DayOfWeek_form)
            
            cur.execute(("INSERT INTO trainingcoursesessions  SET SemesterID=%s, CourseID=%s, CourseCost =%s ,StartDate=TIMESTAMP('%s'),EndDate =TIMESTAMP('%s'),Approved = 0,Section =%s,Active =%s") % (Semester_form,Course_form,CourseCost_form,StartDate_form,EndDate_form,Section_form,Active_form))
    
            cur.execute(("SELECT tcs.CourseSessionID FROM trainingcoursesessions tcs left join trainingcourses tc on tcs.CourseID=tc.CourseID WHERE tc.ProviderID=%s and tcs.CourseID=%s and tcs.SemesterID=%s")%(v_provider_id,Course_form,Semester_form))
            corsesid=cur.fetchone()
            print('corsesid',corsesid)
            #WeekDays = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
            cur.execute("DELETE FROM trainingcoursesessiondays WHERE CourseSessionID =%s"%(corsesid[0]))
            
            for dy in DayOfWeek_form:
                print('dy: ',dy)
                cur.execute("INSERT INTO trainingcoursesessiondays SET CourseSessionID =%s, DayOfWeek =%s"%(corsesid[0],dy))
                conn.commit()
                msg="Course Offerings details added suceesfully."
                        
        return redirect(url_for('providers_profile', msg=msg))

		
    @app.route('/moveupanddown',methods =["GET", "POST"])
    @pro_token_required
    def moveupanddown():
        if request.method == "GET":
            return "Worng moveupanddown Method"

        elif request.method == "POST":
            error = ''
            print('moveupanddown request Method is',request.method)
            
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            #print('provider_id moveupanddown in',v_provider_id)
            flag_form = request.form['flag']
            SemesterID_form = request.form['SemesterID']
            print('SemesterID_form moveupanddown in',SemesterID_form)
            #print('flag_form moveupanddown in',flag_form)
            cur.execute("SELECT SemesterYear, Sequence, SemesterID FROM trainingsemesters  WHERE  SemesterID =%s" %(SemesterID_form))
            curRow = cur.fetchone()
            print('curRow',curRow)
            
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


    @app.route('/code_title_del',methods =["GET", "POST"])
    @pro_token_required
    def code_title_del():
        if request.method == "GET":
            return "Worng code_title_del Method"

        elif request.method == "POST":
            error = ''
            print('code_title_del request Method is',request.method)
            
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            #print('provider_id code_title_del in',v_provider_id)
            CourseID_form = request.form['CourseID']
            print('CourseID code_title_del in',CourseID_form)
            
            cur.execute("Delete From trainingcourses WHERE CourseID =%s" % (CourseID_form))
            conn.commit()
            print("Deleted code and title")
            msg="Code and title deleted suceesfully."
                        
        return redirect(url_for('providers_profile', msg=msg))
		

    @app.route('/code_title_edit',methods =["GET", "POST"])
    @pro_token_required
    def code_title_edit():
        if request.method == "GET":
            return "Worng code_title_edit Method"

        elif request.method == "POST":
            error = ''
            print('code_title_edit request Method is',request.method)
            
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            #print('provider_id code_title_edit in',v_provider_id)
            CourseCode_form = request.form['CourseCode']
            CourseTitle_form = request.form['CourseTitle']
            CourseID_form = request.form['CourseID']
            
            if len(CourseTitle_form)>0:
                cur.execute("UPDATE trainingcourses SET ProviderID =%s, CourseCode =%s, CourseTitle = '%s' WHERE  CourseID =%s" %(v_provider_id,CourseCode_form,CourseTitle_form,CourseID_form))
                conn.commit()
                #print("Updated course title",cur)
                msg="Code and title updated suceesfully."
            else:
                msg="You must provide the course title"
            
        return redirect(url_for('providers_profile', msg=msg))


    @app.route('/code_title_add',methods =["GET", "POST"])
    @pro_token_required
    def code_title_add():
        if request.method == "GET":
            return "Worng code_title_add Method"

        elif request.method == "POST":
            error = ''
            print('code_title_add request Method is',request.method)
            
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            print('provider_id code_title_add in',v_provider_id)
            CourseCode_form = request.form['CourseCode']
            CourseTitle_form = request.form['CourseTitle']
            print('CourseTitle_form in',len(CourseTitle_form))

            if len(CourseTitle_form)>0:
                cur.execute("INSERT INTO trainingcourses SET ProviderID =%s, CourseCode =%s, CourseTitle = '%s'" % (v_provider_id,CourseCode_form,CourseTitle_form))
                conn.commit()
				
                #print("insert course title",cur)
                msg="Code and title added suceesfully."
            else:
                msg="You must provide the course title"
            
        return redirect(url_for('providers_profile', msg=msg))
		
		
    @app.route('/semdel',methods =["GET", "POST"])
    @pro_token_required
    def semdel():
        if request.method == "GET":
            return "Worng semdel Method"

        elif request.method == "POST":
            error = ''
            
            providername=session['v_providername']
            v_provider_id=session['v_provider_id']
            SemesterID_form = request.form['SemesterID']
            print('SemesterID_form',SemesterID_form)

            cur.execute("DELETE from trainingsemesters WHERE SemesterID =%s" % (SemesterID_form))
            conn.commit()
            
            #print('cur',semName)
            msg="Semester deleted."
            
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
            #print('provider_id semedit in',v_provider_id)
            SemesterName_form = request.form['SemesterName']
            print('SemesterName',SemesterName_form)
            SemesterID_form = request.form['SemesterID']
            print('SemesterID',SemesterID_form)

            if len(SemesterName_form)>0:
                cur.execute("UPDATE trainingsemesters SET SemesterName ='%s' WHERE  ProviderID =%s and SemesterID =%s" % (SemesterName_form,v_provider_id,SemesterID_form))
                conn.commit()
                msg="Semester Name updated."
            else:
                msg="Semester Name not updated."
			
            
        return redirect(url_for('providers_profile', msg=msg))
		 #return render_template('providers_profile.html')
		

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
            #print('cur',v_sequence)
            n_seq=0
            n_seq=v_sequence[0]
            #print('v_sequence[0]',v_sequence[0])
            if v_sequence[0] is None:
                n_seq=1
            else:
                n_seq=n_seq+1
            #print('n_seq',n_seq)
			
            if len(SemesterName_form)>0:
                cur.execute("INSERT INTO trainingsemesters(ProviderID,SemesterName, SemesterYear,Sequence) VALUES(%s,%s,%s,%s)",(v_provider_id,SemesterName_form,SemesterYear_form,n_seq))
                
                conn.commit()
                print("Semester details have been updated.")
                msg="Semester details have been updated."
            else:
                print("Semester details have not been updated.")
                msg="Semester details have not updated."

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

            #print('NewPassword_form length:',len(NewPassword_form)) 
			
            if len(NewPassword_form) >0:
			    
                if NewPassword_form == ConfirmPassword_form:
                    #print ('NewPassword_form and ConfirmPassword_form matches.')
                    msg="NewPassword_form and ConfirmPassword_form matches."
                    CurrentPassword_form = NewPassword_form
                else:
                    #print ('Sorry!! New Password and Confirm Password did not match.')
                    msg="Sorry!! New Password and Confirm Password did not match"
            else:
                 #print ('Password did not change')
                 msg="Password did not change"
                            

            sqlCur="UPDATE  trainingproviders SET ProviderName='%s', Email='%s', Password='%s', Address='%s', City='%s', Zip='%s', BusinessName='%s', Website='%s', FirstName='%s', LastName='%s', Phone='%s', HaveLicense='%s', StateExempt='%s', IDValue='%s' WHERE ProviderID =%s" %(ProviderName_form, Email_form, CurrentPassword_form, Address_form, City_form, Zip_form, BusinessName_form, Website_form, FirstName_form, LastName_form, Phone_form, HaveLicense_form, StateExempt_form, IDValue_form, v_provider_id)
            
            #print ('query ->', sqlCur)
            cur.execute(sqlCur)
            conn.commit()


        return redirect(url_for('providers_profile', msg=msg))
        

	
	
    @app.route('/providers')
    def providers():
        return render_template('providers_intro.html')

		
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
            print('SemesterID: ',SemesterID)
            
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
        #print("approveditas: ",approveditas)
			
        return render_template('providers_profile.html', data=data, semCnt=semCnt, providername=providername, acinfo=acinfo, cours=cours, get_course=select_course, hasCourseandSemester=hasCourseandSemester, hasCouoffsem=hasCouoffsem, hasCouoffsemCount=hasCouoffsemCount, SemesterID=SemesterID, hasCouoffses=hasCouoffses, appData=appData, selsem=selsem, selcrs=selcrs, sesDys=sesDys, dysCnt=dysCnt, WeekDays=WeekDays, sesData=sesData, approveditas=approveditas)

		
    @app.route('/providers_login',methods =["GET", "POST"])
    def providers_login():
	        	
        if request.method == "GET":
           return render_template('providers_login.html')
        elif request.method == "POST":
            error = ''
            #print('Request Method is',request.method)    
            email_form = request.form['Email']
            password_form = request.form['Password']
                        
	    #CHECKS IF USERNAME EXSIST
            
            cur.execute("SELECT ProviderID ,ProviderName , Email, Password FROM trainingproviders WHERE email='"+ email_form+"'")		
            row = cur.fetchone()

            if not row is None:
                v_provider_id=row[0]
                #print('ProviderID from DB :',v_provider_id)
                v_providername=row[1]
                #print('ProviderName from DB :',v_providername)
                v_email=row[2]
                v_password=row[3]
                                           
                if password_form == v_password:
                    token = jwt.encode({'email' : v_email, 'password' : v_password, 'v_provider_id' : v_provider_id, 'Providername': v_providername, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=1800)}, app.config['SECRET_KEY'], algorithm='HS256')
                    #print('token created:',token)
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
                
                        
                    
          
    #@app.route('/pro_logout')
    #def pro_logout():
     #   session.pop('v_providername', None)
      #  return redirect(url_for('providers'))


    @app.route('/pro_logout')
    def pro_logout():
        session.pop('token', None)
        msg = 'You were logged out' 
        resp = app.make_response(render_template('providers_login.html', msg=msg))
        resp.set_cookie('token', expires=0)
        return render_template('providers_login.html') 
            
        
 
#conn.close()           

if __name__ == "__main__":
    app.run(host='192.168.110.4', debug=True, port=80)
        
