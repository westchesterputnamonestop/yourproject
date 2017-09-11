from flask import Flask, render_template, request, redirect, url_for
from db import Database
import mysql.connector
import json
from flask_jwt import JWT, jwt_required, current_identity 
import jwt
import datetime
from functools import wraps

app = Flask(__name__,template_folder='../templates',static_folder='static')
app.config['SECRET_KEY'] = 'super-secret'
data = Database()
cur, conn = data.connection()


class xologin():
    def xologin_token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            #print('insdie wraps')		
            token = session.get('token')
            if not token:
                print('Invalid Token')
                return render_template('user_index.html')
            try:
                tkn_data = jwt.decode(token, app.config['SECRET_KEY'])
                
            except:
                print('Oops Token expired')
                return render_template('user_index.html')
            return f(*args, **kwargs)
        return decorated
		
    def xologinrequest ($auth)
	    #Try Login 	
		$this->_email=$auth['email'];
		$this->_password = $auth['password'];
		$this->_authenticate_type = $auth['authenticate'];
		$this->_resirect_page = $auth ['redirect'];


		#conn.close()           

if __name__ == "__main__":
    app.run(host='192.168.110.4', debug=True, port=80)