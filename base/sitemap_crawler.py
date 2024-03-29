import re
import urllib.request

from urllib.error import URLError, HTTPError, ContentTooShortError

def download(url, user_agent='wswp', num_retries=2, charset='utf-8'):
	print('Downloading:', url)
	request = urllib.request.Request(url)
	request.add_header('User-agent', user_agent)
	try:
		resp = urllib.request.urlopen(request)
		cs = resp.headers.get_content_charset()
		if not cs:
			cs = charset
		html = resp.read().decode(cs)
	except(URLError, HTTPError, ContentTooShortError) as e:
		print('Downloading error:', e.reason)
		html = None
		if num_retries > 0:
			if hasattr(e, 'code') and 500 <= e.code < 600:
				# recursively retry 5xx HTTP errors
				return Download(url, num_retries - 1)
	return html

def crawl_sitemap(url):
	# download the sitemap file
	sitemap = download(url)
	# extract the sitemap link
	links = re.findall('<loc>(.*?)</loc>', sitemap)
	#download each link
	for link in links:
		html = download(link)	

if __name__ == '__main__':
	crawl_sitemap('http://example.python-scraping.com/sitemap.xml')

