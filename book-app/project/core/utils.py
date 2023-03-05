# Webscraper using 'multithreading'

from bs4 import BeautifulSoup
import requests

# specifying user agent, You can use other user agents
# available on the internet
HEADERS = {
	'User-Agent' : ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
					'AppleWebKit/537.36 (KHTML, like Gecko)'
					'Chrome/108.0.0.0 Safari/537.36'),
	'Accept-Language': 'en-US, en;q=0.5'
}


def wb_author(url):
	# Making the HTTP request
	webpage = requests.get(url, headers=HEADERS)

	# Creating the soup object containing web data
	soup = BeautifulSoup(webpage.content, 'lxml')

	# Retrieving author
	try: 
		# Outer tag object
		author = soup.find("span", {"class": "author notFaded"})
		# Inner navigable string object
		author_value = author.a.string
		# 

	except AttributeError:

		author_value = ""

	return author_value


def wb_pg_num(url):
	# Making the HTTP request
	webpage = requests.get(url, headers=HEADERS)

	# Creating the soup object containing web data
	soup = BeautifulSoup(webpage.content, 'lxml')

	# Retreiving page number
	try:
		# Outer tag object
		pages = soup.find("div", {"class": "a-section a-spacing-none a-text-center rpi-attribute-value"})
		# Inner navigable string object
		pages_value = pages.span.a.span.string
		# changes / # pages / to / #
		num = ""
		for c in pages_value:
			if c.isdigit():
				num = num + c

	except AttributeError:
		num = 0

	return int(num)