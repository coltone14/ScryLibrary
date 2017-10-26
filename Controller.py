
import DBManager as DBM
import Scrape
import time as t
from datetime import *

min_interval = 5

def collect():
	print('collecting @ ', datetime.now())	# current time
	start = t.time()

	articles_list = Scrape.get_articles()	# scraping data
	DBM.populate_db(articles_list)			# saving to database

	print(t.time() - start)		# timing the execution
	print('Next collection @ ~', datetime.now() + timedelta(minutes = min_interval))	# approx. next collection time


while 1:
	collect()
	t.sleep(min_interval * 60)





		

 