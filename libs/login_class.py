from flask import Flask, session, redirect, escape, url_for, request, render_template, make_response, send_from_directory, jsonify
import mysql.connector
import json
from db import Database
from flask_jwt import JWT, jwt_required, current_identity 
import jwt
import datetime
from functools import wraps



app = Flask(__name__,template_folder='../templates',static_folder='static')
app.config['SECRET_KEY'] = 'super-secret'
data = Database()
cur, conn = data.connection()


class login():
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            #print('insdie wraps')		
            token = session.get('token')
            if not token:
                print('Invalid Token')
                return render_template('login.html')
            try:
                tkn_data = jwt.decode(token, app.config['SECRET_KEY'])
                #print('insdie wraps Token: ', tkn_data)
                
            except:
                print('Oops Token expired')
                return render_template('login.html')
                
            return f(*args, **kwargs)
        return decorated
	
	
		
		
    @app.route('/')
    def index():
        return render_template('index.html')
		
    @app.route('/emp_profiles')
    @token_required
    def emp():
        return render_template('emp_profile.html')

    @app.route('/youth')
    @token_required
    def youth():
        return render_template('youth.html')

    @app.route('/jobseeker')
    @token_required
    def jobseeker():
        token = session['token']
        v_email = session['v_email']
        return render_template('jobseeker.html', token=token, v_email=v_email)
        
      
    @app.route('/login',methods =["GET", "POST"])
    def login():
	
        if request.method == "GET":
           return render_template('login.html')
        elif request.method == "POST":
            error = ''
            print('Request Method is',request.method)    
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
                    token = jwt.encode({'email' : v_email, 'password' : v_password, 'profile_id' : v_profile_id, 'first_name': v_first_name,'last_name': v_last_name, 'registration_type': v_registration_type, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=15)}, app.config['SECRET_KEY'], algorithm='HS256')
                    print('token created:',token)
                    tkn = json.dumps({'token' :  token.decode('UTF-8'),'profile_id' : v_profile_id,'email' : v_email,'password' : v_password})
                    tdecode = jwt.decode(token, app.config['SECRET_KEY'])
                    #print('token decode:',tdecode)
                    					
					
                    if v_registration_type == 'Job Seeker':
                        htm = 'jobseeker'
                    elif v_registration_type == 'Employer':
                        htm = 'emp'
                    elif v_registration_type == 'InternStudent':
                        htm = 'youth'
                    session['token']=token
                    session['v_email']=v_email
                    return redirect(url_for(htm))
                    
                return 'Invalid ID or password1'
            else:
                return 'Invalid ID or password2'
				
				
				
		#return 'Enter Password'
        else:
            print(email_form + '...USER DOESNOT EXISTS..!!!')
            return 'Invalid ID or password3'
                
                        
                    
          
    @app.route('/logout')
    def logout():
        session.pop('email', None)
        return redirect(url_for('index'))
            
        
 
#conn.close()           

if __name__ == "__main__":
    app.run(host='192.168.110.4', debug=True, port=80)
        
