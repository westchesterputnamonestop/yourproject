from flask import Flask, render_template, request
from db import Database
import json
import datetime
application = Flask(__name__)
data = Database()
cur, conn = data.connection()

class job_posting:
    
      def selected_sectors(self,job_id=None)
          cur.execute=("SELECT js.job_id,js.sector_id,s.sector_name FROM jobs_sectors js, sectors s WHERE job_id=".$job_id." AND js.sector_id=s.sector_id") 
     return $sel_sectors_res;
