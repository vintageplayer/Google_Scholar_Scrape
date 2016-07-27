#from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import json
import re

baseurl = "https://scholar.google.com/"

# Function to return a BeautifulSoup object of the requested page url
def get_soup(aurl):
	hdr = {'User-Agent':'Mozilla/5.0'}
	req = urllib.request.Request(aurl,headers=hdr)
	html = urllib.request.urlopen(req)
	asoup = BeautifulSoup(html.read(),'html.parser')
	return asoup


def get_user_profile(aname):
	searchName = re.sub(' ','+',aname)
	# search_link = baseurl + 'scholar?q=author:"'+searchName+'"&btnG=&hl=en&as_sdt=0%2C5'
	author_search_link = baseurl + 'citations?view_op=search_authors&mauthors=author:"'+searchName+'"&hl=en&oi=ao'
	soup = get_soup(author_search_link)
	content =  soup.find('div',{'id':'gs_ccl'})
	authors = content.find_all('div',{'class':'gsc_1usr gs_scl'})
	for author in authors:
		print(author.find('h3',{'class':'gsc_1usr_name'}).find('a')['href'])


userName = 'cnr rao'
get_user_profile(userName)
# url = "https://scholar.google.co.in/citations?user=Zs9227oAAAAJ&hl=en"
# soup = get_soup(url)
# print(soup.prettify())