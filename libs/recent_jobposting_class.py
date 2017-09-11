#all recent job postings
from flask import Flask, render_template, request
from db import Database
import datetime

application = Flask(__name__)
data = Database()
cur, conn = data.connection()


class RecentJob:
#Jobseeker Profile page recent job postings 
    def recent_job(self, keyword=None, limit=10, offset=0):
        print("Keyword in recent_jon ---> {}".format(keyword))
        if keyword:
            if keyword[0] and not keyword[1]:
                keyword = keyword[0] + '%'
                cmd="SELECT j.job_id,j.job_title,j.job_city,j.job_state,jl.job_level_name,j.publish_date FROM jobs j, job_levels jl WHERE j.job_level_id=jl.job_level_id and j.job_title LIKE '"+keyword+"' ORDER BY j.publish_date desc LIMIT %s OFFSET %s;" %(limit, offset)
            elif keyword[1] and not keyword[0]:
                sector = keyword[1]
                cmd="select j.job_id,j.job_title,j.job_city,j.job_state,jl.job_level_name,j.publish_date from jobs j, job_levels jl, jobs_sectors js, sectors s where j.job_level_id=jl.job_level_id and j.job_id=js.job_id and js.sector_id=s.sector_id and s.sector_name='"+sector+"' ORDER BY j.publish_date desc limit %s offset %s;" %(limit, offset)
            elif keyword[1] and keyword[0]:
                sector_value = keyword[1]
                keyword= keyword[0]+ '%'
                cmd="select j.job_id,j.job_title,j.job_city,j.job_state,jl.job_level_name,j.publish_date from jobs j, job_levels jl, jobs_sectors js, sectors s where j.job_level_id=jl.job_level_id and j.job_id=js.job_id and js.sector_id=s.sector_id and j.job_title LIKE '"+keyword+"' and s.sector_name='"+sector_value+"' ORDER BY j.publish_date desc limit %s offset %s;" %(limit, offset)
            else:
                cmd="SELECT j.job_id,j.job_title,j.job_city,j.job_state,jl.job_level_name,j.publish_date FROM jobs j, job_levels jl WHERE j.job_level_id=jl.job_level_id ORDER BY j.publish_date desc LIMIT %s OFFSET %s;"%(limit,offset)
        else:
            cmd="SELECT j.job_id,j.job_title,j.job_city,j.job_state,jl.job_level_name,j.publish_date FROM jobs j, job_levels jl WHERE j.job_level_id=jl.job_level_id ORDER BY j.publish_date desc LIMIT %s OFFSET %s;"%(limit,offset)
        print ("###################",cmd)
        cur.execute(cmd)
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
            recentjob.append((job_id, job_title, job_level_name, str(job_city+', '+job_state), publish_date))
        print ("$$$$$",recentjob)
        return recentjob

    def total_jobs(self,keyword=None):
        print("Keyword in recent_jon ---> {}".format(keyword))
        if keyword:
            if keyword[0] and not keyword[1]:
                keyword = keyword[0] + '%'
                cmd="SELECT j.job_id,j.job_title,j.job_city,j.job_state,jl.job_level_name,j.publish_date FROM jobs j, job_levels jl WHERE j.job_level_id=jl.job_level_id and j.job_title LIKE '"+keyword+"' ORDER BY j.publish_date;"
            elif keyword[1] and not keyword[0]:
                sector = keyword[1]
                cmd="select j.job_id,j.job_title,j.job_city,j.job_state,jl.job_level_name,j.publish_date from jobs j, job_levels jl, jobs_sectors js, sectors s where j.job_level_id=jl.job_level_id and j.job_id=js.job_id and js.sector_id=s.sector_id and s.sector_name='"+sector+"' ORDER BY j.publish_date;"
            elif keyword[1] and keyword[0]:
                sector_value = keyword[1]
                keyword= keyword[0]+ '%'
                cmd="select j.job_id,j.job_title,j.job_city,j.job_state,jl.job_level_name,j.publish_date from jobs j, job_levels jl, jobs_sectors js, sectors s where j.job_level_id=jl.job_level_id and j.job_id=js.job_id and js.sector_id=s.sector_id and j.job_title LIKE '"+keyword+"' and s.sector_name='"+sector_value+"' ORDER BY j.publish_date;"
            else:
                cmd="SELECT j.job_id,j.job_title,j.job_city,j.job_state,jl.job_level_name,j.publish_date FROM jobs j, job_levels jl WHERE j.job_level_id=jl.job_level_id ORDER BY j.publish_date;"
        else:
            cmd="SELECT j.job_id,j.job_title,j.job_city,j.job_state,jl.job_level_name,j.publish_date FROM jobs j, job_levels jl WHERE j.job_level_id=jl.job_level_id ORDER BY j.publish_date;"
        print("###################",cmd)
        # if not keyword:
        #     cmd = "SELECT j.job_id,j.job_title,j.job_city,j.job_state,jl.job_level_name,j.publish_date FROM jobs j, job_levels jl where j.job_level_id=jl.job_level_id ORDER BY j.publish_date;"
        # else:
        #     keyword = keyword + '%'
        #     cmd = "SELECT j.job_id,j.job_title,j.job_city,j.job_state,jl.job_level_name,j.publish_date FROM jobs j, job_levels jl where j.job_level_id=jl.job_level_id and j.job_title LIKE '"+keyword+"' ORDER BY j.publish_date;"
        cur.execute(cmd)
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
            recentjob.append((job_id, job_title, job_level_name, str(job_city+', '+job_state), publish_date))
        return recentjob
 

if __name__ == "__main__":
    application.run(debug=True)
	
