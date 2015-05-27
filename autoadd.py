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
import sys
import os
import jsonrpc
import sqlite3
from requests.auth import HTTPBasicAuth

configParser = ConfigParser.RawConfigParser()   
configFilePath = r'config'
configParser.read(configFilePath)
couchPotatoURL = configParser.get('couchpotato', 'URL')
couchPotatoAPIKey = configParser.get('couchpotato', 'APIKey')
nzbGetAPIUser = configParser.get('nzbget', 'user')
nzbGetAPIPassword = configParser.get('nzbget', 'password')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data
def imdbRequest ( name ):
	try:
		url = 'http://www.omdbapi.com/?t=' + urllib.quote_plus(name)
		request = requests.get(url)
		json_data = json.loads(request.text)
		if json_data['Response'] == "False":
			print "Movie not found on IMDB"
			return
		imdbID = json_data['imdbID']
		couchPotatoSearch(name, imdbID)
	except requests.exceptions.RequestException, e:
	    print 'FAIL:', e
def couchPotatoAdd ( imdbID ):
	try:
		request = requests.get(couchPotatoURL + '/couchpotato/api/' + couchPotatoAPIKey + '/movie.add/?identifier=' + imdbID)
		json_data = json.loads(request.text)
		#movieID = json_data['movie']['_id']
		#request = requests.get(couchPotatoURL + '/couchpotato/api/' + couchPotatoAPIKey + '/movie.delete/?delete_from=wanted&id=' + movieID)
	except requests.exceptions.RequestException, e:
	    print 'FAIL:', e
def couchPotatoDownload ( movieID ):
	try:
		request = requests.get(couchPotatoURL + '/couchpotato/api/' + couchPotatoAPIKey + '/media.get?id=' + movieID)
		json_data = json.loads(request.text)
		movieID = json_data['movie']['_id']

	except requests.exceptions.RequestException, e:
	    print 'FAIL:', e
def couchPotatoSearch (name, imdbID):
	try:
		url = couchPotatoURL + '/couchpotato/api/' + couchPotatoAPIKey + '/media.list/?search=' + urllib.quote_plus(name)
		request = requests.get(url)
		json_data = json.loads(request.text)
		count = json_data['total']
		fieldnames = ["released","title"]
		comv=""
		
		for i in range(0, count):
			comv += json_data['movies'][i]['info']['released'] + "," + json_data['movies'][i]['title'] + "\n"

		csvfile = open("movies.csv", "wb")
		csvfile.write(comv)
		csvfile.close()


		csvfile = open("movies.csv", "r")
		reader =csv.DictReader(csvfile, fieldnames)
		out = json.dumps([r for r in reader])
		json_data = json.dumps(out)
		json_data  = json_data.replace('\\', '').strip()
		json_data = json_data[1:-1]
		json_data = json.loads(json_data)
		name = name.replace('\n', '').strip()
		csvfile.close()
		if os.path.isfile("movies.csv"):
		        os.remove("movies.csv")
		if count == 0:
			print bcolors.OKGREEN + "Movie (" + name + ") not found in the CouchPotato Database. Adding now!"+ bcolors.ENDC
			couchPotatoAdd(imdbID)
		else:
			print bcolors.WARNING + "The following movies were found in your library that matched your search terms" + bcolors.ENDC
			for i in range(0, count):
				title = json_data[i]['title']
				release = json_data[i]['released']
				print bcolors.BOLD + "Movie Title: " + bcolors.ENDC + title + bcolors.BOLD + "\n Release Date: " + bcolors.ENDC + release + "\n\n"	

		#print json.dumps(json_data[0], sort_keys=True, indent=4)
	except requests.exceptions.RequestException, e:
	    print 'FAIL:', e

with open('movielist.txt') as f:
	for line in f:
	 	imdbRequest (line)
