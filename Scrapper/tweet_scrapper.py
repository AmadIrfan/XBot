import time
import csv
from datetime import datetime
from model import Tweet
from Driver import WebDriver
from rich.progress import Progress
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from Auth.Authentication import CookiesAuth
from bs4 import BeautifulSoup


class TwitterScraper:
    def __init__(self, headless: bool = False):
        # print("✔ TwitterScraper initialized ....")
        self.driver = WebDriver(headless=headless).driver
        self.wait = WebDriverWait(self.driver, 10)
        self.tweet_links = []  # Global list to store tweet links

    def search(self, query: str = ""):
        """Search for a query on X."""
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
                )
            )
            search_box = self.driver.find_element(
                By.XPATH, "//input[@data-testid='SearchBox_Search_Input']"
            )
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            print(f"🔍 Searching for: {query}")
            time.sleep(2)
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet']"))
            )
        except Exception as e:
            print(f"⚠️ Search failed: {e}")

    def scroll_to_load(self, min_tweets: int = 30, delay: int = 2) -> list[str]:
        """Scroll and collect unique tweet links until we have enough."""
        print(f"⬇️ Scrolling to collect {min_tweets} tweet links...")
        
        collected_links = []
        scroll_count = 0
        max_scrolls = 50
        no_new_tweets_count = 0
        
        while len(collected_links) < min_tweets and scroll_count < max_scrolls:
            # Get current page HTML and parse with BeautifulSoup
            page_html = self.driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')
            
            # Find all tweet articles
            tweets = soup.find_all('article', {'data-testid': 'tweet'})
            
            # Extract links from current view
            previous_count = len(collected_links)
            for tweet in tweets:
                try:
                    # Find the link containing '/status/'
                    time_link = tweet.find('a', href=lambda href: href and '/status/' in href)
                    
                    if time_link and time_link.get('href'):
                        tweet_url = time_link['href']
                        
                        # Make it a full URL
                        if tweet_url.startswith('/'):
                            tweet_url = f"https://x.com{tweet_url}"
                        
                        # Add only if not already collected
                        if tweet_url not in collected_links:
                            collected_links.append(tweet_url)
                except:
                    continue
            
            new_tweets_found = len(collected_links) - previous_count
            # print(f"📜 Collected {len(collected_links)} unique links (found {new_tweets_found} new) after scroll {scroll_count + 1}")
            
            # If we have enough links, stop
            if len(collected_links) >= min_tweets:
                print(f"✅ Collected {len(collected_links)} tweet links")
                return collected_links[:min_tweets]
            
            # Check if no new tweets were found
            if new_tweets_found == 0:
                no_new_tweets_count += 1
                if no_new_tweets_count >= 3:
                    print(f"⚠️ No new tweets found after 3 scrolls. Stopping with {len(collected_links)} links")
                    return collected_links
            else:
                no_new_tweets_count = 0
            
            # Scroll down to load more
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(delay)
            scroll_count += 1
        
        # Return whatever we collected
        print(f"⚠️ Reached max scrolls. Returning {len(collected_links)} tweet links")
        return collected_links

    def collect_tweet_links(self, page_html: str, limit: int = 30) -> list[str]:
        """Use BeautifulSoup to extract tweet links from HTML."""
        print(f"🔗 Extracting tweet links with BeautifulSoup...")
        
        soup = BeautifulSoup(page_html, 'html.parser')
        tweets = soup.find_all('article', {'data-testid': 'tweet'})
        
        links = []
        for i, tweet in enumerate(tweets[:limit], start=1):
            try:
                # Find the link containing '/status/' which is the tweet URL
                time_link = tweet.find('a', href=lambda href: href and '/status/' in href)
                
                if time_link and time_link.get('href'):
                    tweet_url = time_link['href']
                    
                    # Make sure it's a full URL
                    if tweet_url.startswith('/'):
                        tweet_url = f"https://x.com{tweet_url}"
                    
                    if tweet_url not in links:
                        links.append(tweet_url)
                        # print(f"  📎 Link {len(links)}: {tweet_url}")
                        
            except Exception as e:
                print(f"⚠️ Failed to extract link from tweet {i}: {e}")
                continue
        
        print(f"✅ Collected {len(links)} tweet links")
        self.tweet_links = links  # Store in global list
        return links

    def fetch_tweet_details_in_tab(self, tweet_url: str) -> dict:
        """Open tweet in new tab and fetch details."""
        original_window = self.driver.current_window_handle
        
        try:
            # Open link in new tab
            self.driver.execute_script(f"window.open('{tweet_url}', '_blank');")
            time.sleep(1)
            
            # Switch to new tab
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(2)
            
            # Wait for tweet to load
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet']"))
            )
            
            # Get page HTML and parse with BeautifulSoup
            page_html = self.driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')
            
            # Find the main tweet article
            tweet = soup.find('article', {'data-testid': 'tweet'})
            
            if not tweet:
                return {}
            
            # Extract user
            user = "Unknown"
            user_elem = tweet.find('div', {'data-testid': 'User-Name'})
            if user_elem:
                user = user_elem.get_text().split('\n')[0]
            
            # Extract text
            text = "[No text available]"
            text_elem = tweet.find('div', {'data-testid': 'tweetText'})
            if text_elem:
                text = text_elem.get_text()
            else:
                # Fallback: find div with lang attribute
                lang_div = tweet.find('div', {'lang': True})
                if lang_div:
                    text = lang_div.get_text()
            
            # Extract datetime
            datetime_posted = ""
            time_elem = tweet.find('time')
            if time_elem:
                datetime_posted = time_elem.get('datetime', '')
            
            # Extract likes
            likes = "0"
            like_button = tweet.find('button', {'data-testid': 'like'})
            if like_button and like_button.get('aria-label'):
                import re
                numbers = re.findall(r'[\d,]+', like_button['aria-label'])
                if numbers:
                    likes = numbers[0].replace(',', '')
            
            # Extract views
            views = "N/A"
            # Look for analytics link
            analytics_link = tweet.find('a', href=lambda href: href and '/analytics' in href)
            if analytics_link and analytics_link.get('aria-label'):
                import re
                numbers = re.findall(r'[\d,]+', analytics_link['aria-label'])
                if numbers:
                    views = numbers[0].replace(',', '')
            
            # Close tab and switch back
            self.driver.close()
            self.driver.switch_to.window(original_window)
            
            return {
                "user": user,
                "text": text,
                "likes": likes,
                "views": views,
                "datetime": datetime_posted,
            }
            
        except Exception as e:
            print(f"⚠️ Error fetching tweet details from {tweet_url}: {e}")
            # Make sure we close the tab and switch back
            try:
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                self.driver.switch_to.window(original_window)
            except:
                pass
            return {}

    def extract_tweets(self, tweet_links: list[str], limit: int = 30) -> list[Tweet]:
        """Visit each tweet link in new tabs and extract details."""
        print("🧩 Starting tweet extraction process...")
        
        if not tweet_links:
            print("⚠️ No tweet links to process!")
            return []
        
        # Use only the links we need
        tweet_links = tweet_links[:limit]
        self.tweet_links = tweet_links  # Store in global list
        
        print(f"🔗 Processing {len(tweet_links)} tweet links")
        
        # Visit each link in new tab and extract details
        tweets_data: list[Tweet] = []
        failed_count = 0
        
        print(f"\n📖 Opening {len(tweet_links)} tweets in new tabs to extract details...")
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Extracting tweet details...", total=len(tweet_links))
            
            for i, link in enumerate(tweet_links, start=1):
                try:
                    details = self.fetch_tweet_details_in_tab(link)
                    
                    if details:
                        tweets_data.append(
                            Tweet(
                                user=details.get("user", "Unknown"),
                                text=details.get("text", "[No text]"),
                                views=details.get("views", "N/A"),
                                likes=details.get("likes", "0"),
                                datetime=details.get("datetime", ""),
                            )
                        )
                    else:
                        failed_count += 1
                    
                    progress.update(task,completed=i, advance=1)
                    
                except Exception as e:
                    print(f"⚠️ Failed to process tweet {i}: {e}")
                    failed_count += 1
                    progress.update(task, advance=1)
                    continue
        
        print(f"✅ Extracted {len(tweets_data)} tweets ({failed_count} failed)")
        return tweets_data

    def exec(self, auth: CookiesAuth, query: str = "ai news", min_tweets: int = 30, tweet_limit: int = 30):
        """Full pipeline: login, search, scroll to collect links, open in tabs, and save to CSV."""
        auth.login(self.driver)
        self.search(query)
        tweet_links = self.scroll_to_load(min_tweets=min_tweets)
        tweet_data = self.extract_tweets(tweet_links, limit=tweet_limit)
        return tweet_data