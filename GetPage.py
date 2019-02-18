import urllib2
from WriteFile import *
import os

def getPage(url, pagesDir):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'), ('Cookie', 'talalatokszama=100')]
	response = opener.open(url)
	
	html = response.read()
	response.close()
	urlParts = url.split('/')
	writeFile(pagesDir + "/" + urlParts[len(urlParts)-1] + ".html", html)
	
if __name__ == "__main__":
	if os.path.isfile('YearSource/page1.html'):
		os.remove('YearSource/page1.html')
		
	getPage('http://www.hasznaltauto.hu/talalatilista/auto/T4R3HR2ADAJ5QRLADR8ISKLR89DZZJQA2MC42I7A89D5MO8K6S1MG25AGUG625FA8RG40ZQOA84OR6A1Q589A2E9AEK3OYCAU98OHZAEF627C2OIS1L3ODM7UR29SY8ZIUY7LO967LLHIW5137G23SZY76FLE8AF09E07AU9I7MYO3R80LWYO/page1')