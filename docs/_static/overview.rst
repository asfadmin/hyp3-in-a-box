Section
        Observations
                ?:Questions
                A:Possibly an answer



Finding new granules:
	lambda_function.lambda_handler is triggered by automatic AWS event
	lambda_function.lambda_handler calls find_new.granule_events
	find_new.granule_events calls find_new.get_new_granules_between for the time since the last call up to the time it's called
	find_new.granules_between calls find_new.make_cmr_query
	find_new.make_cmr_query creates a CMR object (from modules/granule_search/src/granule_search/cmr/cmr.py)
	from make_cmr_query via the CMR object:
	the timeframe that should be searched is added to the search parameters of te CMR object and formatted
	the CMR object sends an HTTP request to the earthdata server, the response from the server should be the granules that were recorded in that timeframe
	        ?: what comunicates the geographic area of the granules that we want? seems like it should be done in the request to the earthdata server. Could also be done afterwards(pote
                   ntialy wasteful). Couldn't find either.

Creating new subscriptions:
	user creates new subscriptions via the html page created by the system.
	back end seems to be done by utility/add_subs/src/subscriptions.py
	has subscriptions.make and subscriptions.make_sub
	make creates multiple subscriptions from a file
	make instantiates "api" class from api_key username and url (created by asf_hyp3.API()
	make calls make_sub to create each subscription
	actual creation is done by the API class
	   ?: what function is actually called by form submission on the html page (what is the actual entry point to the back end?)
	   can make_sub be called without make(if so where does the api variable come from, if not is a file created for each single new subscription?) Where the heck is the source file for
           the API class (asf_hyp3)??!
           where is timeframe data included in the subscription (the make_sub function just uses required args

Events:
	"Events" are actually just data, normally strings, often in json format this is just the way
	that the functions use AWS services to communicate between machines.
		?: which event triggers the lambda handler for find_new_granules?
		A: done by AWS automatically

Environments:
	what supplies the data in os.environ that is used in the setup for various environments?
	os.environ seems to look at data from the os so presumably this is set up by AWS either
	with instructions fromm the provided CloudFormation template or done this way automatically.

Processing:
	A hyp3_Daemon manages each worker shutting it down if it's been idle for too long(currently
	2 minutes). The Daemon checks for new jobs(currently every second), when a new job is found 
	the Daemon calls hyp3_process.process_job which will call the processing function registered
	with the worker and return either a success or fail event that will be used by the Daemon to
	trigger the e-mail aparatus. 
	
	The worker is passed to the Daemon during the Daemon's creation (i'm not sure where the worker
	is created, maybe AWS?). The worker calls it's handler function. Since I don't know where the 
	worker is created i'm not sure what determines what the handler function is but it looks
	like the handler.make_hyp3_processing_function_from function which adds the filesystem 
	management to a handler. The current handler that's being used seems to be rtc-snap.handler 
	which downloads the granule and makes a command line call to the procSentinelRTC-3.py program
	to do the actual processing (although it could call anything if configured so)
		?: the handler.hyp3_wrapper looks like it's what's being called by the worker but it's
		wrapped by the handler.make_hyp3_processing_function_from function which takes a 
		handler function. Is this one of those Python things where you run a function on a
		function? if so where is the function to be modified passed to 
		handler.make_hyp3_processing_function_from?
	        ?: where is worker actually created and given it's handler function?
