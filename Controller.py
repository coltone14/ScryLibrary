
import DBManager as DBM
import Scrape
import time as t
from datetime import *

min_interval = 5	# article data collected every "min_interval" minutes
days = 90	# articles older than this amount of days will be deleted

def collect():
	print('\nCollecting @ ', datetime.now())	# current time
	start = t.time()

	articles_list = Scrape.get_articles()	# scraping data
	DBM.populate_db(articles_list)			# saving to database
	DBM.prune_db(days)						# pruning articles

	print(str(t.time() - start), 'seconds')		# timing the execution
	print('Next collection @ ~', datetime.now() + timedelta(minutes = min_interval),'\n')	# approx. next collection time


while 1:
	try:
		collect()
		t.sleep(min_interval * 60)
	
	except KeyboardInterrupt:
		print('\n--Procedure Interrupted--')
		break




		

 