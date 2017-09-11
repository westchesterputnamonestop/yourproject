#!/var/www/yourproject/yourprojectenv/bin/python3
from flask import Flask
application = Flask(__name__)
import mysql.connector


class Database():
    
# Database class initiates a mysql connection.
    

    def connection(self, user="root", password="Armlock21@", host="localhost", database="wpos_dev"):
        """
        Connection method will create a cursor for executing queries.
            args
             user(str): username for connecting to DB
             password(str): password for connecting to DB
             host(str): Hot ip to connect with DB
             database(str): Database to use
            returns
             connection(obj): mysql connection object
             cursor(obj): cursor object for queries
        """
        try:
            connection = mysql.connector.Connect(user=user, password=password, host=host, database=database)
            cursor = connection.cursor(buffered=True)
            return cursor, connection

        except Exception as e:
            return str(e)

    def execute(self, connection, cursor, query):
        """
        Execute method will use cursor for executing queries.
            args
             connection(obj): mysql connection object
             cursor(obj): cursor object for queries
             query(str): query
            returns
             connection(obj): mysql connection object
             cursor(obj): cursor object for queries
        """
        try:
            print ("execute def called")
            print (query)

            cursor.execute(query)
            connection.commit()
            #cursor.close()
            return cursor

        except Exception as e:
            return str(e)

    def dis_connection(self, connection):
        """
        Connection method will create a cursor for executing queries.
             args
              connection(obj): mysql object
             returns
        """
        try:
            connection.colse()

        except Exception as e:
            return str(e)

if __name__ == '__main__':
    application.run(debug=True)
