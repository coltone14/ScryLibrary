# ScryLibrary
program and django files

Scrape does the dirty work. It collects the article data using the BeautifulSoup and Json libraries. Each website has its own function, which is also a thread. One data collection cycle typically lasts 8-12 seconds.
DBManager is the database manager, handling the database connection as well as populating and pruning the database.
Controller runs the full program on a 5 minute interval.
