from tweets import scrape
from tweets import search_chunks


search1 = "#storm #daniel until:2023-09-12 since:2023-09-01"
search2 = "#kategida #daniel until:2023-09-12 since:2023-09-01"
search3 = "#storm #thessaly #daniel until:2023-09-12 since:2023-09-01"
search4 = "#storm #daniel #derna until:2023-09-12 since:2023-09-01"
search5 = "#πλημμύρες #κακοκαιρια #Daniel until:2023-09-12 since:2023-09-01"
search6 = "#storm #daniel"
# Circumvent X breaking down when wanting to bring lots of tweets. Break general hashtags into a list of search terms to loop through
start_date = "2023-09-01"
end_date = "2024-09-01"

## usage example : note , this is still experimental , it returns random crappy results and eventually the loop breaks for some reason
queries = search_chunks.break_into_timechunks(search6, start_date, end_date)

## tested list. Supply your own! 
multiple_search_terms = [search1,search2,search3,search4,search5,search6]


tweets = scrape.get_tweets(queries,max_tweets = 300)
scrape.export_tweets_collected(tweets,search3)