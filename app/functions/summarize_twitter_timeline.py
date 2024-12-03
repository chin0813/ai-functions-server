import os
import time
import re
import sqlite3
import traceback
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from groq import Groq
from pydantic import BaseModel
from app.utils.ai_functions import AIFunctions


load_dotenv()

if not load_dotenv():
    print("Warning: .env file not loaded")

class SummarizeTwitterTimelineInput(BaseModel):
    login: str
    password: str

class SummarizeTwitterTimelineOuput(BaseModel):
    summary: str

def summarize_twitter_timeline(SummarizeTwitterTimelineInput) -> SummarizeTwitterTimelineOuput:
    try:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            print("Error: GROQ_API_KEY is not set.")
            exit(1)

        print(f"API Key loaded: {api_key[:5]}...")  


        client = Groq(api_key=api_key)

        chrome_options = Options()
        # chrome_options.add_argument("user-data-dir=C:/Users/mklas/AppData/Local/Google/Chrome/User Data")
        # chrome_options.add_argument("profile-directory=Profile 3")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=chrome_options)

        timeout_value = 30  # This should be an int, float, or None
        driver.set_page_load_timeout(timeout_value)
        driver.set_script_timeout(timeout_value)

        driver.get("https://x.com/i/flow/login?lang=en")

        # Wait for the username field to appear
        username_field = None
        for _ in range(timeout_value):
            try:
                username_field = driver.find_element(By.XPATH, '//input[@name="text"]')
                if username_field:
                    break
            except:
                time.sleep(1)
        if not username_field:
            raise ValueError("Username field did not appear within the timeout period.")
        
        username_field.send_keys(SummarizeTwitterTimelineInput.login)
        # username_field.send_keys("irenezhaovp@gmail.com")
        
        # Click next
        next_buttons = driver.find_elements(By.XPATH, '//button')
        for button in next_buttons:
            if "next" in button.get_attribute("innerText").strip().lower():
                button.click()
                break
            
        # Wait for the password field to appear
        password_field = None
        for _ in range(timeout_value):
            try:
                password_field = driver.find_element(By.XPATH, '//input[@name="password" and @type="password"]')
                if password_field:
                    break
            except:
                time.sleep(1)
        if not password_field:
            raise ValueError("Password field did not appear within the timeout period.")

        password_field.send_keys(SummarizeTwitterTimelineInput.password)
        # password_field.send_keys("vpsuper999")

        # Click on the "Log in" button
        login_buttons = driver.find_elements(By.XPATH, '//button')
        for button in login_buttons:
            if "log in" in button.get_attribute("innerText").strip().lower():
                button.click()
                break

        time.sleep(timeout_value)
        
        # Wait for the articles to appear
        tweet_elements = None
        for _ in range(timeout_value):
            try:
                tweet_elements = driver.find_elements(By.XPATH, '//article[@role="article"]')
                if tweet_elements:
                    break
            except:
                time.sleep(1)
        if not tweet_elements:
            raise ValueError("Tweet elements did not appear within the timeout period.")

        tweets = []
        for tweet_element in tweet_elements[:10]:
            tweet_content = tweet_element.text
            video_links = tweet_element.find_elements(By.XPATH, './/video')
            media_links = []

            for video in video_links:
                video_url = video.get_attribute('src')
                if video_url:
                    media_links.append(video_url)

            if media_links:
                tweet_content += "\nMedia Links: " + ', '.join(media_links)

            tweets.append(tweet_content)

        def clean_tweet_data(tweet):
            tweet = re.sub(r'http\S+', "", tweet)
            tweet = re.sub(r'@[\w]+', '', tweet)
            tweet = re.sub(r'#\w+', '', tweet)
            tweet = re.sub(r'[^\W\S]', '', tweet)
            tweet = re.sub(r'\n+', '\n', tweet)
            tweet = tweet.strip()
            tweet = tweet.replace('\n',' ')
            return tweet

        cleaned_tweets = [clean_tweet_data(tweet) for tweet in tweets]

        print("\n--- Prepared Data for API ---")
        for idx, tweet in enumerate(cleaned_tweets, 1):
            print(f"Tweet {idx}: {tweet}")

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a smart assistant that can summarize what you have learned. You will be given some tweets to summarize."},
                {"role": "user", "content": f"These are the tweets: \n" + "\n".join(cleaned_tweets)}
            ],
            model="llama3-8b-8192"  
        )

        summary_response = chat_completion.choices[0].message.content
        print("\n--- Generated Response ---")
        print(summary_response)

        time.sleep(34)
        driver.quit()
    except Exception as e:
        traceback.print_exc()
        raise ValueError(f"Failed to summarize Twitter timeline: {e}")

AIFunctions.register("summarize_twitter_timeline", SummarizeTwitterTimelineInput, SummarizeTwitterTimelineOuput, summarize_twitter_timeline)
