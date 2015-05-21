#!python

import requests
import json
from json import JSONEncoder
import ConfigParser
import urllib
import collections
from collections import defaultdict
import StringIO
import csv
import os
import jsonrpc
import sqlite3
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
requests.packages.urllib3.disable_warnings()
import sys;
reload(sys);
sys.setdefaultencoding("utf8")
#params = JSONEncoder().encode({'code': "117A479E", 'client_id': "44db761b802994857956a87eace751657a976e2abc911aec10bf5127f0b3d4f3", "client_secret": "d7447910a3cc56c69fc5962d15a2d095234f80cbb10118487d38ad66e2a39a42", "redirect_uri": "urn:ietf:wg:oauth:2.0:oob", "grant_type": "authorization_code"})
#headers = {"Content-type": "application/json", "Accept": "text/plain", "Content-length": repr(len(params))}
#r = requests.post("https://api-v2launch.trakt.tv/oauth/token", data=params, headers=headers)
#response = json.loads(r.text)
#print response
def trendingMovies():

	header = {'Content-type': 'application/json', "trakt-api-version": "2", 'trakt-api-key': '44db761b802994857956a87eace751657a976e2abc911aec10bf5127f0b3d4f3'}
	data = requests.get("https://api-v2launch.trakt.tv/movies/trending?page=1&limit=400", headers=header)
	json_data = json.loads(data.text)
	for i in json_data:
		print i['movie']['title']

def popularMovies():

	header = {'Content-type': 'application/json', "trakt-api-version": "2", 'trakt-api-key': '44db761b802994857956a87eace751657a976e2abc911aec10bf5127f0b3d4f3'}
	data = requests.get("https://api-v2launch.trakt.tv/movies/popular?page=1&limit=400", headers=header)
	json_data = json.loads(data.text)
	for i in json_data:
		print i['title']

def updatedMovies():

	header = {'Content-type': 'application/json', "trakt-api-version": "2", 'trakt-api-key': '44db761b802994857956a87eace751657a976e2abc911aec10bf5127f0b3d4f3'}
	data = requests.get("https://api-v2launch.trakt.tv/movies/updates?page=1&limit=200", headers=header)
	json_data = json.loads(data.text)
	for i in json_data:
		print i['movie']['title']
def relatedMovies():

	header = {'Content-type': 'application/json', "limit": "50", "trakt-api-version": "2", 'trakt-api-key': '44db761b802994857956a87eace751657a976e2abc911aec10bf5127f0b3d4f3'}
	data = requests.get("https://api-v2launch.trakt.tv/movies/tt1632708/related?page=1&limit=200", headers=header)
	json_data = json.loads(data.text)
	for i in json_data:
		print i['title']
trendingMovies()
popularMovies()
updatedMovies()
relatedMovies()