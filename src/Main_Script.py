from subprocess import call
call(["brew","services","start","tor"])
import socks
import socket
socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
socket.socket 								= socks.socksocket

import requests
import urllib.request
from bs4 import BeautifulSoup
import json
import re
import os
import time
from time import sleep
from random import choice

# Libraries required to limit the time taken by a request
import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass


@contextmanager
def time_limit(seconds):
	def signal_handler(signum, frame):
		raise TimeoutException
	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(seconds)
	try:
		yield
	finally:
		signal.alarm(0)

baseurl 									= "https://scholar.google.com"
request_count 								= 0
global_request_count						= 0
DOS_flag									= 0
continous_block_number						= 0

# Checking existenc of the required directory 
def ckdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return


def get_new_soup(aurl):
	global request_count
	global global_request_count
	global DOS_flag

	if DOS_flag == 1:
		continous_block_number				+= 1
		if continous_block_number%40 and continous_block_number>1:
			print('The last 40 ips have face DOS with the first request.')
			print('Sleeping for 5 mins. Sleep time : '+str(time.asctime(time.localtime(time.time()))))
			sleep(300)
			continous_block_number 			= 0
	else:
		continous_block_number 				= 0

	if DOS_flag == 1 :
		call(["brew","services","stop","tor"])
		call(["brew","services","start","tor"])
		sleep(5)
		while True:
			try:
				# Waiting 60 seconds to recieve a responser object
				with time_limit(60):
					print(requests.get("http://icanhazip.com").text)
				break
			except Exception:
				print("Error requesting for ip address.")
				continue
		DOS_flag 							= 0

	request_count 							+= 1
	global_request_count 					+= 1
	print('Sending a request. Count : '+str(request_count))
	print('Global successful request count : '+str(global_request_count))

	user_agents 							= ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36','Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11','Opera/9.25 (Windows NT 5.1; U; en)','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)','Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1']
	user_agent 								= choice(user_agents)
	hdr 									= {'User-Agent':user_agent}

	while  True:
		try:
			try:
				with time_limit(300):
					content 				= requests.get(aurl,headers=hdr).content
				break
			except TimeoutException:
				print('Request times out. Trying again...')
				continue
		except Exception as err:
			print('Error in request. Error :')
			print(err.message)
			continue

	soup 									= BeautifulSoup(content,'html.parser')
	return soup


# Function to return a BeautifulSoup object of the requested page url
def get_soup(aurl):
	return get_new_soup(aurl)
	global request_count
	global global_request_count

	request_count							+= 1

	if request_count > 10 :
		global_request_count 				+= request_count
		request_count 						= 0
		print('Reached session request limit.')
		print('Global Request count : '+str(global_request_count))
		print('Sleeping for 15 mins. Sleep time : '+str(time.asctime(time.localtime(time.time()))))
		sleep(600)

	print('Sending a request. Count : '+str(request_count))
	sleep(2)
	user_agents 							= ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36','Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11','Opera/9.25 (Windows NT 5.1; U; en)','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)','Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1']
	user_agent 								= choice(user_agents)
	hdr 									= {'User-Agent':user_agent}
	req 									= urllib.request.Request(aurl,headers=hdr)
	html									= urllib.request.urlopen(req)
	asoup 									= BeautifulSoup(html.read(),'html.parser')
	return asoup


"""
	Function which accepts the name of the scholar and attempts to return the profile link
"""
def get_user_link(aname):
	global DOS_flag

	searchName 								= re.sub(' ','+',aname)
	# search_link = baseurl + 'scholar?q=author:"'+searchName+'"&btnG=&hl=en&as_sdt=0%2C5'
	author_search_link						= baseurl + '/citations?view_op=search_authors&mauthors=author:"'+searchName+'"&hl=en&oi=ao'
	while True:
		try:
			soup 							= get_soup(author_search_link)
			content							=  soup.find('div',{'id':'gs_ccl'})
			try:
				author 						= content.find_all('div',{'class':'gsc_1usr gs_scl'})[0]

			except IndexError:
				return None
			break
		except AttributeError:
			print('Requesting for user link again.')
			DOS_flag 						= 1
	author_page_link 						= baseurl + author.find('h3',{'class':'gsc_1usr_name'}).find('a')['href']
	return author_page_link



"""
	Function to get paper titles and partial list of authors in a citation
"""
def get_citation_data(aurl):
	print('Getting citation details for the paper')

	global DOS_flag

	nexturl									= aurl
	Citation_list							= []
	flag 									= 0

	global global_request_count

	while flag==0 :
		while True:
			try:
				soup 						= get_soup(nexturl)
				results_body				= soup.find('div',{'id':'gs_bdy'}).find('div',{'id':'gs_res_bdy'})
				results 					= results_body.find('div',{'id':'gs_ccl'})
			except AttributeError:
				global_request_count		-= 1
				DOS_flag 					= 1
				print('Requesting again')
				continue
			break

		articles 							= results.find_all('div',{'class':'gs_r'})

		# Iterating over all articles citing the original paper
		for article in articles:
			article_dict					= {}
			details 						= article.find('div',{'class':'gs_ri'})

			headers							= details.find('h3',{'class':'gs_rt'})
			try:
				article_dict['Title']		= str(headers.find('a').get_text())
				article_dict['Paper_link']	= headers.find('a')['href']
			except AttributeError:
				article_dict['Paper_link']	= None
				article_dict['Title']		= headers.get_text()

			authors 						= details.find('div',{'class':'gs_a'}).get_text().split('-')[0]
			authors 						= re.sub('[^A-Za-z, ]','',authors)
			authors 						= re.sub(', ',',',authors)
			article_dict['authors']			= authors.split(',')

			footer_details 					= details.find('div',{'class':'gs_fl'}).find_all('a')

			article_dict['Citations_Link']	= baseurl+footer_details[0]['href']

			Citation_list.append(article_dict)

		try:
			nav_menu						= soup.find('div',{'id':'gs_n'})
			checkMore						= nav_menu.find('tr').find_all('td')[-1]
			if checkMore.get_text() == "Next":
				nexturl						= baseurl+checkMore.find('a')['href']
		except Exception:
			flag 							= 1

	return Citation_list



"""
	Function to get the links of all papers written by the user
"""
def get_user_paper_links(aurl):
	print('Getting details of the papers written by the author.')

	global paper_dir
	global DOS_flag

	pageSize 								= 100
	startIndex 								= 163
	flag 									= 0
	paper_count								= 163
	page_count								= 0

	# Looping over every 100 titles till no more articles are available
	while flag == 0 :
		page_count							+= 1
		print('Accessing page : '+str(page_count))

		temp_url 							= aurl + '&cstart=' + str(startIndex) + '&pagesize=' + str(pageSize)

		while True:
			try:
				soup 						= get_soup(temp_url)

				# Finding the rows containing article data
				papers 						= soup.find('tbody',{'id':'gsc_a_b'}).find_all('tr')

				break
			except AttributeError:
				print('Requesting for the paper links page again.')
				DOS_flag 					= 1

		# Iterating through each link
		for paper in papers[::]:
			paper_count 					+= 1
			print('Accessing Paper : '+str(paper_count))

			article_dict 					= {}

			header_info 					= paper.find('td',{'class':'gsc_a_t'})

			title_details 					= header_info.find('a')
			article_dict['title'] 			= title_details.get_text()
			article_dict['paper_link'] 		= baseurl+title_details['href']

			more_details 					= header_info.find_all('div',{'class':'gs_gray'})

			author_details 					= more_details[0].get_text()
			article_dict['authors'] 		= author_details.split(', ')

			publication_details 			= more_details[1].get_text()
			article_dict['publication'] 	= publication_details

			# Finding the link to citations
			citations_data 					= paper.find('td',{'class':'gsc_a_c'}).find('a')
			if citations_data['href']=='':
				# print('No citations')
				article_dict['citations'] 	= None
			else:
				# print('Citations exist.')
				Citation_Link 				= citations_data['href'] + '&num=20'
				Citation_list 				= get_citation_data(Citation_Link)
				article_dict['citations'] 	= Citation_list

			year 							= paper.find('td',{'class':'gsc_a_y'}).find('span').get_text()

			file_name						= paper_dir+'/paper '+str(paper_count)+'.json'
			with open(file_name,'w') as outfile:
				json.dump(article_dict,outfile)

		# Checking if more articles for the author exist
		checkMore 							= soup.find('button',{'id':'gsc_bpf_more'})
		try:
			checkMore['disabled']
			flag 							= 1 
		except KeyError:
			startIndex 						+= 100


"""
	Start of the program
"""
base_dir 									= '../output/Author Data'
ckdir(base_dir)
userNames 									= ['snehanshu saha','cnr rao']
for userName in userNames[1::]:
	# print('Searching for author : ',userName)
	link = get_user_link(userName)
	if not link:
		print('No author "'+userName +'" found!')
	else:
		author_dir 							= base_dir+'/'+userName
		ckdir(author_dir)

		paper_dir 							= author_dir+'/Papers'
		ckdir(paper_dir)

		paper_links 						= get_user_paper_links(link)