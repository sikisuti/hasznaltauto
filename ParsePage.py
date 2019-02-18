#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys  
import os
import getopt
from lxml import html

from WriteFile import *

def parsePage(fileName, destination):
	carCnt = 0
	yearErr = 0
	benzinErr = 0
	ccErr = 0
	perfErr = 0
	priceErr = 0
	
	f = html.parse(fileName)
	root = f.getroot()

	listContainer = root.xpath("//div[starts-with(@class, 'feherbox')]")[0]
	carList = listContainer.xpath("div[starts-with(@class, 'talalati_lista ')]|//div[@class = 'talalati_lista']")
#	print len(carList)
	content = ""
	line = ""
	for car in carList:
		carCnt += 1
		line = ""
		
		carHead = car.xpath(".//div[@class='talalati_lista_head']")[0]
		carLink = carHead.xpath(".//a//@href")[0]
		linkParts = carLink.split('/')
		line += linkParts[4] + "\t"
		if len(linkParts) >= 5:
			line += linkParts[5] 
		line += "\t"
			
		carInfo = car.xpath(".//div[@class='talalati_lista_infosor']")[0]
		infoParts = carInfo.xpath("text()")[1].split(u'\u00a0\u00a0\u00b7\u00a0\u00a0')
	#	print len(infoParts)
	# Year, month
		try:
			yearData = infoParts[1].split('/')
			line += yearData[0] + '\t'
		except:
			yearErr += 1
			errLog = "error year, month\n"
			errLog += fileName + " " + linkParts[4] + " " + linkParts[5] + "\n"
			errLog += html.tostring(carInfo) + "\n\n"
			writeFile("err.log", errLog)
			continue
		if len(yearData) > 1:
			line += yearData[1] + '\t'
		else:
			line += '\t'
		
	# Benzin, diesel
		try:
			if infoParts[2] == 'Benzin' or infoParts[2] == u'Dízel':
				line += infoParts[2] + '\t'
			else:
				benzinErr += 1
				continue
		except:
			benzinErr += 1
			errLog = "error Benzin, Diesel\n"
			errLog += fileName + " " + linkParts[4] + " " + linkParts[5] + "\n"
			errLog += html.tostring(carInfo) + "\n\n"
			writeFile("err.log", errLog)
			continue
		
	# cc	
		if len(infoParts) == 6:
			try:
				ccWhole = infoParts[3].split(" ")
				cc = int(ccWhole[0])
				cc = int("%.0f" % (cc / 200.0)) * 200
				line += str(cc) + '\t'
			except:
				ccErr += 1
				print "error cc"
				print html.tostring(carInfo)
				print sys.exc_info()[0]
		else:
			line += '\t'
			
	# performance		
		if len(infoParts) == 6:
			try:
				line += infoParts[len(infoParts) - 2] + '\t'
			except:
				perfErr += 1
				print "error performance"
				print html.tostring(carInfo)
				print sys.exc_info()[0]
		else:
			line += '\t'
			
	# price
		try:
			arsor = car.xpath(".//div[@class='arsor']")[0]
			akcio = arsor.xpath(".//span[@class='akcioshirdetes']")
			if len(akcio) > 0:
				price = akcio[0].xpath(".//text()")[0]
			else:
				price = arsor.xpath(".//text()")[0]
				
			ar = int(price.split(u'\xa0')[0].replace('.', ''))
			
			#if __name__ == "__main__":
				#print str(carCnt + 1) + " " + price.encode("UTF-8", 'ignore')
			line += str(ar)
		except:
			priceErr += 1
			errLog = "error price\n"
			errLog += fileName + " " + linkParts[4] + " " + linkParts[5] + "\n"
			errLog += html.tostring(arsor) + "\n\n"
			writeFile("err.log", errLog)
			continue
			
		'''
		try:
			print line.encode("UTF-8", 'ignore')
		except:
			errCnt += 1
			print "Line print error"
			print html.tostring(carInfo)
			'''
		line += '\n'
		content += line.encode("UTF-8", 'ignore')

	writeFile(destination, content)
		
	return carCnt, yearErr, benzinErr, ccErr, perfErr, priceErr
	
def getLastPage(fileName):
	f = html.parse(fileName)
	root = f.getroot()

	return root.xpath("//a[starts-with(@title, 'Utols')]//text()")[0]
	
if __name__ == "__main__":
	carCnt = 0
	yearErr = 0
	benzinErr = 0
	ccErr = 0
	perfErr = 0
	priceErr = 0	
	sumErr = 0

	pageNumber = ''
	outputFile = ''
	pagesDir = 'Pages'

	# Get arguments
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hp:o:",["page=","ofile="])
	except getopt.GetoptError:
		print 'main.py -p <pageNumber> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'main.py -p <pageNumber> -o <outputfile>'
			sys.exit()
		elif opt in ("-p", "--page"):
			pageNumber = arg
		elif opt in ("-o", "--ofile"):
			outputFile = arg
			pagesDir = arg.replace(".", "_")
			
	f = open(outputFile, 'w')
	f.write(u'Marka\tTipus\tEv\tHonap\tUzemanyag\tcc\tTeljesitmeny\tAr\n')
	f.close()
	f = open("err.log", 'w')
	f.close()
	
	if pageNumber == '':
		for file in os.listdir(pagesDir):
			carCntTmp, yearErrTmp, benzinErrTmp, ccErrTmp, perfErrTmp, priceErrTmp = parsePage(pagesDir + '/' + file, outputFile)
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
			
	else:
		carCnt, yearErr, benzinErr, ccErr, perfErr, priceErr = parsePage(pagesDir + '/page' + pageNumber + '.html', outputFile)
		sys.stdout.write("Cars: " + str(carCnt) + ", errors: " + str(sumErr) + " year: " + str(yearErr) + " benzin: " + str(benzinErr) + " cc: " + str(ccErr) + " perf: " + str(perfErr) + " price: " + str(priceErr))