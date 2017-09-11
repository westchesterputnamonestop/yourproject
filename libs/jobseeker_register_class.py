from flask import Flask, render_template, request, redirect, url_for
from db import Database
from dynamic_form_class import Dynamicformdata
import mysql.connector
import json

application = Flask(__name__)
data = Database()
cur, conn = data.connection()
form_data = Dynamicformdata()


class JobseekerRegister:
    """
    This class renders GET and POST for registration form.
    """

    def user_exist_check_admin(self, email, profile_id):
        """
            User exist check admin 
            returns
             (bool): true/false
        """
        if email and profile_id:
            condition = "WHERE email == {} and profile_id == {};".format(email, profile_id)
        elif email:
            condition = "WHERE email == {};".format(email)
        else:
            condition = ";"
        row = data.execute(conn, cur, "SELECT * FROM profiles {}".format(condition))
        if row <= 0:
            return True
        else:
            return False

    def insert_into_db(self, dict_fields):
        """
        
        :param dict_fields: 
        :return: 
        """
        print("++++++++")
        print("inside 'def insert_into_db(self, dict_fields)' on jobseeker_register_class.py")
        print("++++++++")
        dict_fields['Securityquestion1'] = self.security_question1(dict_fields['Securityquestion1'])
        dict_fields['Securityquestion2']=self.security_question1(dict_fields['Securityquestion2'])

        try:
            profiles_insert='''INSERT INTO profiles(first_name,last_name,email,password,security_question1,security_answer1,security_question2,security_answer2) VALUES(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\')'''.format(
                dict_fields['FirstName'],dict_fields['LastName'],dict_fields['Email'],
                dict_fields['Password'],dict_fields['Securityquestion1'],
                dict_fields['Securityanswer1'],dict_fields['Securityquestion2'],
                dict_fields['Securityanswer2'])
            print("&&&&&&&&&&")
            print("Insert statement profiles_insert ------> {}".format(profiles_insert))
            print("&&&&&&&&&&")
            insert_cur = data.execute(conn, cur, profiles_insert)
            print("##################")
            print("data.execute(conn, cur, profiles_insert) -----> {}".format(insert_cur))
            print("##################")
            profile_id=insert_cur.lastrowid
            print("*********************")
            print("Insert into Problies table")
            print("profile id --------> {}".format(profile_id))
            print("*********************")
        except mysql.connector.Error as e:
            print("Error {}".format(e))
            return False
        salary_expected = self.salary_expected(dict_fields['Salaryexpected'])
        try:
            jobseekers_insert='''INSERT INTO jobseekers(jobseeker_profile_id,address_line1,city,state,zip,phone,times_viewed,JobCenterID,Unemployed,Readytowork,RTWStatus,isnewregistration,entity,agency,dob,gender,country_other) VALUES(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'1\',\'1\',\'1\',\'1\',\'1\',\'1\',\'1\',\'1\',\'{6}\','M','aaa')'''.format(
                profile_id,dict_fields['Address1'],dict_fields['City'],dict_fields['State'],dict_fields['Zip'],
                dict_fields['Phone'],dict_fields['dob'])
            print("&&&&&&&&&&")
            print("Insert statement jobseeker_insert ------> {}".format(jobseekers_insert))
            print("&&&&&&&&&&")
            jobseeker_cur = data.execute(conn, cur, jobseekers_insert)
            print("##################")
            print("data.execute(conn, cur, jobseekers_insert) -----> {}".format(jobseeker_cur))
            print("##################")
            jobseeker_profile_id=jobseeker_cur.lastrowid
            print("*********************")
            print("Insert into Jobseeker table")
            print("jobseeker profile id --------> {}".format(jobseeker_profile_id))
            print("*********************")
            jobseekers_select = ''' SELECT jobseeker_profile_id from jobseekers where jobseeker_profile_id=\'{}\''''.format(profile_id)
            select_query_cur = data.execute(conn, cur, jobseekers_select)
            for jobseeker_profile_id in select_query_cur:
                if (jobseeker_profile_id.count('(u\''))>0:
                    jobseeker_profile_id=str(jobseeker_profile_id).replace('(u\'','').replace('\',)','')
                else:
                    jobseeker_profile_id=str(jobseeker_profile_id).replace('(\'','').replace('\',)','')
                print("##########")
                print("select_query_cur = data.execute(conn, cur, jobseekers_select)")
                print(" Select query with in for loop x*---> {}".format(jobseeker_profile_id))
        except mysql.connector.Error as e:
            print("Error {}".format(e))
            return False
        return True

    def update_db(self):
        """
        
        :return: 
        """
        pass

    def security_question1(self, question_id):
        """
                
        :return: 
        """
        try:
            security_question_query = '''SELECT Question FROM securityquestions WHERE QuestionID = \'{}\' LIMIT 1'''.format(question_id)
            security_cur=data.execute(conn, cur, security_question_query)
            print("##########")
            print("def security_question1(self, question_id)")
            print(" security question with data*---> {}".format(cur))
            for question in security_cur:
                if (question.count('(u\''))>0:
                    question=str(question).replace('(u\'','').replace('\',)','')
                else:
                    question=str(question).replace('(\'','').replace('\',)','')
                print("##########")
                print("def security_question1(self, question_id)")
                print(" security question with in for loop x*---> {}".format(question))
                return question
        except Exception as e:
            print(e)

    def preferred_time(self,time_id):
        """

        :return: 
        """
        try:
            security_question_query='''SELECT Preferred FROM preferredtimes WHERE PreferredID = \'{}\' LIMIT 1'''.format(
                time_id)
            preferred_cur = data.execute(conn, cur, security_question_query)
            print("##########")
            print("    def preferred_time(self,time_id)")
            print(" preferred_time with data---> {}".format(cur))
            for preferred in preferred_cur:
                if (preferred.count('(u\''))>0:
                    preferred=str(preferred).replace('(u\'','').replace('\',)','')
                else:
                    preferred=str(preferred).replace('(\'','').replace('\',)','')
                print("##########")
                print("    def preferred_time(self,time_id)")
                print(" preferred_time with in for loop ---> {}".format(preferred))
                return preferred
        except Exception as e:
            print(e)

    def salary_expected(self,salary_id):
        """

        :return: 
        """
        try:
            security_question_query='''SELECT SalaryMax,SalaryMin FROM salaryranges WHERE SalaryRangeID = \'{}\' LIMIT 1'''.format(
                salary_id)
            salary_expected_cur = data.execute(conn, cur, security_question_query)
            print("##########")
            print("def salary_expected(self,salary_id):")
            print(" salary_expected with data---> {}".format(cur))
            for salarymax, salarymin in salary_expected_cur:
                print("##########")
                print("def salary_expected(self,salary_id):")
                print(" salary_expected with in loop x*---> {}".format(str(salarymax + '-' + salarymin)))
                return str(salarymin + '-' + salarymax)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    jobseeker_obj = JobseekerRegister()
    application.run(debug=True)
    jobseeker_obj.render_static()