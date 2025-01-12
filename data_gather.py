from tweets import scrape


tweets = scrape.get_tweets(search = "#storm #daniel until:2023-09-12 since:2023-09-01")
scrape.export_tweets_collected(tweets)