# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import HttpResponse

from django.conf import settings
import requests
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


import twitter


url = 'http://127.0.0.1:8000/googlesearch/search_twitter/'
@csrf_exempt
def search_twitter(request):
	print "in views"
	if request.method == 'POST':
		data = json.loads(request.body)
		query = data['query']
		Twitter_Consumer_Key = settings.TWITTER_CONSUMER_KEY
		Twitter_Consumer_Secret = settings.TWITTER_CONSUMER_SECRET

		Access_Token = settings.ACCESS_TOKEN
		Access_Token_Secret = settings.ACCESS_TOKEN_SECRET

		api = twitter.Api(consumer_key= Twitter_Consumer_Key,
                      consumer_secret= Twitter_Consumer_Secret,
                      access_token_key= Access_Token,
                      access_token_secret= Access_Token_Secret)
		#print(api.VerifyCredentials())
		# try:
		# 	api.PostUpdates("Test Status 3 posted from Twitter API.")
		# except Exception, e:
		# 	return HttpResponse(json.dumps({'message': "error"}))
		
		#url = "https://twitter.com/search?q="+query+"&src=typd"
		results = api.GetSearch(raw_query="q="+query+"&src=typd")
		#&result_type=recent&count=5
		status = results[0]
		print status.text
		return HttpResponse(json.dumps({'message': status.text}))



@csrf_exempt
def search_duckgo(request):
	print "in views"
	if request.method == 'POST':
		data = json.loads(request.body)
		query = data['query']
		#url = 'http://api.duckduckgo.com/?q='+query
		req = requests.get('http://api.duckduckgo.com/?q='+query+'&format=json')
		json_response = req.json()
		print json_response
		return HttpResponse(json.dumps({'message':json_response['Abstract']}))

@csrf_exempt
def search_google(request):
	print "in views"
	if request.method == 'POST':
		data = json.loads(request.body)
		query = data['query']
		req = requests.get('https://www.googleapis.com/customsearch/v1?key='
			+ settings.GOOGLE_API_KEY 
			+'&cx=017576662512468239146:omuauf_lfve&q='+query)
		
		#these 2 lines are for test
		# json_response = req.text
		# print json_response

		json_response = req.json()
		print json_response
		json_response = json_response['items'] 
		json_response = json_response[1] #1st result from google custom search
		json_response = json_response['title'] #title from first search



		#now from duckduckgo
		return HttpResponse(json.dumps({'message':json_response}))	

@csrf_exempt
def search_twitter(request):
	print "in views"
	if request.method == 'POST':
		data = json.loads(request.body)
		query = data['query']
