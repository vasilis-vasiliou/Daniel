from tweets import scrape

search1 = "#storm #daniel until:2023-09-12 since:2023-09-01"
search2 = "#kategida #daniel until:2023-09-12 since:2023-09-01"
search3 = "#storm #thessaly #daniel until:2023-09-12 since:2023-09-01"
search4 = "#storm #daniel #derna until:2023-09-12 since:2023-09-01"
search5 = "#πλημμύρες #κακοκαιρια #Daniel until:2023-09-12 since:2023-09-01"

tweets = scrape.get_tweets(search = search3,max_tweets = 200)
scrape.export_tweets_collected(tweets,search3)