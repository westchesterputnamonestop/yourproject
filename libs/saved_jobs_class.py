from flask import Flask, render_template, request, redirect, url_for, flash
from db import Database
from dynamic_form_class import Dynamicformdata
import mysql.connector
import datetime
import json

application = Flask(__name__)
data = Database()
cur, conn = data.connection()
form_data = Dynamicformdata()


class SavedJobs:
    """
    This class renders GET and POST for registration form.
    """
    def saved_jobs(self, user_id, job_id):
        """

        """
        if user_id and job_id:
            save_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            print("++++++++")
            print("inside 'INSERT INTO savedjobs (jobseekerID, jobID, SaveDate) values' on saved_jobs_class.py")
            print("++++++++")
            try:
                job_insert='''INSERT INTO savedjobs (jobseekerID, jobID, SaveDate) values ('{0}', '{1}', '{2}')'''.format(user_id, job_id, save_date)
                
                print("Insert statement job_insert ------> {}".format(job_insert))
                
                insert_cur=data.execute(conn,cur,job_insert)
               
                print("data.execute(conn, cur, job_insert) -----> {}".format(insert_cur))
               
                jobseekerid=insert_cur.lastrowid
               
                print("Insert into saved jobs table")
                print("profile id --------> {}".format(jobseekerid))
                
            except mysql.connector.Error as e:
                print("Error {}".format(e))
                return False
            return True

if __name__ == "__main__":
    savedjobs = SavedJobs()
    application.run(debug=True)
    jobseeker_obj.render_static()