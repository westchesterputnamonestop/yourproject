from flask import Flask,render_template,request,redirect,url_for
from db import Database
import re
import hashlib

application = Flask(__name__)
data = Database()
cursor, connection = data.connection()


class DataValidator:
    """
    """

    def stripslashes(self, s):
        r = re.sub(r"\\(n|r)","\n",s)
        r = re.sub(r"\\","",r)
        return r

    def check_input(self,value):
        """
        :param value: 
        :return: 
        """
        if not value.isdigit():
            value = connection.converter.escape(value)
            print("++++++++")
            print("inside 'check_input' on data_validator.py for this vlaue --------> {}".format(value))
            print("++++++++")
        return value

    def data_encrypt(self, value):
        """        
        :return: 
        """
        value = self.check_input(value)
        encrypt_value = hashlib.sha256(str(value).encode('utf-8')).hexdigest()
        return encrypt_value
