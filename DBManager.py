import pymysql



def populate_db(articles_list):	# insert/update articles
	try:	#connect to database
		connection = pymysql.connect(unix_socket='/var/run/mysqld/mysqld.sock',user='root',database='articles_test', charset='utf8')
		print("Database Connection Successful")
	except:
		print("Connection Error")
		return

	for article in articles_list:
		title = article.title.replace("'", "`")
		author = article.author.replace('  ',' ').replace("'", "`")	#some names have 2 spaces
		_date = article.date
		link = article.link
		source = article.source
		source_url = article.source_url
		game = article.game
		premium = article.premium
	
		col_list = (title, author, _date, link, source, source_url, game, premium)	#correspond with database
		try:
			with connection.cursor() as cursor:
        		# Create a new record
				query = "INSERT INTO article values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % col_list 
				cursor.execute(query + " ON DUPLICATE KEY UPDATE title = '%s', author = '%s', date = '%s', link = '%s', source = '%s', source_url = '%s', game = '%s', premium = '%s'" % col_list)
    			# connection is not autocommit by default. must commit to save changes
			connection.commit()
		except:
			print("Error Inserting %s" % title)	
	
	connection.close()


def prune_db(days):	# delete articles older than this amount of days

	try:	#connect to database
		connection = pymysql.connect(unix_socket='/var/run/mysqld/mysqld.sock',user='root',database='articles_test', charset='utf8')
	except:
		print("Connection Error")
		return

	try:
		with connection.cursor() as cursor:
        	# Create a new record
			query = "DELETE FROM article WHERE UNIX_TIMESTAMP(date) < UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL %s DAY))" % days
			cursor.execute(query)
    		# connection is not autocommit by default. must commit to save changes
			connection.commit()
		print('Deleted articles older than %s days' % days)
	
	except:
		print("Error Pruning Articles")

	finally:
		connection.close()