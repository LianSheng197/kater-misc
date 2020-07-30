import sys
import requests
import time
from bs4 import BeautifulSoup

def hello(start, end):
    for i in range(start, end):
        print(i)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
        Html = 'http://webcache.googleusercontent.com/search?q=cache:https://kater.me/d/' + \
            str(i)
        res = requests.get(Html, headers=headers, timeout=30)
        res.encoding = "utf-8"
        print(res.status_code)
        soup = ""
        soup = BeautifulSoup(res.text, 'html.parser')

        # 只存有內容的快取
        if(soup is not None):
            with open(str(i) + '.html', 'w', encoding="utf-8") as file:
                file.write(soup.prettify())
        time.sleep(20)

if(len(sys.argv) == 3):
    hello(int(sys.argv[1]), int(sys.argv[2]))
else:
    print("參數錯誤")