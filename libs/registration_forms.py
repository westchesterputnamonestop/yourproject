from flask import Flask, render_template, request, redirect, url_for
from data_validator import DataValidator
from jobseeker_register_class import JobseekerRegister
from db import Database
from dynamic_form_class import Dynamicformdata
import json


formvalues=dict()
data_validator = DataValidator()
job_seeker_obj=JobseekerRegister()
data_obj=Database()
dynamic_obj=Dynamicformdata()

class RegistrationForms:
    """
    """

    def register_user(self, request):
        """
        
        :return: 
        """

        form_data = self.collect_registration_submission(request)
        save = self.save_to_database(form_data)
        if not save[0]:
            return (False, save[1])
        else:
            return (True, save[1])

    def collect_registration_submission(self, request):
        """

        :return: 
        """
        try:
            formvalues=dict()
            if request:
                dict_fields={}
                for elements in request.items():
                    dict_fields[elements[0]]=elements[1].data
                for key, value in dict_fields.items():
                    formvalues[key] = data_validator.check_input(value)
                if 'email' in formvalues and formvalues['email'] and 'profile_id' in formvalues and formvalues['profile_id']:
                    print("job_seeker_obj.user_exist_check_admin(email=formvalues['email'], profile_id=formvalues['profile_id'])")
                    exist = job_seeker_obj.user_exist_check_admin(email=formvalues['email'], profile_id=formvalues['profile_id'])
                if 'email' in formvalues and formvalues['email']:
                    print(''' job_seeker_obj.user_exist_check_admin(email=formvalues['email']) ''')
                    exist = job_seeker_obj.user_exist_check_admin(email=formvalues['email'], profile_id=None)
                return formvalues
        except Exception as e:
            print(e)

    def save_to_database(self, formvalues):
        if 'profile_id' in formvalues:
            return (job_seeker_obj.update_db(), formvalues)
        else:
            return (job_seeker_obj.insert_into_db(formvalues), formvalues)
