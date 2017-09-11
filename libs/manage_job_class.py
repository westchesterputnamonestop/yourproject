from flask import Flask, render_template, request, redirect, url_for
from db import Database
import mysql.connector
import json

application = Flask(__name__)

class manage_job:

   def get_save_job(user,)
       cur.execute("SELECT jobID,SaveDate FROM savedjobs WHERE jobseekerID = '$user' AND jobID = '$job_id' ORDER BY SaveDate DESC LIMIT 4;")
       getsavejob=[]       		
        if(!$view_save) { mysql_error(); return FALSE;}   
        return $view_save;
    }
