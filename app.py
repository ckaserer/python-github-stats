import os
import sys
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pyodbc
import time
import datetime
import github
import json
from typing import TypeVar
from flask_cors import CORS


# Initialize Flask
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)


# Setup Flask Restful framework
api = Api(app)

# Create connection to Azure SQL
conn = pyodbc.connect(os.environ['WWIF'])

GITHUB_ORG = os.getenv('GITHUB_ORG', None)
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', None)

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
        finally:    
            cursor.close()
        return result


class GitHubTrafficCheck(Queryable):
    def get(self):   
        if GITHUB_ORG is None or GITHUB_TOKEN is None:
            sys.exit('You need to provide github org & token: set env GITHUB_ORG, GITHUB_TOKEN')
        
        gh = github.GitHub(access_token=GITHUB_TOKEN)
        result = []
        for item in gh.orgs('gepardec/repos?type=public').get():
            try:
                views_14_days = gh.repos(GITHUB_ORG, item.name).traffic.views.get()
                for view_per_day in views_14_days['views']:                    
                    # Convert String Timestamp to Unix String looks like: 2020-06-18T00:00:00Z
                    unixtime = time.mktime(datetime.datetime.strptime(view_per_day['timestamp'], '%Y-%m-%dT%H:%M:%SZ').timetuple())
                    print(f"INSERT INTO repostats(repo, viewDate, viewCount, uniques) VALUES ('{GITHUB_ORG}/{item.name}', {int(unixtime)}, {view_per_day['count']}, {view_per_day['uniques']})")
                    try:
                        result.append(self.executeQueryJson(f"INSERT INTO repostats(repo, viewDate, viewCount, uniques) OUTPUT INSERTED.repo,INSERTED.viewDate,INSERTED.viewCount,INSERTED.uniques VALUES ('{GITHUB_ORG}/{item.name}', {int(unixtime)}, {int(view_per_day['count'])}, {int(view_per_day['uniques'])})"))
                    except:
                        # print(f"UPDATE repostats SET viewCount = {int(view_per_day['count'])}, uniques = {int(view_per_day['uniques'])} OUTPUT INSERTED.repo,INSERTED.viewDate,INSERTED.viewCount,INSERTED.uniques WHERE repo = '{GITHUB_ORG}/{item.name}' AND viewDate = {int(unixtime)}")
                        result.append(self.executeQueryJson(f"UPDATE repostats SET viewCount = {int(view_per_day['count'])}, uniques = {int(view_per_day['uniques'])} OUTPUT INSERTED.repo,INSERTED.viewDate,INSERTED.viewCount,INSERTED.uniques WHERE repo = '{GITHUB_ORG}/{item.name}' AND viewDate = {int(unixtime)}"))

                    timestamp = view_per_day['timestamp']
                    data = { 'uniques': view_per_day['uniques'], 'count': view_per_day['count']}    
                    print(item.name, timestamp, data)
            except:
                print(item.name,"no access",file=sys.stderr)
    
        # result = self.executeQueryJson(f"SELECT ID,habit,occured FROM habits WHERE CONVERT(VARCHAR, habit) = '{habit}' ORDER BY occured DESC")   
        return result, 200

    def post(self):   
        return self.get()

class GitHubViewTraffic(Queryable):
    def get(self, org, repo):   
        result = self.executeQueryJson(f"SELECT repo,viewDate,viewCount,uniques FROM repostats WHERE repo = '{org}/{repo}' ORDER BY viewDate DESC")   
        return result, 200

    def post(self, org, repo):   
        return self.get(org, repo)
    
# Create API routes
api.add_resource(GitHubTrafficCheck, '/collect')
api.add_resource(GitHubViewTraffic, '/view', '/view/<org>/<repo>')
