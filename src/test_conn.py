from subprocess import call
call(["brew","services","start","tor"])
import socks
import socket
socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
socket.socket = socks.socksocket

import requests
from bs4 import BeautifulSoup
from time import sleep


def get_new_soup(aurl):
	global request_count
	global global_request_count

	request_count += 1

	if request_count > 5 :
		call(["brew","services","stop","tor"])
		call(["brew","services","start","tor"])
		sleep(10)
		global_request_count += 5
		request_count = 0

	content = requests.get(aurl).content
	soup = BeautifulSoup(content,'html.parser')

	return soup

request_count = 0
global_request_count = 9
# url = 'http://icanhazip.com'
url = 'https://scholar.google.co.in/scholar?oi=bibs&hl=en&cites=13887102137911521444'
while True:
	print(get_new_soup(url))