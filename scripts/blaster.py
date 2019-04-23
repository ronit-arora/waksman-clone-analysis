from lxml import html
import requests
import re
import zipfile
import io
import json
import datawait

# My personal (Ronit Arora) api key - this may change over time if I replaced it, which could affect the script.
api_key = '5319163d6a6ab2543a166a4b93e5116c1f08'

# Global variables
base_url = 'https://blast.ncbi.nlm.nih.gov/Blast.cgi?'



def blaster(query, program, db):
	"""Retrieves data from a BLAST search of a certain query

	Parameters
	----------

	query
		the input sequence

	program
		which type of BLAST program is being used (e.x. blastn, blastx, blastp)


	Returns
	-------

	datadict
		dictionary (JSON) data of BLAST search
	"""
	# The URL to get initial RID from (but returns HTML content)
	PARAMS = {'CMD':'Put', 'PROGRAM':program, 'DATABASE':db, 'QUERY': query, 'API_KEY':api_key}
	# url = base_url + "CMD=Put&" + "PROGRAM=blastn&" "DATABASE=nr&" + "FORMAT_TYPE=JSON&" "QUERY=" + test_query

	# intro references an HTML object
	intro = requests.get(base_url, PARAMS)
	print(intro)
	# scrape through to find rid & wait time in the html object content
	rid, wait_time = query_info(intro)

	# Initial Information
	print("RID: " + rid)
	print("Wait Time: " + wait_time)

	datawait.rest(int(wait_time) + 10)

	# Check to make data is ready - if not, wait in intervals of 30 seconds
	checkstatus = isready(rid)
	print("STATUS: " + str(isready(rid)))

	while(not checkstatus):
		datawait.rest(60)
		checkstatus = isready(rid)
		print("STATUS: " + str(isready(rid)))

	# Rather than just a JSON file, NCBI sends a zip file containg the json file.
	# This involves retrieving the file
	output = requests.get(base_url, {'CMD': 'Get', 'RID': rid, 'API_KEY' : api_key, 'FORMAT_TYPE': 'JSON2'})
	print(output)
	print(output.url)
	z = zipfile.ZipFile(io.BytesIO(output.content))

	# Converting to json from bytes stream
	datadict = {}
	with z.open(rid + '_1.json') as myfile:
		datadict = json.loads(myfile.read())

	return datadict



def query_info(doc):
	"""Gets initial Request ID and wait time.

	Parameters
	----------

	docs : HTTP object
		The object that contains the HTML content of the initial NCBI webpage


	Returns
	-------

	rid
		The Request ID to retrieve search results on NCBI
	wait_time
		How much (estimated) time to wait before NCBI will provide data
	"""

	# Convert to HTML for easier scraping
	tree = html.fromstring(doc.content)

	# The path to the comment containing the rid and wait time - is a one-element-list
	# Note xpath found directly from NCBI site source code
	comment = tree.xpath('//*[@id="FormatForm"]/comment()[4]')

	# Get the comment in string form
	mystring = str(comment[0])

	# Locating the indices of the strings 'RID' and 'RTOE', and then returning the indices following them (actual values)
	values = re.split('\W+', mystring)
	index_id = values.index('RID')
	index_time = values.index('RTOE')
	return values[index_id + 1], values[index_time + 1]

def isready(rid):
	"""Checks if data is ready to be sent

	Parameters
	----------
	rid
		The Request ID to retrieve search results on NCBI


	Returns
	-------
	status
		If ready, returns true. Otherwise, False

	"""

	# Params for url
	PARAMS = {'CMD':'Get', 'RID':rid, 'API_KEY':api_key}

	# XPath for comment indicating status
	xpath_var = '//*[@id="qb"]/comment()'
	try:
		nana = requests.get(base_url, PARAMS)
		print(nana)
		tree = html.fromstring(nana.content)
	except:
		return False

	status_comment = tree.xpath(xpath_var)
	print(status_comment)

	# If it doesn't exist then it's automatically false
	if len(status_comment) == 0:
		return False

	# Getting string value of comment
	mystring = str(status_comment[0])

	# Status is likely always Ready if it exists, but this is a second check to make sure
	# Break down comment to extract and return status
	values = re.split('\W+', mystring)
	index_status = values.index('Status')
	if(values[index_status + 1] == 'READY'):
		return True
	return False
