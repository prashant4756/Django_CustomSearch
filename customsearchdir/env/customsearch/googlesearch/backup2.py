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
import timeit
#import multiprocessing
from multiprocessing import Process
from Queue import Queue

def search_twitter(query):
	if query != "":
		print "Twitter---------------------------->\n\n\n\n\n"
		api = twitter.Api(consumer_key= settings.TWITTER_CONSUMER_KEY,
                      consumer_secret= settings.TWITTER_CONSUMER_SECRET,
                      access_token_key= settings.ACCESS_TOKEN,
                      access_token_secret= settings.ACCESS_TOKEN_SECRET)
		#print(api.VerifyCredentials())
		try:
			results = api.GetSearch(raw_query="q="+query+"&src=typd&count=1")
			status = results[0]
			print status.text
			twitter_data = status.text
			q.get()
			q.task_done()
			print "after task 1"
			return status.text
		except Exception, e:
			return "somthing went wrong at twitter"		

		
		# return HttpResponse(json.dumps({'message': status.text}))


def search_duckgo(query):
	if query != "":
		try:
			print "duckduckgo ----------------------------->\n\n\n\n\n"
			req = requests.get('http://api.duckduckgo.com/?q='+query+'&format=json&num=1')
			json_response = req.json()
			# print "duckduckgo------------------------------>\n\n\n\n"
			# print json_response
			related_topics = json_response['RelatedTopics']		
			first_result = related_topics[0]
			print first_result['Text'] + json_response['Abstract']
			duckgo_data = first_result['Text'] + json_response['Abstract']
			q.get()
			q.task_done()
			print "after task 2"
			return first_result['Text'] + json_response['Abstract']
		except Exception, e:
			return "somthing went wrong at duckduckgo"

		
		# return HttpResponse(json.dumps({'message':json_response['Abstract']}))

def search_google(query):
	if query != "":
		try:
			req = requests.get('https://www.googleapis.com/customsearch/v1?key='
			+ settings.GOOGLE_API_KEY 
			+'&cx=017576662512468239146:omuauf_lfve&q='+query
			+'&num=1')
		
			#these 2 lines are for test
			# json_response = req.text
			# print json_response

			json_response = req.json()
			print "Google ----------------------------->\n\n\n\n\n"
			# print json_response
			json_response = json_response['items'] 
			json_response = json_response[0] #1st result from google custom search
			snippet = json_response['snippet'] #title from first search
			google_data = snippet
			q.get()
			q.task_done()
			print "after task 3"
			print snippet
	  		return snippet
			#return HttpResponse(json.dumps({'message':json_response}))	
	
		except Exception, e:
			return "somthing went wrong at Google"
		
@csrf_exempt
def custom_search(request):
	start_time = timeit.default_timer()
	if request.method == 'POST':
		data = json.loads(request.body)
		query = data['query']
	
		q = Queue()
		p1 = Process(target=search_google, args=(query,))
    	p1.start()
    	q.put(p1)
    	p2 = Process(target=search_twitter, args=(query,))
    	p2.start()
    	q.put(p2)
    	p3 = Process(target=search_duckgo, args=(query,))
    	p3.start()
    	q.put(p3)

    	# google_data = p1.join
    	# twitter_data = p2.join
    	# duckgo_data = p3.join
    	q.join()
    	end_time = timeit.default_timer()
    	print "time taken: "+str(start_time)+" and "+ str(end_time)+" : "+str(end_time - start_time)

    	if google_data is None:
    		google_data = "None"
    	if twitter_data is None:
    		twitter_data = "None"
    	if duckgo_data is None:
    		duckgo_data = "None"

    	return HttpResponse(json.dumps({"query":query,
			"results":{
				"google": google_data,
				"twitter": twitter_data,
				"duckduckgo": duckgo_data
			}
		}))
		# google_data = search_google(query)
		# twitter_data = search_twitter(query)
		# duckgo_data = search_duckgo(query)

		# process = q.get()
		
