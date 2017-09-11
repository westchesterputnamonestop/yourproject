from flask import Flask, render_template, request, session, redirect, url_for,jsonify
import re
import json

app = Flask(__name__,template_folder='../templates',static_folder='static')
class validate:
    @app.route("/form")
    def main():
        return render_template('employer/signup.html')

@app.route("/formvalidate", methods=['GET', 'POST'])
def loginvalidate():
    login_info = request.get_json()
    firstname = str(login_info['firstname'])
    lastname = str(login_info['lastname'])
    title = str(login_info['title'])
    companyname = str(login_info['companyname'])
    address = str(login_info['address'])
    city = str(login_info['city'])
    state  = str(login_info['state'])
    zip = str(login_info['zip'])
    phone = str(login_info['phone'])
    extension = str(login_info['extension'])
    altphone = str(login_info['altphone'])
    fax = str(login_info['fax'])
    website = str(login_info['website'])
    einnumber = str(login_info['einnumber'])
    companyinformation = str(login_info['companyinformation'])
    skillstrainingwanted = str(login_info['skillstrainingwanted'])
    sectors = login_info['sectors']
    terms = login_info['terms']
    email = str(login_info['email'])
    password = str(login_info['password'])
    phonenum = str(login_info['number'])
    securityquestion1 = str(login_info['securityquestion1'])
    securityanswer1 = str(login_info['securityanswer1']) 
    securityquestion2 = str(login_info['securityquestion2'])
    securityanswer2 = str(login_info['securityanswer2'])
    print(terms)
    info = []
    firstnamedata={
        'type':'name',
        'field':'first name',
        'errorname': 'firstname',
        'input':firstname
    }
    info.append(firstnamedata)
    lastnamedata={
        'type':'name',
        'field':'last name',
        'errorname': 'lastname',
        'input':lastname
    }
    info.append(lastnamedata)
    titledata={
        'type':'title',
        'field':'title',
        'errorname': 'title',
        'input':title
    }
    info.append(titledata)
    companynamedata={
        'type':'text',
        'field':'companyname',
        'errorname': 'companyname',
        'input':companyname
    }
    info.append(companynamedata)
    addressdata={
        'type':'address',
        'field':'address',
        'errorname': 'address',
        'input':address
    }
    info.append(addressdata)
    citydata={
        'type':'city',
        'field':'city',
        'errorname': 'city',
        'input':city
    }
    info.append(citydata)
    statedata={
        'type':'state',
        'field':'state',
        'errorname': 'state',
        'input':state
    }
    info.append(statedata)
    zipdata={
        'type':'zip',
        'field':'zip',
        'errorname': 'zip',
        'input':zip
    }
    info.append(zipdata)
    phonedata={
        'type':'phonenumber',
        'field':'phone',
        'errorname': 'phone',
        'input':phone
    }
    info.append(phonedata)
    extensiondata={
        'type':'extension',
        'field':'extension',
        'errorname': 'extension',
        'input':extension
    }
    info.append(extensiondata)
    altphonedata={
        'type':'phonenumber',
        'field':'altphone',
        'errorname': 'altphone',
        'input':altphone
    }
    info.append(altphonedata)
    
    faxdata={
        'type':'phonenumber',
        'field':'fax',
        'errorname': 'fax',
        'input':fax
    }
    info.append(faxdata)
    websitedata={
        'type':'website',
        'field':'website',
        'errorname': 'website',
        'input':website
    }
    info.append(websitedata)

    einnumberdata={
        'type':'code',
        'field':'einnumber',
        'errorname': 'einnumber',
        'input':einnumber
    }
    info.append(einnumberdata)    
    companyinformationdata={
        'type':'text',
        'field':'companyinformation',
        'errorname': 'companyinformation',
        'input':companyinformation
    }
    info.append(companyinformationdata)
    skillstrainingwanteddata={
        'type':'text',
        'field':'skillstrainingwanted',
        'errorname': 'skillstrainingwanted',
        'input':skillstrainingwanted
    }
    info.append(skillstrainingwanteddata)
    sectorsdata={
        'type':'sectors',
        'field':'sectors',
        'errorname': 'sectors',
        'input':sectors
    }
    info.append(sectorsdata)
    termsdata={
        'type':'terms',
        'field':'terms',
        'errorname': 'terms',
        'input':terms
    }
    info.append(termsdata)
    emaildata={
        'type':'email',
        'field':'user name',
        'errorname': 'email',
        'input':email
    }
    info.append(emaildata)
    passworddata={
        'type':'password',
        'field':'password',
        'errorname': 'password',
        'input':password
    }
    info.append(passworddata)
    phonenumdata={
        'type':'phonenumber',
        'field':'phone number',
        'errorname': 'phnumber',
        'input':phonenum
    }
    info.append(phonenumdata)
    securityquestion1data={
        'type':'securityquestion1',
        'field':'securityquestion1',
        'errorname': 'securityquestion1',
        'input':securityquestion1
    }
    info.append(securityquestion1data)
    securityanswer1data={
        'type':'text',
        'field':'securityanswer1',
        'errorname': 'securityanswer1',
        'input':securityanswer1
    }
    info.append(securityanswer1data)
    securityquestion2data={
        'type':'securityquestion2',
        'field':'securityquestion2',
        'errorname': 'securityquestion2',
        'input':securityquestion2
    }
    info.append(securityquestion2data)
    securityanswer2data={
        'type':'text',
        'field':'securityanswer2',
        'errorname': 'securityanswer2',
        'input':securityanswer2
    }
    info.append(securityanswer2data)

    errors = validate(info)
    if not errors:
        success={'success':"login success full"}
        return jsonify(success)
    return jsonify(errors)

def validate(info):
    citypattern = "^[a-zA-Z]|[ ][a-zA-Z]*$"
    titlepattern = "^[A-Za-z0-9-,.]|[ ][a-zA-Z]{4,40}$"
    addresspattern = "^[0-9]{0,5}[ ][A-Za-z]|[0-9]{5}[A-Za-z][ ][0-9-]||[0-9]{5}[-][A-Za-z][ ][0-9-]*$"
    zippattern = "^[0-9]{5}$"
    codepattern =  "^[0-9]{1,8}$"
    extensionpattern = "^[0-9]{3,6}$"
    namepattern =  "^[a-zA-Z].{4,25}|[ ][a-zA-Z].{4,25}$"
    textpattern = "^[A-Za-z0-9-,.]|[ ][a-zA-Z]*$"
    emailpattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    passwordpattern =  "^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{5,}$"
   #phnumberpattern = "^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$"
    phnumberpattern = "^[0-9]{3}-[0-9]{3}-[0-9]{4}|[0-9]{10}$"
    errors = {}
    for data in info:
        if data['type'] == "name":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"
            elif not re.match(namepattern, data['input']):
                errors[data['errorname']]="invalid pattern given for "+data['field']
        if data['type'] == "code":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"
            elif not re.match(codepattern, data['input']):
                errors[data['errorname']]="invalid pattern given for "+data['field']
        if data['type'] == "section":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"
            elif not re.match(codepattern, data['input']):
                errors[data['errorname']]="invalid pattern given for "+data['field']


        if data['type'] == "title":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"
            elif not re.match(titlepattern, data['input']):
                errors[data['errorname']]="invalid pattern given for "+data['field']

        elif data['type'] == "semester":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"
        elif data['type'] == "course":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"


        if data['type'] == "text": 
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"
            elif not re.match(textpattern, data['input']):
                errors[data['errorname']]="invalid pattern given for "+data['field']
        elif data['type'] == "address":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"
            elif not re.match(addresspattern, data['input']):
                errors[data['errorname']]="invalid pattern given for "+data['field']
        elif data['type'] == "city":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"
            elif not re.match(citypattern, data['input']):
                errors[data['errorname']]="invalid pattern given for "+data['field']
        elif data['type'] == "existingpassword":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"

        elif data['type'] == "state":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"
        elif data['type'] == "zip":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"
            elif not re.match(zippattern, data['input']):
                errors[data['errorname']]="invalid pattern given for "+data['field']
        elif data['type'] == "phonenumber":
            if not data['input']:
               errors[data['errorname']]=data['field']+" is a mandatory field"
            elif not re.match(phnumberpattern, data['input']):
                errors[data['errorname']]="invalid pattern given for "+data['field']
        elif data['type'] == "extension":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"
            elif not re.match(extensionpattern, data['input']):
                errors[data['errorname']]="invalid pattern given for "+data['field']
        elif data['type'] == "website":
            if not data['input']:
                 errors[data['errorname']]=data['field']+" is a mandatory field"
            elif not re.match(textpattern, data['input']):
                 errors[data['errorname']]="invalid pattern given for "+data['field']
        elif data['type'] == "einnumber":
            if not data['input']:
               errors[data['errorname']]=data['field']+" is a mandatory field"
            elif not re.match(zippattern, data['input']):
                errors[data['errorname']]="invalid pattern given for "+data['field']
        elif data['type'] == "sectors":
            if len(data['input'])==0:
                errors[data['errorname']]=data['field']+" is a mandatory field"
        elif data['type'] == "terms":
            if not data['input']:
                errors[data['errorname']]="Please agree for terms and conditions"
        elif data['type'] == "securityquestion1":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"
        elif data['type'] == "securityquestion2":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"
        elif  data['type'] == "email":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"
            elif not re.match(emailpattern, data['input']):
                errors[data['errorname']]="invalid pattern given for "+data['field']
        elif  data['type'] == "password":
            if not data['input']:
                errors[data['errorname']]=data['field']+" is a mandatory field"
            elif not re.match(passwordpattern, data['input']):
                errors[data['errorname']]="invalid pattern given for "+data['field']
        
    return errors
    
      
if __name__ == "__main__":
    app.run(host='192.168.110.4', debug=True, port=80)
