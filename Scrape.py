import urllib.request
import bs4 as bs
import requests
from dateutil.parser import *
from datetime import *
import threading


class Article:

	articles_list = []

	def __init__(self, title, author, date, link, source, source_url, game, content_type, premium):
		self.title = title
		self.author = author
		self.date = format_date(date)
		self.link = link
		self.source = source
		self.source_url = source_url
		self.game = game
		self.content_type = content_type
		self.premium = premium
		Article.articles_list.append(self)


################ Parsing and Formatting ###################
def make_soup(req, source_url):
	try:
		with urllib.request.urlopen(req) as source:
			code = source.read()
		if 'feed' in source_url or 'rss' in source_url:
			soup = bs.BeautifulSoup(code, 'html.parser')
			return soup
		else:	
			soup = bs.BeautifulSoup(code, 'lxml')
			return soup
	except:
		print("Error requesting " + source_url)
		return False


def format_date(_date):
	if _date.lower().strip() == 'today':			#set the date as the current date
		return date.today().isoformat()
	elif _date.strip() == '':
		return 'NULL'	
	else:
		return parse(_date).date()				#standardize dates for database
	#################################

	


				# MTG #
def get_wotc_articles():
	source = "http://magic.wizards.com/en/rss/rss.xml"
	source_url = 'http://magic.wizards.com/en/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return 

	for chunk in soup.find_all('item'):	
		try:
			title = chunk.find('title').text	# article title
			if 'ROUND' in title:
				continue
			author = chunk.find('dc:creator').text.replace('By','').strip()	#author
			date = chunk.find('pubdate').text		#date
			link = "http://magic.wizards.com" +chunk.find('link').text	# article link
			
			temp_article = Article(title, author, date, link, 'Wizards of the Coast', source_url, 'Magic: The Gathering', 'Article', 0)
		except:
			print ('Error Collecting WOTC Article')


def get_cfb_articles():	# videos
	source = "http://www.channelfireball.com/feed/"
	source_url = 'http://store.channelfireball.com/landing'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return 

	for chunk in soup.find_all('item'):	
		try:
			link = chunk.find('link').text		# article link
			title = chunk.find('title').text	# article title
			author = chunk.find('dc:creator').text.strip()	#author
			date = chunk.find('pubdate').text		#date

			if '/articles/' in link:
				content_type = 'Article'
			elif '/videos/'	in link:
				content_type = 'Video'
			
			temp_article = Article(title, author, date, link, 'Channel Fireball', source_url, 'Magic: The Gathering', content_type, 0)
		except:
			print ('Error Collecting CFB Article')



def get_scg_articles():	# videos
	source = "http://www.starcitygames.com/tags/Premium~Select/"
	source_url = 'http://www.starcitygames.com/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return 

	for chunk in soup.find_all('article', {'class':'articles all'}):	
		try:
			title = chunk.a.text	# article title
			author = chunk.find('p', {'class':'premium_author'}).text.strip()	# author
			date = chunk.find('p', {'class':'tag_article_date'}).text	# article date
			link = chunk.a.get('href')	# article link

			if '#Premium' in chunk.find('aside').text:
				premium = 1
			else:
				premium = 0

			if '#Video' in chunk.find('aside').text:
				content_type = 'Video'
			elif '#Podcast' in chunk.find('aside').text:
				content_type = 'Podcast'
			else:
				content_type = 'Article'	

			temp_article = Article(title, author, date, link, 'StarCityGames', source_url, 'Magic: The Gathering', content_type, premium)	
		except:
			print ('Error Collecting SCG Article')


def get_tcg_articles():	
	source = "http://magic.tcgplayer.com/rss/rssfeed.xml"
	source_url = 'http://magic.tcgplayer.com/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return

	for chunk in soup.find_all('item'):	
		
		try:
			titleauth = chunk.find('title').text.split(', by')
			title = titleauth[0]	# article title
			author = chunk.find('dc:creator').text.replace('By','').strip()	#author
			date = chunk.find('pubdate').text		#date
			link = chunk.find('link').text	# article link
			
			temp_article = Article(title, author, date, link, 'TCGPlayer', source_url, 'Magic: The Gathering', 'Article',0)	
		except:
			print ('Error Collecting TCG Article')


def get_mtggf_articles():	# videos # podcasts
	source = "https://www.mtggoldfish.com/feed"
	source_url = 'https://www.mtggoldfish.com/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return 

	for chunk in soup.find_all('entry'):	
		try:
			title = chunk.find('title').text	# article title
			author = chunk.find('name').text.strip()	#author
			date = chunk.find('published').text		#date
			link = 	chunk.find('url').text		# article link

			if 'stream' in title.lower() or 'instant deck tech' in title.lower():
				content_type = 'Video'
			elif 'podcast' in title.lower():
				content_type = 'Podcast'
			else:
				content_type = 'Article'	

			temp_article = Article(title, author, date, link, 'MTG Goldfish', source_url, 'Magic: The Gathering', content_type, 0)	
		except:
			print ('Error Collecting MTGGF Article')


def get_mtgmc_articles():
	source = "http://www.mtgmintcard.com/articles"
	source_url = 'http://www.mtgmintcard.com/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return 

	for chunk in soup.find_all('div', {'class':'col-sm-4'}):	
		try:
			title = chunk.a.text	# article title
			#getting rid of 'by ', then removing author and tags to leave only the date.
			authdatetags = chunk.find('div', {'class':'articlesDateAndWriter'}).text.replace('by ','')
			tags = chunk.find('div', {'class':'articlesTag'}).text
			author = chunk.find('div', {'class':'articlesDateAndWriter'}).a.text.strip()	#author
			authdate = authdatetags.replace(tags, '')
			date_and_day = authdate.replace(author, '').strip().split(',')	#removing author, splitting date and day
			date = date_and_day[0]		#omitting day
			link = chunk.a.get('href')	# article link

			temp_article = Article(title, author, date, link, 'MTG Mint Card', source_url, 'Magic: The Gathering', 'Article', 0)
		except:
			print ('Error Collecting MTGMC Article')		

def get_gm_articles():	# videos  # podcasts
	source = "http://www.gatheringmagic.com/feed/"
	source_url = 'http://www.gatheringmagic.com/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return

	for chunk in soup.find_all('item'):	
		try:
			title = chunk.find('title').text	# article title
			author = chunk.find('dc:creator').text	#author
			date = chunk.find('pubdate').text		#date
			link = chunk.find('link').text	# article link
			
			category_list = chunk.find_all('category')
			for category in category_list:
				category = category.text.strip().lower()
				if category == 'podcast':
					content_type = 'Podcast'
					break
				elif category == 'video':
					content_type = 'Video'
					break
				else:
					content_type = 'Article'	

			temp_article = Article(title, author, date, link, 'Gathering Magic', source_url, 'Magic: The Gathering', content_type, 0)
		except:
			print ('Error Collecting GM Article')

def get_edhrec_articles(): #videos #podcasts
	source = "http://articles.edhrec.com/feed/"
	source_url = 'https://edhrec.com/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return

	for chunk in soup.find_all('item'):	
		try:
			title = chunk.find('title').text	# article title
			author = chunk.find('dc:creator').text	#author
			date = chunk.find('pubdate').text		#date
			link = chunk.find('link').text	# article link

			category_list = chunk.find_all('category')
			for category in category_list:
				category = category.text.strip().lower()
				if category == 'articles':
					content_type = 'Article'
					break
				elif category == 'podcast':
					content_type = 'Podcast'
					break
				else:
					content_type = 'Video'

			temp_article = Article(title, author, date, link, 'EDHREC', source_url, 'Magic: The Gathering', content_type, 0)
		except:
			print ('Error Collecting EDHREC Article')

'''def get_tappedout_articles():
	source = "http://tappedout.net/mtg-articles/"
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)
	articles={}

	if soup == False:
		return articles

	
	for chunk in soup.find_all('div', {'class':'well'}):	
		
		title = chunk.h2.a.text	# article title
		authdate = chunk.h4.text.split('by')
		author = authdate[1].strip()	# author
		date = authdate[0].strip()	# article date
		link = "http://tappedout.net" + chunk.h2.a.get('href')	# article link

		date = format_date(date)
		articles[title] = [author, date, link, 'TappedOut', 'http://tappedout.net/', 'Magic: The Gathering', content_type]	# add dict entry
	
	return articles'''

def get_flipside_articles():
	source = "https://www.flipsidegaming.com/blogs/magic-blog"
	source_url = 'https://www.flipsidegaming.com/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return

	for chunk in soup.find_all('div', {'class':'mt-xl mb-sm'}):	
		try:
			title = chunk.h2.a.text	# article title
			author = chunk.find('strong').text.replace('Posted by', '').strip()	# author
			date = chunk.find('em').text	# article date
			link = "https://www.flipsidegaming.com" + chunk.h2.a.get('href')	# article link
			
			temp_article = Article(title, author, date, link, 'FlipSide Gaming', source_url, 'Magic: The Gathering', 'Article', 0)
			
		except:
			continue 
			#posts with no author are just decklists
	

def get_hareruya_articles():	# videos
	source = "http://www.hareruyamtg.com/article/en/"
	source_url = 'http://www.hareruyamtg.com/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return

	for chunk in soup.find_all('div', {'class':'article_list ref clearfix'}):	
		
		try:
			title = chunk.find('li', {'class':'article_ttl'}).text.strip()	# article title	
			author = chunk.find('li', {'class':'article_author'}).text.strip()	#author
			date = chunk.p.text		#date
			link = chunk.a.get('href')	# article link

			
			cat_soup = chunk.find('ul', {'class':'data tag_container clearfix'})
			for category in cat_soup.find_all('li'):
				category = category.text.strip().lower()
				if category == 'video':					
					content_type = 'Video'
					break
				else:
					content_type = 'Article'
		except:
			continue

		temp_article = Article(title, author, date, link, 'HareruyaMTG', source_url, 'Magic: The Gathering', content_type, 0)
		

def get_pucatrade_articles():
	source = "https://pucatrade.com/articles"
	source_url = 'https://pucatrade.com/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return

	big_chunk = soup.find('div', {'class':'tse-content'})
	for chunk in big_chunk.find_all('div', {'class':['head','item']}):	
			try:
				title = chunk.find(['h1','h2'],{'class':'title'}).text.strip()	# article title		
				author = chunk.find('div', {'class':'name'}).text.strip()	#author
				date = chunk.find('div', {'class':'date letter'}).text		#date
				try:
					title = chunk.find(['h2'],{'class':'title'}).text.strip()
					author = chunk.find('div', {'class':'name'}).text.strip()	#author
					date = chunk.find('div', {'class':'date letter'}).text		#date
					link = 'https://pucatrade.com' + chunk.h2.a.get('href')	# article link
				except:
					title = chunk.find(['h1'],{'class':'title'}).text.strip()
					author = chunk.find('div', {'class':'name'}).text.strip()	#author
					date = chunk.find('div', {'class':'date letter'}).text		#date
					link = 'https://pucatrade.com' + big_chunk.a.get('href')


				temp_article = Article(title, author, date, link, 'Pucatrade', source_url, 'Magic: The Gathering', 'Article', 0)
			except:
				print ('Error Collecting PT Article')

def get_legitmtg_articles():
	source = "http://legitmtg.com/"
	source_url = 'http://legitmtg.com/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return

	for chunk in soup.find_all('article'):	
		try:
			title = chunk.h1.text	# article title
			author = chunk.p.a.get('title').strip()	#author
			date = chunk.p.find('time').text.strip()		#date
			link = chunk.h1.a.get('href')	# article link

			cat_soup = chunk.find('p', {'class':'meta'})
			content_type = 'Article'
			for category in cat_soup.find_all('a'):
				category = category.text.strip().lower()
				if category == 'multimedia':					
					content_type = 'Video'
				elif category == 'podcasts':
					content_type = 'Podcast'
					break	

			temp_article = Article(title, author, date, link, 'Legit MTG', source_url, 'Magic: The Gathering', content_type, 0)
		except:
			print ('Error Collecting LMTG Article')

def get_mtg1_articles():
	source = "http://mtg.one/"
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return

	for chunk in soup.find_all('article'):	
		try:
			title = chunk.find('h2',{'class':'entry-title'}).text.strip()
			date = chunk.find('time').text		#date
			link = chunk.h2.a.get('href')	# article link

			#author only listed on article page, need to go deeper
			authreq = urllib.request.Request(link, headers={'User-Agent' : "Google Chrome"})
			authsoup = make_soup(authreq, link)

			if authsoup == 'error':		#go to next article if error
				continue
			author = authsoup.find('div', {'class':'saboxplugin-authorname'}).a.text.strip()

			temp_article = Article(title, author, date, link, 'MTG.ONE', source, 'Magic: The Gathering', 'Article', 0)
		except:
			print ('Error Collecting MTG1 Article')

def get_cs_articles():
	source = "http://commandersociety.com/feed/"
	source_url = 'http://commandersociety.com/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return

	for chunk in soup.find_all('item'):	
		try:
			title = chunk.find('title').text	# article title
			author = chunk.find('dc:creator').text	#author
			date = chunk.find('pubdate').text		#date
			link = chunk.find('link').text	# article link

			category_list = chunk.find_all('category')
			for category in category_list:
				category = category.text.strip().lower()
				content_type = 'Article'	
				if category == 'videos':
					content_type = 'Video'
					break
				elif category == 'podcasts':
					content_type = 'Podcast'
					break

			temp_article = Article(title, author, date, link, 'Commander Society', source_url, 'Magic: The Gathering', content_type, 0)
		except:
			print ('Error Collecting CS Article')

#######################################


				# HS #
def get_blizzpro_articles():
	source = "http://hearthstone.blizzpro.com/feed/"
	source_url = 'http://hearthstone.blizzpro.com/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return

	for chunk in soup.find_all('item'):	
		try:
			title = chunk.find('title').text	# article title
			author = chunk.find('dc:creator').text	#author
			date = chunk.find('pubdate').text		#date
			link = chunk.find('link').text	# article link

			category_list = chunk.find_all('category')
			for category in category_list:
				category = category.text.strip().lower()
				content_type = 'Article'	
				if category == 'podcast':
					content_type = 'Podcast'
					break

			temp_article = Article(title, author, date, link, 'BlizzPro', source_url, 'Hearthstone', content_type, 0)
		except:
			print ('Error Collecting BP Article')

def get_blizzard_articles():
	source = "https://playhearthstone.com/en-us/blog/"
	source_url = 'https://playhearthstone.com/en-us/blog/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return

	articles_chunk = soup.find('div', {'class':'articles'})			
	for chunk in articles_chunk.find_all('h3', {'class':'article-title'}):	
		try:
			title = chunk.a.text.strip()	# article title
			link = chunk.a.get('href')	# article link
			if 'playhearthstone' in link:			# non playhearthstone articles are ignored
				link = 'https://playhearthstone.com' + link
			else:
				continue

			#going deeper to get date and author
			req2 = urllib.request.Request(link, headers={'User-Agent' : "Google Chrome"})
			soup2 = make_soup(req2, link)

			if soup2 == False:	#go to next article if error
				continue
			else:
				author = soup2.find('a', {'class':'article-author'}).text.strip()	#author
				date = soup2.find('span', {'class':'publish-date'}).text		#date
			
				temp_article = Article(title, author, date, link, 'Blizzard', source_url, 'Hearthstone', 'Article', 0)
		except:
			print ('Error Collecting BLZRD Article')

def get_toast_articles():	# videos
	source = "https://disguisedtoast.com/"
	source_url = 'https://disguisedtoast.com/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return

	for chunk in soup.find_all('div', {'class':'col-xs-12 col-sm-6'}):	
		try:
			title = chunk.h3.a.text.strip()	# article title
			link = 'https://disguisedtoast.com' + chunk.h3.a.get('href')	# article link
			author = 'Disguised Toast'	#author
			date = chunk.find('span', {'class':'dt-timestamp'}).text.replace('Published','').strip()		#date
			
			temp_article = Article(title, author, date, link, 'Disguised Toast', source_url, 'Hearthstone', 'Article', 0)
		except:
			print ('Error Collecting TOAST Article')

def get_hsplayers_articles():
	source = "https://hearthstoneplayers.com/feed/"
	source_url = 'https://hearthstoneplayers.com/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return

	for chunk in soup.find_all('item'):	
		try:
			title = chunk.find('title').text.strip()	# article title
			author = chunk.find('dc:creator').text	#author
			date = chunk.find('pubdate').text		#date
			link = chunk.find('link').text	# article link
			
			temp_article = Article(title, author, date, link, 'Hearthstone Players', source_url, 'Hearthstone', 'Article', 0)
		except:
			print ('Error Collecting HSP Article')

def get_vs_articles():
	source = "https://www.vicioussyndicate.com/feed/"
	source_url = 'https://www.vicioussyndicate.com/'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return

	for chunk in soup.find_all('item'):	
		try:
			title = chunk.find('title').text.strip()	# article title
			author = chunk.find('dc:creator').text	#author
			date = chunk.find('pubdate').text		#date
			link = chunk.find('link').text	# article link

			if chunk.find('category').text.lower() == 'vs news':
				continue	#ignore VS news posts
			
			temp_article = Article(title, author, date, link, 'Vicious Syndicate', source_url, 'Hearthstone', 'Article', 0)
		except:
			print ('Error Collecting VS Article')

def get_tempostorm_articles():	 # videos
	#json request
	source = 'https://tempostorm.com/api/articles?filter=%7B%22limit%22:20,%22order%22:%22createdDate+DESC%22,%22where%22:%7B%22isActive%22:true,%22articleType%22:%5B%22hs%22%5D%7D,%22fields%22:%7B%22id%22:true,%22articleType%22:true,%22authorId%22:true,%22createdDate%22:true,%22description%22:true,%22photoNames%22:true,%22themeName%22:true,%22title%22:true,%22premium%22:true,%22isActive%22:true%7D,%22include%22:%5B%7B%22relation%22:%22author%22,%22scope%22:%7B%22fields%22:%5B%22username%22%5D%7D%7D,%7B%22relation%22:%22slugs%22%7D%5D%7D'
	source_url = 'https://tempostorm.com/'
	req = requests.get(source)
	data = req.json()

	for item in data:
		try:
			title = (item['title']).strip()
			author = (item['author']['username']).strip()
			date = item['createdDate']
			link = 'https://tempostorm.com/articles/' + item['slugs'][0]['slug']
			
			if item['premium']['isPremium'] == True:
				premium = 1
			else:
				premium = 0	

			if '[Video]' in item['description']:
				content_type = 'Video'
			else:
				content_type = 'Article'
			
			temp_article = Article(title, author, date, link, 'Tempo Storm', source_url, 'Hearthstone', content_type, premium)
		except:
			print ('Error Collecting TS Article')

def get_hearthhead_articles():	
	source = "http://www.hearthhead.com/feed.atom"
	source_url = 'http://www.hearthhead.com'
	req = urllib.request.Request(source, headers={'User-Agent' : "Google Chrome"})
	soup = make_soup(req, source)

	if soup == False:
		return

	for chunk in soup.find_all('entry'):	
		try:
			title = chunk.find('title').text.strip()	# article title
			author = chunk.find('author').text	#author
			date = chunk.find('updated').text		#date
			link = chunk.find('id').text	# article link
			
			temp_article = Article(title, author, date, link, 'Hearthhead', source_url, 'Hearthstone', 'Article', 0)
		except:
			print ('Error Collecting HH Article')

def get_articles():
	
	Article.articles_list.clear()	# clear list before because this is in a loop

		### MTG Threads
	t1 = threading.Thread(target = get_scg_articles)
	t2 = threading.Thread(target = get_cfb_articles)	
	t3 = threading.Thread(target = get_mtggf_articles)
	t4 = threading.Thread(target = get_mtgmc_articles)
	t5 = threading.Thread(target = get_gm_articles)
	t6 = threading.Thread(target = get_edhrec_articles)
	t7 = threading.Thread(target = get_tcg_articles)
	t8 = threading.Thread(target = get_wotc_articles)
	t9 = threading.Thread(target = get_flipside_articles)
	t10 = threading.Thread(target = get_hareruya_articles)
	t11 = threading.Thread(target = get_pucatrade_articles)
	t12 = threading.Thread(target = get_legitmtg_articles)
	t13 = threading.Thread(target = get_mtg1_articles)
	t14 = threading.Thread(target = get_cs_articles)
	#### HS Threads
	th1 = threading.Thread(target = get_blizzpro_articles)
	th2 = threading.Thread(target = get_blizzard_articles)
	th3 = threading.Thread(target = get_toast_articles)
	th4 = threading.Thread(target = get_hsplayers_articles)
	th5 = threading.Thread(target = get_vs_articles)
	th6 = threading.Thread(target = get_tempostorm_articles)
	th7 = threading.Thread(target = get_hearthhead_articles)
	#### Starting Threads
	t1.start()
	t2.start()
	t3.start()
	t4.start()
	t5.start()
	t6.start()
	t7.start()
	t8.start()
	t9.start()
	t10.start()
	t11.start()
	t12.start()
	t13.start()
	t14.start()
	th1.start()
	th2.start()
	th3.start()
	th4.start()
	th5.start()
	th6.start()
	th7.start()
	### Joining threads
	t1.join()
	t2.join()
	t3.join()
	t4.join()
	t5.join()
	t6.join()
	t7.join()
	t8.join()
	t9.join()
	t10.join()
	t11.join()
	t12.join()
	t13.join()
	t14.join()
	th1.join()
	th2.join()
	th3.join()
	th4.join()
	th5.join()
	th6.join()
	th7.join()

	print('Data Collection Successful')
	return Article.articles_list