import pymysql



def populate_db(articles_list):
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
		content_type = article.content_type
		premium = article.premium
	
		col_list = (title, author, _date, link, source, source_url, game, content_type, premium)	#correspond with database
		try:
			with connection.cursor() as cursor:
        		# Create a new record
				query = "INSERT INTO article values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % col_list 
				cursor.execute(query + " ON DUPLICATE KEY UPDATE title = '%s', author = '%s', date = '%s', link = '%s', source = '%s', source_url = '%s', game = '%s', content_type = '%s', premium = '%s'" % col_list)
    			# connection is not autocommit by default. must commit to save changes
			connection.commit()
		except:
			print("Error Inserting %s" % title)	
	
	connection.close()