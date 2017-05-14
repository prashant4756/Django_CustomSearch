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
from multiprocessing import Process,Manager

@csrf_exempt
def custom_search(request):
	
	manager = Manager()
	q = manager.Queue()
	print q.qsize()
	start_time = timeit.default_timer()
	return_dict = manager.dict()
	if request.method == 'POST':
		data = json.loads(request.body)
		query = data['query']

		p1 = Process(target=search_google, args=(query,return_dict,q,"google process"))
    	p1.daemon = True
    	p1.name ="google process"
    	q.put(p1.name)
    	print p1

    	p2 = Process(target=search_twitter, args=(query,return_dict,q,"twitter process"))
    	p2.daemon = True
    	p2.name ="twitter process"
    	q.put(p2.name)
    	print p2

    	p3 = Process(target=search_duckgo, args=(query,return_dict,q,"duckduckgo process"))
    	p3.daemon = True
    	p3.name ="duckduckgo process"
    	q.put(p3.name)
    	print p3

    	print q.qsize()
    	  	
    	p1.start()
    	p2.start()
    	p3.start()
    	

    	print "before p1 join"
    	p1.join(1)
    	print "after p1 join"
    	p2.join(1)
    	print "after p2 join"
    	p3.join(1)
    	print "after p3 join"

    	# q.join()
    	print "after q.join()"
    	if p1.is_alive(): 
    		print "timed out1"
    		p1.terminate()
    		p1.join()
    		return_dict[p3.name]= "timed out"

    	if p2.is_alive(): 
    		print "timed out2"
    		p2.terminate()
    		p2.join()
    		return_dict[p3.name]= "timed out"

    	if p3.is_alive(): 
    		print "timed out3"
    		p3.terminate()
    		p3.join()
    		return_dict[p3.name]= "timed out"

    	print "after time outs"
    	end_time = timeit.default_timer()
    	time_taken = end_time - start_time
    	print "time taken: "+str(start_time)+" and "+ str(end_time)+" : "+str(time_taken)

    	print return_dict.values()

    	if time_taken > 1.0:
    		return HttpResponse(json.dumps(
    		{"query":query,
			"results": "error: time taken is greater than 1 sec"
			}))

    	else:
	    	google_data = return_dict["google process"]
	    	twitter_data = return_dict["twitter process"]
	    	duckgo_data = return_dict["duckduckgo process"]

	    	return HttpResponse(json.dumps(
	    		{"query":query,
				"results":{
					"google": google_data,
					"twitter": twitter_data,
					"duckduckgo": duckgo_data
				}
			}))
		

def search_twitter(query,return_dict,q,key):
	p = q.get()
	print "in twitter "+p+" "+str(q.qsize())
	if query != "":
		print "Twitter---------------------------->\n"
		api = twitter.Api(consumer_key= settings.TWITTER_CONSUMER_KEY,
                      consumer_secret= settings.TWITTER_CONSUMER_SECRET,
                      access_token_key= settings.ACCESS_TOKEN,
                      access_token_secret= settings.ACCESS_TOKEN_SECRET)
		#print(api.VerifyCredentials())
		try:
			results = api.GetSearch(raw_query="q="+query+"&src=typd&count=1")
			status = results[0]
			data = status.text
			q.task_done()
			# print "printing data in function twitter: ->\n"+ data
			return_dict[key] = data
		except Exception, e:
			return_dict[key] = "somthing went wrong at twitter"		

		
		# return HttpResponse(json.dumps({'message': status.text}))


def search_duckgo(query,return_dict,q,key):
	p = q.get()
	print "in duckduckgo"+p+" "+str(q.qsize())
	if query != "":
		try:
			print "duckduckgo ----------------------------->\n"
			req = requests.get('http://api.duckduckgo.com/?q='+query+'&format=json&num=1')
			json_response = req.json()
			# print "duckduckgo------------------------------>\n\n\n\n"
			# print json_response
			related_topics = json_response['RelatedTopics']		
			first_result = related_topics[0]
			data = first_result['Text'] + json_response['Abstract']
			q.task_done()
			# print "printing data in function duckduckgo: ->\n"+ data
			return_dict[key] = data
		except Exception, e:
			return_dict[key] = "somthing went wrong at duckduckgo"

		
def search_google(query,return_dict,q,key):
	p = q.get()
	print "in google"+p+" "+str(q.qsize())
	if query != "":
		# search for space seperated 
		query = query.replace(" ", "%20")
		try:
			req = requests.get('https://www.googleapis.com/customsearch/v1?key='
			+ settings.GOOGLE_API_KEY 
			+'&cx=017576662512468239146:omuauf_lfve&q='+query
			+'&num=1')

			json_response = req.json()
			print "Google ----------------------------->\n"
			json_response = json_response['items'] 
			json_response = json_response[0] #1st result from google custom search
			snippet = json_response['snippet'] #title from first search
			data = snippet
			q.task_done()
			# print "printing data in function google: ->\n"+ data
			return_dict[key] = data
		except Exception, e:
			return_dict[key] = "somthing went wrong at Google"
