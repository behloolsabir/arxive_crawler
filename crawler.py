#! /usr/bin/env python
import urllib
import time
import feedparser
import re
from time import gmtime, strftime


# Base api query url
base_url = 'http://export.arxiv.org/api/query?';

# Search parameters
search_query = 'cat:physics.class-ph'	# search for electron in all fields
start = 0				# start at the first result
total_results = 3700			# want 20 total results
results_per_iteration = 1000		# 5 results at a time
wait_time = 3				# number of seconds to wait beetween calls
#total_results = results_per_iteration 

print 'Searching arXiv for %s' % search_query

##################################################
#pattern to determine all the authors as feedparse gives only the first author 
regex = '<name>(.+?)</name>'
author_pattern = re.compile(regex)


##################################################
#pattern to determine max no. of results for the query
regex_max_result = '<opensearch:totalResults xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">(.+?)</opensearch:totalResults>'
max_result_pattern = re.compile(regex_max_result)
##################################################
	

fo = open('parsed_text.dat','w+')
go = open('raw_html_text.dat','w+')

fo.write ("Crawling Start time:" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n')
go.write ("Crawling Start time:" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n')

search_count=0
article_count=start

for i in range(start,start+total_results,results_per_iteration):
    
    print "Results %i - %i" % (i,i+results_per_iteration)

    query = 'search_query=%s&start=%i&max_results=%i&sortBy=lastUpdatedDate&sortOrder=ascending' % (search_query, i, results_per_iteration)

    # perform a GET request using the base_url and query
    response = urllib.urlopen(base_url+query).read()
    go.write ("\n\nSearch count: " + str(search_count) + "\n")
    go.write ('\nquery: ' + base_url + query + "\n\n")
    go.write (response)

    search_count += 1

    # parse the response using feedparser
    feed = feedparser.parse(response)

    
    if i==start:
	max_result_calculated = re.findall(max_result_pattern, response) 
	print "Maximum nos. of result for the given query is:", max_result_calculated[0]
	#total_results = max_result_calculated[0]	#for all possible results of the query
	total_results = 3				#test total results 

    # Run through each entry, and print out information
    for entry in feed.entries:
        #article_id = 'arxiv-id: %s\n' % entry.id.split('/abs/')[-1]	#just gives the ID and not the complete link
	
        article_id = 'arxiv-id: %s\n' % entry.id	#this will give the entire link with the ID
        article_updated = 'Updated on: %s\n' % entry.updated
        article_published = 'Published on: %s\n' % entry.published
        article_title = 'Title: %s\n' % entry.title
	article_summary = 'Abstract: %s\n' % entry.summary
##################################################
	#to print all the authors
	try: 
	    article_authors = 'Authors: %s\n' % ', '.join(author.name for author in entry.authors)
	except AttributeError:
	    pass
##################################################
	#article_authors = re.findall(author_pattern, response)		#printing all the authors using reg expressions. Bug:This prints all the authors for each query together

        # feedparser v4.1 only grabs the first author
        #print 'First Author:  %s' % entry.author
        #print 'Author:  %s' % entry.author.name
	#print authors

	fo.write ('\n\n\nArticle no.: ' + str(article_count) + '\n')
	fo.write (article_id.encode('utf-8'))
	fo.write (article_updated.encode('utf-8'))
	fo.write (article_published.encode('utf-8'))
	fo.write (article_title.encode('utf-8'))
	fo.write (article_summary.encode('utf-8'))
	fo.write (article_authors.encode('utf-8'))

	#fo.write ('Author: '+', '.join(article_authors) + '\n')	#uncomment this planning to print all the authors using reg expression
	
	#fo.write (article_title)
	article_count += 1
    
    # Remember to play nice and sleep a bit before you call
    # the api again!
    print 'Sleeping for %i seconds' % wait_time 
    time.sleep(wait_time)

fo.write ("\n\nCrawling End time:" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n')
go.write ("\n\nCrawling End time:" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n')

fo.close()
go.close()
