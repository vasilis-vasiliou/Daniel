from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time
from datetime import datetime

def get_tweets(search,max_tweets=100):
    # Load environment variables
    EMAIL = os.getenv("X_email")
    PASSWORD = os.getenv("X_pass")

    # Initialize the driver
    driver = webdriver.Chrome()

    try:
        # Navigate to the login page
        driver.get("https://x.com/login")
        
        # Wait for the email input field to be visible and fill in the email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        email_input.send_keys(EMAIL)
        
        # Locate and click the "Next" button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'css-146c3p1') and .//span[text()='Next']]"))
        )
        next_button.click()
        
        # Wait for the potential username input field
        try:
            username_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@data-testid='ocfEnterTextTextInput']"))
            )
            username_input.send_keys('basibluepill')
            
            # Locate and click the "Next" button after entering the username
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'css-146c3p1') and .//span[text()='Next']]"))
            )
            next_button.click()
        except:
            print("Username input not required.")
        
        # Wait for the password field to be visible and fill in the password
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(PASSWORD)
        
        # Submit the form by pressing Enter
        password_input.send_keys(Keys.RETURN)
        
        # Wait to ensure the login is successful or redirected
        WebDriverWait(driver, 10).until(
            EC.url_changes("https://x.com/login")
        )
        
        print("Login successful!")
    except Exception as e:
        print(f"An error occurred while trying to login: {e}")
    
    print(f'starting the search process for the terms supplied: {search}')
            # Start collecting tweets for search term
    tweets = []
    tweet_ids = set()  # To avoid duplicates
    scroll_attempts = 0
    max_scroll_attempts = 50  # Safeguard against infinite scrolling
    for search_query in search:
        explore_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Search and explore']"))
    )
    
    # Click the explore icon
        explore_button.click()
        
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@data-testid='SearchBox_Search_Input']"))
        )
    
        print(f'Now searching : {search_query}')
        search_input.send_keys(search_query)
        search_input.send_keys(Keys.RETURN)
            
        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//article"))
            )
            


        while len(tweets) < max_tweets and scroll_attempts < max_scroll_attempts:
            try:
                # Dynamically locate tweet elements in each iteration
                tweet_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//article[@data-testid='tweet']"))
                )

                for tweet_element in tweet_elements:
                    try:
                        # Extract unique tweet ID
                        tweet_id = tweet_element.get_attribute("data-tweet-id") or str(hash(tweet_element.text))

                        # Extract tweet text
                        tweet_text_element = tweet_element.find_element(By.XPATH, "//div[@data-testid='tweetText']")
                        tweet_text = tweet_text_element.text if tweet_text_element else "N/A"

                        # Extract user name
                        user_name_element = tweet_element.find_element(By.XPATH, ".//div[@data-testid='User-Name']//a[@role='link']")
                        user_name = user_name_element.text if user_name_element else "N/A"

                        # Extract timestamp
                        timestamp_element = tweet_element.find_element(By.XPATH, "//time")
                        timestamp = timestamp_element.get_attribute("datetime") if timestamp_element else "N/A"


                        # views locator : #id__zrtchw1xwla > div:nth-child(4) > a > div > div.css-175oi2r.r-xoduu5.r-1udh08x > span > span > span
                        # Avoid duplicates
                        if tweet_id and tweet_id not in tweet_ids:
                            tweets.append({
                                "id": tweet_id,
                                "text": tweet_text,
                                "user_name": user_name,
                                "timestamp": timestamp,
                            })
                            tweet_ids.add(tweet_id)
                            print(f'tweet by {user_name} @{timestamp} saying : {tweet_text}' )
                            if len(tweets) >= 100:
                                break
                    except Exception as inner_ex:
                        # Handle any issues with individual tweet elements
                        print(f"Skipping a tweet due to error: {inner_ex}")

                # Scroll down to load more tweets
                scroll_height = driver.execute_script("return document.body.scrollHeight")
                print(scroll_height)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                new_scroll_height = driver.execute_script("return document.body.scrollHeight")
                time.sleep(2)  # Allow time for new content to load
                scroll_attempts += 1
                if scroll_height == new_scroll_height:
                    print('no more tweets. breaking ..')
                    break

            except Exception as e:
                print(f"Error while scrolling or locating tweets: {e}")
                break  # Exit the loop if repeated issues occur
        
    driver.close()
    return tweets



def export_tweets_collected(tweets,search_text):    # Create a DataFrame and export to CSV
    df = pd.DataFrame(tweets)
    current_date = datetime.now()
    df.to_csv(f"data/tweets{current_date}_{search_text}.csv", index=False)
    print("Exported tweets")


