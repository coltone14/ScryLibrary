
import DBManager as DBM
import Scrape
import time





start = time.time()
articles_list = Scrape.get_articles()
print(time.time() - start)
DBM.populate_db(articles_list)


		

 