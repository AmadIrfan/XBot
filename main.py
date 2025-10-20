import pandas  as pd
from save import CSVSave
from pathlib import Path
from Cookies import Cookies
from Auth import CookiesAuth
from Scrapper import TwitterScraper
from settings import COOKIE_PATH, HEADLESS




class Bot:
    def __init__(self):
        print('Bot initialize.... ')

    def exec(self):
        try:
            query = input("Enter search query for X (Twitter): ") or "AI trends"    
            cookies = Cookies(cookies_path=Path(COOKIE_PATH))
            cookie = cookies.load_cookies()
            ts = TwitterScraper(headless=HEADLESS)
            auth = CookiesAuth(cookies=cookie)
            tweets=ts.exec(auth=auth,query=query)
            svc=CSVSave()
            svc.save(tweets,output_csv=f'{query}.csv')
        except Exception as e:
            print(f'{e}')
        finally:
                print(" Closing browser...")
                print(" Done.")


    
    
    
def main():
    bot=Bot()
    bot.exec()

if __name__ == "__main__":
    main()
    pass



# df=pd.read_csv('./wars.csv',encoding='utf-8',delimiter='|')
# print(df.head(5))
# user|text|views|likes|datetime
# print(len(df))
# for i in df['views']:
#      print(i)