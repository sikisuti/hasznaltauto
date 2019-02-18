def writeFile(fileName, content):
	f = open(fileName, 'a')
	f.write(content)
	f.close