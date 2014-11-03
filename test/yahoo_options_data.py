import json
import sys
import re
import urllib 

from bs4 import BeautifulSoup

def functionNotUsed(input):
	print "a"
	print "a"
	print "a"
	print "a"
	print "a"
	print "a"
	print "a"
	print "a"
	print "a"
	print "a"
	print "a"
	print "a"
	print "a"
	print "a"
	print "a"
	pass

def contractAsJson(filename):

	jsonQuoteData = {
		"currPrice" : 0.0,
		"dateUrls" : [],
		"optionQuotes" : []
	}

	bs = BeautifulSoup(open(filename).read())
	currNum = bs.find_all('span', class_ = 'time_rtq_ticker')[0].contents[0].contents[0]
	jsonQuoteData['currPrice'] = float(currNum)

	company = bs.find_all('div', class_ = 'title')[0].contents[0].contents[0]
	company = company.split('(',)[1].split(')',)[0]
	print company
	compstr = '\/q\/o[ps]\?s\='
	compstr = compstr + str(company)
	compstr = compstr + '\&m\=\d{4}\-\d{2}'
	reg = re.compile(compstr)
	tagList = bs.find_all('a', href = reg)
	for tag in tagList:
		jsonQuoteData['dateUrls'].append('http://finance.yahoo.com' + str(tag['href']).replace('&', '&amp;'))

	compstr = 'yfnc_((tabledata1)|(h))'
	reg = re.compile(compstr)
	loop = 0
	newDict = dict()
	searchList = bs.find_all('td', class_ = reg)
	for tag in searchList:
		if tag is searchList[-1]:
			break
		if loop == 0:
			newDict['Strike'] = tag.a.strong.contents[0]
		elif loop == 1:
			entry = tag.a.contents[0]
			newDict['Symbol'] = entry[:-15]
			newDict['Date'] = entry[-15:-9]
			newDict['Type'] = entry[-9:-8]
		elif loop == 2:
			target = tag.contents[0]
			if target == 'N/A':
				newDict['Last'] = target
			else:
				target = tag.b.contents[0]
				newDict['Last'] = target
		elif loop == 3:
			target = tag.span.b.contents[0]
			newDict['Change'] = tag.text
		elif loop == 4:
				target = tag.contents[0]
				newDict['Bid'] = target
		elif loop == 5:
				target = tag.contents[0]
				newDict['Ask'] = target
		elif loop == 6:
				target = tag.contents[0]
				newDict['Vol'] = target
		elif loop == 7:
				target = tag.contents[0]
				newDict['Open'] = target

		loop = loop + 1
		if loop == 8:
			loop = 0
			jsonQuoteData['optionQuotes'].append(newDict)
			print newDict
			newDict = dict()

	jsonQuoteData['optionQuotes'].sort(key=lambda x : -int(str(x['Open']).translate(None, ',')))
	jsonQuoteData = json.dumps(jsonQuoteData)

	return jsonQuoteData
