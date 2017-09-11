#contains all the dynamic form data , used commonly
from flask import Flask, render_template, request
from db import Database
import json
import datetime
application = Flask(__name__)
data = Database()
cur, conn = data.connection()


class Dynamicformdata:
    def render_static(self):
        if request.method =="POST":
            render_static=request.get_data()
            raw_str = render_static.decode('utf8').replace("'",'"')
            my_list = raw_str.split('&')
            my_json_dump = json.dumps(my_list)
        return my_json_dump + " it is there "

    def recent_job(self):
        cur.execute("select j.job_id,j.job_title,j.job_city,j.job_state,jl.job_level_name,j.publish_date from jobs j, job_levels jl where j.job_level_id=jl.job_level_id limit 10;")
        recentjob = []


        for job_id,job_title,job_city,job_state,job_level_name,publish_date in cur:
            if (job_title.count('(u\'')) > 0:
                job_id=str(job_id).replace('(u\'','').replace('\',)','')
                job_title = str(job_title).replace('(u\'','').replace('\',)','')
                job_city=str(job_city).replace('(u\'','').replace('\',)','')
                job_state = str(job_state).replace('(u\'','').replace('\',)','')
                job_level_name=str(job_level_name).replace('(u\'','').replace('\',)','')
                publish_date = datetime.datetime.strptime(str(publish_date).replace('(u\'','').replace('\',)',''),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %I:%M %p')
            else:
                job_id=str(job_id).replace('(\'','').replace('\',)','')
                job_title = str(job_title).replace('(\'','').replace('\',)','')
                job_city=str(job_city).replace('(\'','').replace('\',)','')
                job_state = str(job_state).replace('(\'','').replace('\',)','')
                job_level_name=str(job_level_name).replace('(\'','').replace('\',)','')
                publish_date = datetime.datetime.strptime(str(publish_date).replace('(\'','').replace('\',)',''),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %I:%M %p')
            recentjob.append((job_id,job_title,str(job_city+', '+job_state),job_level_name,publish_date))
        return recentjob

    def states(self):
        cur.execute("SELECT StateID, StateName from xostates")
        xostates = []
        for stateid,states in cur:
            if (states.count('(u\'')) > 0:
                stateid=str(stateid).replace('(u\'','').replace('\',)','')
                states = str(states).replace('(u\'','').replace('\',)','')
            else:
                stateid=str(stateid).replace('(\'','').replace('\',)','')
                states = str(states).replace('(\'','').replace('\',)','')
            xostates.append((stateid, states))
        return xostates

    def counties(self):
        cur.execute("SELECT county_id, county_name from counties")
        counties = []
        for county_id, county in cur:
            if (county.count('(u\'')) > 0:
                county_id=str(county_id).replace('(u\'','').replace('\',)','')
                county=str(county).replace('(u\'','').replace('\',)','')
            else:
                county_id=str(county_id).replace('(\'','').replace('\',)','')
                county = str(county).replace('(\'','').replace('\',)','')
            counties.append((county_id, county))
        return counties

    def sectors(self):
        cur.execute("SELECT sector_name from sectors")
        sectors = []
        for sector in cur:
            if (sector.count('(u\'')) > 0:
                sector = str(sector).replace('(u\'','').replace('\',)','')
            else:
                sector = str(sector).replace('(\'','').replace('\',)','')
            sectors.append(sector)
        return sectors

    def securityquestions(self):
        cur.execute("SELECT QuestionID, Question from securityquestions")
        securityquestions = []
        for securityquestionid, securityquestion in cur:
            if (securityquestion.count('(u\'')) > 0:
                securityquestionid=str(securityquestionid).replace('(u\'','').replace('\',)','')
                securityquestion=str(securityquestion).replace('(u\'','').replace('\',)','')
            else:
                securityquestionid=str(securityquestionid).replace('(\'','').replace('\',)','')
                securityquestion = str(securityquestion).replace('(\'','').replace('\',)','')
            securityquestions.append((securityquestionid, securityquestion))
        return securityquestions

    def jobcenters(self):
        cur.execute("SELECT JobCenterID, JobCenterName from jobcenters")
        jobcenters = []
        for jobcenterid, jobcenter in cur:
            if (jobcenter.count('(u\'')) > 0:
                jobcenterid=str(jobcenterid).replace('(u\'','').replace('\',)','')
                jobcenter=str(jobcenter).replace('(u\'','').replace('\',)','')
            else:
                jobcenterid=str(jobcenterid).replace('(\'','').replace('\',)','')
                jobcenter = str(jobcenter).replace('(\'','').replace('\',)','')
            jobcenters.append((jobcenterid, jobcenter))
        return jobcenters

    def preferredtimes(self):
        cur.execute("SELECT PreferredID,Preferred from preferredtimes")
        preferredtimes = []
        for preferredid, preferredtime in cur:
            if (preferredtime.count('(u\'')) > 0:
                preferredid=str(preferredid).replace('(u\'','').replace('\',)','')
                preferredtime = str(preferredtime).replace('(u\'','').replace('\',)','')
            else:
                preferredid=str(preferredid).replace('(\'','').replace('\',)','')
                preferredtime = str(preferredtime).replace('(\'','').replace('\',)','')
            preferredtimes.append((preferredid, preferredtime))
        return  preferredtimes

    def salaryranges(self):
        cur.execute("SELECT SalaryMin,SalaryMax from salaryranges")
        salaryranges = []
        for salary in cur:
            if (salary.count('(u\'')) > 0:
                salary = str(salary).replace('(u\'','').replace('\',)','')
            else:
                salary = str(salary).replace('(\'','').replace('\',)','')
            salaryranges.append(salary)
        return salaryranges
    def entity(self):
        cur.execute("SELECT Entity from entity")
        entity = []
        for Entity in cur:
            if (Entity.count('(u\'')) > 0:
                Entity = str(Entity).replace('(u\'','').replace('\',)','')
            else:
                Entity = str(Entity).replace('(\'','').replace('\',)','')
            entity.append(Entity)
        return entity

    def savedjobs(self, profile_id=None):
        cur.execute("SELECT sj.JobseekerID,sj.JobID,sj.SaveDate,j.job_title,j.job_city, j.job_state, j.publish_date  from savedjobs sj, jobs j where sj.JobID=j.job_id and JobseekerID='{}' ORDER BY SaveDate desc".format(profile_id))
        savedjobs = []
        for JobseekerID, JobID, SaveDate, job_title, job_city, job_state, publish_date in cur:
            if (str(JobID).count('(u\'')) > 0:
                JobseekerID = str(JobseekerID).replace('(u\'','').replace('\',)','')
                JobID=str(JobID).replace('(u\'','').replace('\',)','')
                SaveDate=str(SaveDate).replace('(u\'','').replace('\',)','')
                job_title=str(job_title).replace('(u\'','').replace('\',)','')
                job_city=str(job_city).replace('(u\'','').replace('\',)','')
                job_state=str(job_state).replace('(u\'','').replace('\',)','')
                publish_date=str(publish_date).replace('(u\'','').replace('\',)','')
            else:
                JobseekerID = str(JobseekerID).replace('(\'','').replace('\',)','')
                JobID=str(JobID).replace('(\'','').replace('\',)','')
                SaveDate=str(SaveDate).replace('(\'','').replace('\',)','')
                job_title=str(job_title).replace('(\'','').replace('\',)','')
                job_city=str(job_city).replace('(\'','').replace('\',)','')
                job_state=str(job_state).replace('(\'','').replace('\',)','')
                publish_date=str(publish_date).replace('(\'','').replace('\',)','')
            savedjobs.append((JobseekerID, JobID, SaveDate,  job_title, job_city+', '+job_state, publish_date))
        return savedjobs

    def customer_partneragencies(self):
        cur.execute("SELECT name from customer_partneragencies")
        customer_partneragencies = []
        for agencies in cur:
            if (agencies.count('(u\'')) > 0:
                agencies = str(agencies).replace('(u\'','').replace('\',)','')
            else:
                agencies = str(agencies).replace('(\'','').replace('\',)','')
            customer_partneragencies.append(agencies)
        return customer_partneragencies

    def get_last_profile_id(self):
        cur.execute("select profile_id from profiles order by profile_id desc limit 1")
        for profileid in cur:
            if (profileid.count('(u\'')) > 0:
                id = str(profileid).replace('(u\'','').replace('\',)','')
            else:
                id = str(profileid).replace('(','').replace(',)','')
        return id

    def job_description(self, job_id=None):
        if job_id:
            cur.execute("select j.job_title,j.status,j.work_days,j.jobdesc_attachment, joblv.job_level_name, j.job_address1, j.job_address2, j.job_city, j.job_state, j.job_zip, j.county_id, j.total_interviews_to_conduct, j.total_openings, j.min_salary, j.max_salary, j.hours_per_week, j.minimum_education, j.degree_required, j.starting_salary, j.dl_required, j.job_url,j.additional_information,j.job_description, sec.sector_name, j.job_id from jobs j, jobs_sectors jsec, sectors sec, job_levels joblv where j.job_id = jsec.job_id and jsec.sector_id=sec.sector_id and j.job_level_id=joblv.job_level_id and j.job_id='{}' limit 1;".format(job_id))
            job_description_list = []
            for job_title, status, work_days, jobdesc_attachment, job_level_name, job_address1, job_address2, job_city, job_state, job_zip, county_id, total_interviews_to_conduct, total_openings, min_salary, max_salary, hours_per_week, minimum_education, degree_required, starting_salary, dl_required, job_url  ,additional_information, job_description, sector_name, job_id in cur:
                if (job_title.count('(u\'')) > 0:
                    job_title = str(job_title).replace('(u\'','').replace('\',)','')
                    status = str(status).replace('(u\'','').replace('\',)','')
                    job_description=str(job_description).replace('(u\'','').replace('\',)','')
                    sector_name=str(sector_name).replace('(u\'','').replace('\',)','')
                    job_level_name=str(job_level_name).replace('(u\'','').replace('\',)','')
                    work_days= str(work_days).replace('(u\'','').replace('\',)','')
                    job_address1=str(job_address1).replace('(u\'','').replace('\',)','')
                    job_address2=str(job_address2).replace('(u\'','').replace('\',)','')
                    job_city=str(job_city).replace('(u\'','').replace('\',)','')
                    job_state=str(job_state).replace('(u\'','').replace('\',)','')
                    job_zip=str(job_zip).replace('(u\'','').replace('\',)','')
                    county_id= str(county_id).replace('(u\'','').replace('\',)','')
                    total_interviews_to_conduct= str(total_interviews_to_conduct).replace('(u\'','').replace('\',)','')
                    total_openings= str(total_openings).replace('(u\'','').replace('\',)','')
                    min_salary= str(min_salary).replace('(u\'','').replace('\',)','')
                    max_salary= str(max_salary).replace('(u\'','').replace('\',)','')
                    hours_per_week= str(hours_per_week).replace('(u\'','').replace('\',)','')
                    minimum_education= str(minimum_education).replace('(u\'','').replace('\',)','')
                    degree_required= str(degree_required).replace('(u\'','').replace('\',)','')
                    starting_salary= str(starting_salary).replace('(u\'','').replace('\',)','')
                    dl_required= str(dl_required).replace('(u\'','').replace('\',)','')
                    job_url= str(job_url).replace('(u\'','').replace('\',)','')
                    additional_information= str(additional_information).replace('(u\'','').replace('\',)','')
                    jobdesc_attachment= str(jobdesc_attachment).replace('(u\'','').replace('\',)','')
                    job_id=str(job_id).replace('(u\'','').replace('\',)','')

                else:
                    job_title = str(job_title).replace('(\'','').replace('\',)','')
                    status = str(status).replace('(\'','').replace('\',)','')
                    job_description=str(job_description).replace('(\'','').replace('\',)','')
                    sector_name=str(sector_name).replace('(\'','').replace('\',)','')
                    job_level_name=str(job_level_name).replace('(\'','').replace('\',)','')
                    work_days= str(work_days).replace('(\'','').replace('\',)','')
                    job_address1=str(job_address1).replace('(\'','').replace('\',)','')
                    job_address2=str(job_address2).replace('(\'','').replace('\',)','')
                    job_city=str(job_city).replace('(\'','').replace('\',)','')
                    job_state=str(job_state).replace('(\'','').replace('\',)','')
                    job_zip=str(job_zip).replace('(\'','').replace('\',)','')
                    county_id= str(county_id).replace('(\'','').replace('\',)','')
                    total_interviews_to_conduct= str(total_interviews_to_conduct).replace('(\'','').replace('\',)','')
                    total_openings= str(total_openings).replace('(\'','').replace('\',)','')
                    min_salary= str(min_salary).replace('(\'','').replace('\',)','')
                    max_salary= str(max_salary).replace('(\'','').replace('\',)','')
                    hours_per_week= str(hours_per_week).replace('(\'','').replace('\',)','')
                    minimum_education= str(minimum_education).replace('(\'','').replace('\',)','')
                    degree_required= str(degree_required).replace('(\'','').replace('\',)','')
                    starting_salary= str(starting_salary).replace('(\'','').replace('\',)','')
                    dl_required= str(dl_required).replace('(\'','').replace('\',)','')
                    job_url= str(job_url).replace('(\'','').replace('\',)','')
                    additional_information= str(additional_information).replace('(\'','').replace('\',)','')
                    jobdesc_attachment= str(jobdesc_attachment).replace('(\'','').replace('\',)','')
                    job_id=str(job_id).replace('(\'','').replace('\',)','')
                job_description_list.append((job_title, status, job_description, sector_name, job_level_name, work_days, job_address1 + job_address2 + job_city+','+ job_state + county_id + ' ' +job_zip, total_interviews_to_conduct, total_openings, (min_salary+ "-" +max_salary), hours_per_week, minimum_education, degree_required,starting_salary, dl_required,job_url, additional_information, jobdesc_attachment, job_id))
            return job_description_list

    def saved_searches(self,limit,js_profile_id):
        cur.execute(
            "SELECT SearchID, q, s, SaveDate from savedsearches where ProfileID = %s LIMIT %s"%(
            js_profile_id,limit))
        recent_saved_searches=[]
        for SearchID,q,s,SaveDate in cur:
            if '(u\'' in str(SearchID):
                q=str(q).replace('(u\'','').replace('\',)','')
                s=str(s).replace('(u\'','').replace('\',)','')
                SaveDate=str(SaveDate).replace('(u\'','').replace('\',)','')
            else:
                q=str(q).replace('(\'','').replace('\',)','')
                s=str(s).replace('(\'','').replace('\',)','')
                SaveDate=str(SaveDate).replace('(\'','').replace('\',)','')
            recent_saved_searches.append((q,s,SaveDate))
        print("$$$$$",recent_saved_searches)
        return recent_saved_searches

    def saved_jobs(self,limit,js_profile_id):
        cur.execute(
            "SELECT a.JobID, a.SaveDate, b.job_title from savedjobs a,jobs b where a.JobseekerID = %s and b.job_id=a.JobID LIMIT %s"%(
            js_profile_id,limit))
        recent_saved_jobs=[]
        for JobID,SaveDate,job_title in cur:
            if '(u\'' in str(JobID):
                job_title=str(job_title).replace('(u\'','').replace('\',)','')
                SaveDate=str(SaveDate).replace('(u\'','').replace('\',)','')
            else:
                job_title=str(job_title).replace('(\'','').replace('\',)','')
                SaveDate=str(SaveDate).replace('(\'','').replace('\',)','')
            recent_saved_jobs.append((job_title,SaveDate))
        print("$$$$$",recent_saved_jobs)
        return recent_saved_jobs

    def applied_jobs(self,limit,js_profile_id):
        cur.execute(
            "SELECT a.job_id, a.date_applied, b.job_title from jobseekers_jobs a, jobs b where a.jobseeker_profile_id = %s and b.job_id=a.job_id LIMIT %s"%(
            js_profile_id,limit))
        applied_jobs=[]
        for JobID,SaveDate,job_title in cur:
            if '(u\'' in str(JobID):
                job_title=str(job_title).replace('(u\'','').replace('\',)','')
                SaveDate=str(SaveDate).replace('(u\'','').replace('\',)','')
            else:
                job_title=str(job_title).replace('(\'','').replace('\',)','')
                SaveDate=str(SaveDate).replace('(\'','').replace('\',)','')
            applied_jobs.append((job_title,SaveDate))
        print("$$$$$",applied_jobs)
        return applied_jobs

    ''' def js_resumes(self, js_profile_id):
        cur.execute("SELECT resume_id,resume_title,last_updated,coverletter_path from resumes where jobseeker_profile_id = %s" %(js_profile_id))
        jbseekr_resumes = []
        for resume_id,resume_title,last_updated,coverletter_path in cur:
            if '(u\'' in str(resume_id):
                resume_title=str(resume_title).replace('(u\'','').replace('\',)','')
                last_updated=str(last_updated).replace('(u\'','').replace('\',)','')
                coverletter_path=str(coverletter_path).replace('(u\'','').replace('\',)','')
            else:
                resume_title=str(resume_title).replace('(\'','').replace('\',)','')
                last_updated=str(last_updated).replace('(\'','').replace('\',)','')
                coverletter_path=str(coverletter_path).replace('(\'','').replace('\',)','')
            jbseekr_resumes.append((resume_title, last_updated,coverletter_path))
        print ("$$$$$",jbseekr_resumes)
        return jbseekr_resumes

    def js_resumes(self, js_profile_id):
        cur.execute("SELECT resume_id,resume_path,resume_title,last_updated,coverletter_path from resumes where jobseeker_profile_id = %s" %(js_profile_id))
        jbseekr_resumes = []
        for resume_id,resume_path,resume_title,last_updated,coverletter_path in cur:
            if '(u\'' in str(resume_id):
                resume_title=str(resume_title).replace('(u\'','').replace('\',)','')
                last_updated=str(last_updated).replace('(u\'','').replace('\',)','')
                coverletter_path=str(coverletter_path).replace('(u\'','').replace('\',)','')
                resume_path=str(resume_path).replace('(u\'','').replace('\',)','')
            else:
                resume_title=str(resume_title).replace('(\'','').replace('\',)','')
                last_updated=str(last_updated).replace('(\'','').replace('\',)','')
                coverletter_path=str(coverletter_path).replace('(\'','').replace('\',)','')
                resume_path=str(resume_path).replace('(u\'','').replace('\',)','')
            jbseekr_resumes.append((resume_title, last_updated,coverletter_path,resume_path))
        print ("$$$$$",jbseekr_resumes)
        return jbseekr_resumes '''
		
#def  getenrolledjobseekerprograms(self,jsid)	
#	cur.execute("SELECT * FROM profiles AS p INNER JOIN jobseekers AS j ON p.`profile_id` = j.`jobseeker_profile_id` LEFT JOIN jobseekercaseworkers AS jw ON jw.JobseekerID = j.`jobseeker_profile_id` LEFT JOIN xousers xou ON xou.UserID = jw.CaseWorker LEFT JOIN jobcenters jc ON j.JobCenterID=jc.JobCenterID WHERE p.registration_type = 'Job Seeker' and p.profile_id=%s"(jsid))
#	jobseekerprograms=[]
#	for 
#	return mysql_query($query);
	

    def js_resumes(self,js_profile_id):
        cur.execute(
            "SELECT resume_id,resume_path,resume_title,last_updated,coverletter_path from resumes where jobseeker_profile_id = %s"%(
            js_profile_id))
        jbseekr_resumes=[]
        for resume_id,resume_path,resume_title,last_updated,coverletter_path in cur:
            if '(u\'' in str(resume_id):
                resume_title=str(resume_title).replace('(u\'','').replace('\',)','')
                last_updated=str(last_updated).replace('(u\'','').replace('\',)','')
                coverletter_path=str(coverletter_path).replace('(u\'','').replace('\',)','')
                resume_path=str(resume_path).replace('(u\'','').replace('\',)','')
                resume_id=str(resume_id).replace('(u\'','').replace('\',)','')
            else:
                resume_title=str(resume_title).replace('(\'','').replace('\',)','')
                last_updated=str(last_updated).replace('(\'','').replace('\',)','')
                coverletter_path=str(coverletter_path).replace('(\'','').replace('\',)','')
                resume_path=str(resume_path).replace('(u\'','').replace('\',)','')
                resume_id=str(resume_id).replace('(u\'','').replace('\',)','')
            jbseekr_resumes.append(
                (resume_title,last_updated,coverletter_path,resume_path,resume_id))
        print("######",jbseekr_resumes)
        return jbseekr_resumes

    def add_resume(self,resume_title="",text_resume="",resume_path="",
                   last_updated=datetime.datetime.utcnow(),server_id="2",jobseeker_profile_id="",
                   additional_information="",coverletter_path=""):
        try:
            resume_insert='''INSERT INTO resumes(resume_title,text_resume,resume_path,last_updated,server_id,jobseeker_profile_id,additional_information,coverletter_path) VALUES(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\')'''.format(
                resume_title,text_resume,resume_path,last_updated,server_id,jobseeker_profile_id,
                additional_information,coverletter_path)
            insert_cur=data.execute(conn,cur,resume_insert)
        except mysql.connector.Error as e:
            print("Error {}".format(e))
            return False

    def update_resume(self,resume_id="",resume_title="",text_resume="",resume_path="",
                      last_updated=datetime.datetime.utcnow()):
        try:
            resume_update='''UPDATE resumes set resume_title=\'{0}\',resume_path=\'{0}\',last_updated= \'{1}\', text_resume=\'{2}\' where resume_id=\'{3}\''''.format(
                resume_title,resume_path,last_updated,text_resume,resume_id)
            insert_cur=data.execute(conn,cur,resume_update)
        except mysql.connector.Error as e:
            print("Error {}".format(e))
            return False
			
         
    def edit_profile(self, profile_id):
        cur.execute("select p.profile_id, p.first_name, p.last_name, j.address_line1, j.address_line2, j.city, j.state, c.county_name, j.zip, j.phone, j.phone2, j.entity, j.one_stop_code, j.preferred_time, j.salary_expected, p.email, p.password, p.security_question1, p.security_answer1, p.security_question2, p.security_answer2 from profiles p, jobseekers j, counties c where p.profile_id=j.jobseeker_profile_id and j.county_id=c.county_id and p.profile_id='{}';".format(profile_id))
       #cur.execute("UPDATE profiles p, jobseekers j, counties c SET p.profile_id, p.first_name, p.last_name, j.address_line1, j.address_line2, j.city, j.state, c.county_name, j.zip, j.phone, j.phone2, j.entity, j.one_stop_code, j.preferred_time, j.salary_expected, p.email, p.password, p.security_question1, p.security_answer1, p.security_question2, p.security_answer2 where p.profile_id=j.jobseeker_profile_id and j.county_id=c.county_id and p.profile_id='{}';".format(profile_id))
        edit_profile = []
        for profile_id, first_name, last_name, address_line1, address_line2, city, state, county_name, zip, phone, phone2, entity, one_stop_code, preferred_time, salary_expected, email, password, security_question1, security_answer1, security_question2, security_answer2 in cur:
            if (first_name.count('(u\'')) > 0:
                profile_id=str(profile_id).replace('(u\'','').replace('\',)','')
                first_name = str(first_name).replace('(u\'','').replace('\',)','')
                last_name=str(last_name).replace('(u\'','').replace('\',)','')
                address_line1=str(address_line1).replace('(u\'','').replace('\',)','')
                address_line2=str(address_line2).replace('(u\'','').replace('\',)','')
                city=str(city).replace('(u\'','').replace('\',)','')
                state=str(state).replace('(u\'','').replace('\',)','')
                county_name=str(county_name).replace('(u\'','').replace('\',)','')
                zip=str(zip).replace('(u\'','').replace('\',)','')
                phone=str(phone).replace('(u\'','').replace('\',)','')
                phone2=str(phone2).replace('(u\'','').replace('\',)','')
                entity=str(entity).replace('(u\'','').replace('\',)','')
                one_stop_code=str(one_stop_code).replace('(u\'','').replace('\',)','')
                preferred_time=str(preferred_time).replace('(u\'','').replace('\',)','')
                salary_expected=str(salary_expected).replace('(u\'','').replace('\',)','')
                email=str(email).replace('(u\'','').replace('\',)','')
                security_question1=str(security_question1).replace('(u\'','').replace('\',)','')
                security_answer1=str(security_answer1).replace('(u\'','').replace('\',)','')
                security_question2=str(security_question2).replace('(u\'','').replace('\',)','')
                security_answer2=str(security_answer2).replace('(u\'','').replace('\',)','')
            else:
                profile_id=str(profile_id).replace('(\'','').replace('\',)','')
                first_name = str(first_name).replace('(\'','').replace('\',)','')
                last_name=str(last_name).replace('(\'','').replace('\',)','')
                address_line1=str(address_line1).replace('(\'','').replace('\',)','')
                address_line2=str(address_line2).replace('(\'','').replace('\',)','')
                city=str(city).replace('(\'','').replace('\',)','')
                state=str(state).replace('(\'','').replace('\',)','')
                county_name=str(county_name).replace('(\'','').replace('\',)','')
                zip=str(zip).replace('(\'','').replace('\',)','')
                phone=str(phone).replace('(\'','').replace('\',)','')
                phone2=str(phone2).replace('(\'','').replace('\',)','')
                entity=str(entity).replace('(\'','').replace('\',)','')
                one_stop_code=str(one_stop_code).replace('(\'','').replace('\',)','')
                preferred_time=str(preferred_time).replace('(\'','').replace('\',)','')
                salary_expected=str(salary_expected).replace('(\'','').replace('\',)','')
                email=str(email).replace('(\'','').replace('\',)','')
                security_question1=str(security_question1).replace('(\'','').replace('\',)','')
                security_answer1=str(security_answer1).replace('(\'','').replace('\',)','')
                security_question2=str(security_question2).replace('(\'','').replace('\',)','')
                security_answer2=str(security_answer2).replace('(\'','').replace('\',)','')
            edit_profile.append((profile_id, first_name, last_name, address_line1, address_line2, city, state, county_name, zip, phone, phone2, entity, one_stop_code, preferred_time, salary_expected, email, security_question1, security_answer1, security_question2, security_answer2))
        return edit_profile
		
    def save_searches(self,q="",s="",ProfileID="",SaveDate=datetime.datetime.utcnow()):
        try:
            search_insert='''INSERT INTO savedsearches(q,s,ProfileID,SaveDate) VALUES(\'{0}\',\'{1}\',\'{2}\',\'{3}\')'''.format(
                q,s,ProfileID,SaveDate)
            insert_cur=data.execute(conn,cur,search_insert)
        except mysql.connector.Error as e:
            print("Error {}".format(e))
            return False

    def save_jobs(self,JobseekerID="",JobID="",SaveDate=datetime.datetime.utcnow()):
        try:
            save_job_insert='''INSERT INTO savedjobs(JobseekerID,JobID,SaveDate) VALUES(\'{0}\',\'{1}\',\'{2}\')'''.format(
                JobseekerID,JobID,SaveDate)
            insert_cur=data.execute(conn,cur,save_job_insert)
        except mysql.connector.Error as e:
            print("Error {}".format(e))
            return False

    def saved_job_count(self,JobseekerID="",JobID=""):
        cur.execute("SELECT count(*) as saved_job_count from savedjobs where JobseekerID = %s and JobID = %s"%(
            JobseekerID,JobID))
        saved_job_cnt = ""
        for saved_job_count in cur:
            if (saved_job_count.count('(u\'')) > 0:
                saved_job_cnt = str(saved_job_count).replace('(u\'','').replace('\',)','')
            else:
                saved_job_cnt = str(saved_job_count).replace('(','').replace(',)','')
        return saved_job_cnt

    def remove_jobs(self,JobseekerID="",JobID=""):
        try:
            job_delete='''DELETE FROM savedjobs where JobseekerID = %s and JobID = %s'''%(
            JobseekerID,JobID)
            delete_cur=data.execute(conn,cur,job_delete)
        except mysql.connector.Error as e:
            print("Error {}".format(e))
            return False
    def apply_job(self,jobseeker_profile_id="",job_id="",resume_id="",date_applied=datetime.datetime.utcnow()):
        try:
            apply_job_insert='''INSERT INTO jobseekers_jobs(jobseeker_profile_id,job_id,resume_id,date_applied) VALUES(\'{0}\',\'{1}\',\'{2}\',\'{3}\')'''.format(
                jobseeker_profile_id,job_id,resume_id,date_applied)
            insert_cur=data.execute(conn,cur,apply_job_insert)
        except mysql.connector.Error as e:
            print("Error {}".format(e))
            return False
			
    def delete_resume(self,resume_id=""):
        try:
            resume_delete='''DELETE FROM resumes where resume_id=\'{0}\''''.format(resume_id)
            delete_cur=data.execute(conn,cur,resume_delete)
        except mysql.connector.Error as e:
            print("Error {}".format(e))
            return False
			
if __name__ == "__main__":
    application.run(debug=True)
