import os
import sys
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pyodbc
import time
import github
import json

# Initialize Flask
app = Flask(__name__)

# Setup Flask Restful framework
api = Api(app)

# Create connection to Azure SQL
#conn = pyodbc.connect(os.environ['WWIF'])

GITHUB_ORG = os.environ['GITHUB_ORG']
GITHUB_USER = os.environ['GITHUB_USER']
GITHUB_PASSWORD = os.environ['GITHUB_PASSWORD']
#GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']

class Queryable(Resource):
    def executeQueryJson(self, myquery):
        result = {}        
        cursor = conn.cursor()  
        try:
            cursor.execute(f"{myquery}")
            columns = [column[0] for column in cursor.description]
            result = []
            for row in cursor.fetchall():
                result.append(dict(zip(columns, row)))
            cursor.commit()    
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        finally:    
            cursor.close()
        return result

class GitHubTrafficCheck(Queryable):
    def get(self):   
        # if GITHUB_ACCESS_TOKEN is None and (GITHUB_USER is None or GITHUB_PASSWORD is None):
        #     sys.exit('You need to provide either github username & password or github access token: set env GITHUB_USER, GITHUB_PASSWORD, GITHUB_ACCESS_TOKEN')
        # if GITHUB_ACCESS_TOKEN is not None and GITHUB_USER is None and GITHUB_ORG is None:
        #     sys.exit('When providing access token, please provide either repo user or repo org: set env GITHUB_USER, GITHUB_ORG')
        
        org=GITHUB_ORG
        user=GITHUB_USER
        password=GITHUB_PASSWORD
        # token=GITHUB_ACCESS_TOKEN

        if org is None:
            org = user

        # if token is not None:
        #     user = None
        #     password = None

        gh = github.GitHub(username=user, password=password, access_token=None)

        for item in gh.orgs('gepardec/repos?type=public&sort=created').get():
            print(item.name)
            try:
                gh.repos(org, item.name).collaborators(user).get()
                views_14_days = gh.repos(org, item.name).traffic.views.get()
                for view_per_day in views_14_days['views']:
                    timestamp = view_per_day['timestamp']
                    data = { 'uniques': view_per_day['uniques'], 'count': view_per_day['count']}    
                    print(timestamp, item.name, data)
            except:
                print("no access")
    
        # result = self.executeQueryJson(f"SELECT ID,habit,occured FROM habits WHERE CONVERT(VARCHAR, habit) = '{habit}' ORDER BY occured DESC")   
        return {}, 200

    def post(self):   
        return self.get()

class GitHubViewTraffic(Queryable):
    def get(self):   
        return {}, 200

    def post(self):   
        return self.get()
    
# Create API routes
api.add_resource(GitHubTrafficCheck, '/check')
api.add_resource(GitHubViewTraffic, '/views')
