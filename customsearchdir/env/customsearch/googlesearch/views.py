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


def search_twitter(query):
	if query != "":
		Twitter_Consumer_Key = settings.TWITTER_CONSUMER_KEY
		Twitter_Consumer_Secret = settings.TWITTER_CONSUMER_SECRET

		Access_Token = settings.ACCESS_TOKEN
		Access_Token_Secret = settings.ACCESS_TOKEN_SECRET

		api = twitter.Api(consumer_key= Twitter_Consumer_Key,
                      consumer_secret= Twitter_Consumer_Secret,
                      access_token_key= Access_Token,
                      access_token_secret= Access_Token_Secret)
		#print(api.VerifyCredentials())
		try:
			results = api.GetSearch(raw_query="q="+query+"&src=typd")
			status = results[0]
			return status.text
		except Exception, e:
			return "somthing went wrong at twitter"		

		
		# return HttpResponse(json.dumps({'message': status.text}))


def search_duckgo(query):
	print "in views"
	if query != "":
		try:
			req = requests.get('http://api.duckduckgo.com/?q='+query+'&format=json')
			json_response = req.json()
			print "duckduckgo------------------------------>\n\n\n\n"
			print json_response
			related_topics = json_response['RelatedTopics']		
			first_result = related_topics[0]
			return first_result['Text'] + json_response['Abstract']
		except Exception, e:
			return "somthing went wrong at duckduckgo"

		
		# return HttpResponse(json.dumps({'message':json_response['Abstract']}))

def search_google(query):
	print "in views"
	if query != "":
		try:
			req = requests.get('https://www.googleapis.com/customsearch/v1?key='
			+ settings.GOOGLE_API_KEY 
			+'&cx=017576662512468239146:omuauf_lfve&q='+query)
		
			#these 2 lines are for test
			# json_response = req.text
			# print json_response

			json_response = req.json()
			print "Google ----------------------------->\n\n\n\n\n"
			print json_response
			json_response = json_response['items'] 
			json_response = json_response[0] #1st result from google custom search
			json_response = json_response['snippet'] #title from first search

	  		return json_response
			#return HttpResponse(json.dumps({'message':json_response}))	
	
		except Exception, e:
			return "somthing went wrong at Google"
		
@csrf_exempt
def custom_search(request):
	print "in views"
	if request.method == 'POST':
		data = json.loads(request.body)
		query = data['query']

		google_data = search_google(query)
		twitter_data = search_twitter(query)
		duckgo_data = search_duckgo(query)

		return HttpResponse(json.dumps({"query":query,
			"results":{
				"google": google_data,
				"twitter": twitter_data,
				"duckduckgo": duckgo_data
			}
		}))