import requests
import bs4
import csv
import threading
import RandomHeaders
COUNT = 0
lock = threading.Lock()
def chunks(l, n):
	for i in xrange(0, len(l), n):
		yield l[i:i + n]
formerPizzaHuts = []

THREADS = 10
with open('locations.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

ADDRESS_LIST = []
i = 0
for valueList in your_list:
	try:
		ADDRESS_LIST.append(valueList[-1].split("(")[0].strip()[:-1])
		i += 1
	except Exception as exp:
		print exp

addressList = chunks(ADDRESS_LIST, int(len(ADDRESS_LIST)/THREADS))



def grabSite(url):
	for i in range(3):
		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
			return requests.get(url, headers=RandomHeaders.LoadHeader(), timeout=10)
		except Exception as exp:
			print exp
			pass

def increment():
	global COUNT
	COUNT = COUNT+1
	print("{} / {}".format(COUNT, i))

def FormerPizzaHut(page):
	valueBool = True
	# Returns true if it's a former pizza hut
	try:
		if "address" in page.select("h4")[0].getText().lower():
			for val in page.select("h5"):
				print val.getText().lower()
				if "pizza hut" in val.getText().lower():
					return False
			return valueBool
		else:
			return "idk"
	except Exception as exp:
		print exp
		return "idk"

def processLocations(listOfLocations):
	for address in listOfLocations:
		lock.acquire
		increment()
		lock.release
		try:
			addressVal = address
			address = address.replace(',', "%2C").replace(" ", "+")
			url = "https://www.google.com/search?q=" + address
			res = grabSite(url)
			page = bs4.BeautifulSoup(res.text, 'lxml')
			if FormerPizzaHut(page) == True:
				formerPizzaHuts.append(addressVal)
				print("{} Former Pizza Huts Found".format(len(formerPizzaHuts)))
		except Exception as exp:
			print exp





if __name__ == '__main__':
	threads = [threading.Thread(target=processLocations, args=(ar,)) for ar in addressList]

	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()



