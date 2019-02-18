import os
import time
import getopt
import shutil
from ParsePage import *
from GetPage import *

if __name__ == "__main__":

	# Initialize variables
	url = ''
	outputFile = ''
	pagesDir = 'Pages'
	
	carCnt = 0
	yearErr = 0
	benzinErr = 0
	ccErr = 0
	perfErr = 0
	priceErr = 0	
	sumErr = 0

	# Get arguments
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hu:o:",["url=","ofile="])
	except getopt.GetoptError:
		print 'main.py -u <url> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'main.py -u <url> -o <outputfile>'
			sys.exit()
		elif opt in ("-u", "--url"):
			url = arg
		elif opt in ("-o", "--ofile"):
			outputFile = arg
			pagesDir = arg.replace(".", "_")
	
	# Clear html source path
	if os.path.isdir(pagesDir):
		shutil.rmtree(pagesDir)		
	os.makedirs(pagesDir)
	
	# Get number of pages and read the first page
	getPage(url, pagesDir)
	lastPageNumber = int(getLastPage(pagesDir + "/page1.html"))
	sys.stdout.write("\rPage 1 / " + str(lastPageNumber) + " read.")	
	
	# Read the reamining pages
	url = url[0:len(url) - 1]
	for num in range(2, lastPageNumber + 1):
		time.sleep(3)
		timeoutCnt = 0
		while timeoutCnt < 10:
			try:
				getPage(url + str(num), pagesDir)	
				sys.stdout.write("\rPage " + str(num) + " / " + str(lastPageNumber) + " read.")
				break
			except:
				timeoutCnt += 1
				print "\nRead error. Attempt number: " + str(timeoutCnt)
				time.sleep(10)
		if timeoutCnt == 10:
			print "Reading error"
			sys.exit()
	
	# Parse html source pages
	if outputFile != '':
	
		# Create output file
		f = open(outputFile, 'w')
		f.write(u'Marka\tTipus\tEv\tHonap\tUzemanyag\tcc\tTeljesitmeny\tAr\n')
		f.close()
		
		for file in os.listdir(pagesDir):
			carCntTmp, yearErrTmp, benzinErrTmp, ccErrTmp, perfErrTmp, priceErrTmp = parsePage(pagesDir + "/" + file, outputFile)
			sumErrTmp = yearErrTmp + benzinErrTmp + ccErrTmp + perfErrTmp + priceErrTmp
			carCnt += carCntTmp
			yearErr += yearErrTmp
			benzinErr += benzinErrTmp
			ccErr += ccErrTmp
			perfErr += perfErrTmp
			priceErr += priceErrTmp
			sumErr = yearErr + benzinErr + ccErr + perfErr + priceErr
			sys.stdout.write("\r" + file + " parsed. Cars: " + str(carCntTmp) + ", errors: " + str(sumErrTmp) + " year: " + str(yearErrTmp) + " benzin: " + str(benzinErrTmp) + " cc: " + str(ccErrTmp) + " perf: " + str(perfErrTmp) + " price: " + str(priceErrTmp))
			if sumErrTmp > 0:
				sys.stdout.write("\n")		
	
	sys.stdout.write("\nDone!\nCars: " + str(carCnt) + ", errors: " + str(sumErr) + " year: " + str(yearErr) + " benzin: " + str(benzinErr) + " cc: " + str(ccErr) + " perf: " + str(perfErr) + " price: " + str(priceErr))