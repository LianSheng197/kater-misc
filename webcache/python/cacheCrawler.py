#!/usr/bin/env python3

import os
import sys
import requests
import signal
import yaml
from time import sleep
from bs4 import BeautifulSoup
from pathlib import Path
from random import randint


def crawler(discussionStart, discussionEnd, UA):
    for i in range(discussionStart, discussionEnd):
        print(f"\r編號 {i}: ", end='')
        headers = {
            "User-Agent": ""
        }
        Html = f"http://webcache.googleusercontent.com/search?q=cache:https://kater.me/d/{str(i)}"

        res = requests.get(Html, headers=headers, timeout=30)
        res.encoding = "utf-8"

        status = res.status_code

        print(f"[{status}] ", end='')

        soup = BeautifulSoup(res.text, 'html.parser')

        # 只存有內容的快取
        if(status == 200):
            filename = f"./d/{str(i)}.html"
            print(f"({filename}) ", end='')
            with open(filename, 'w', encoding="utf-8") as file:
                file.write(soup.prettify())

        s = randint(6789, 23456) / 1000
        print(f"等待請求間隔 {s} 秒")
        waiting(s)


def handler(sig, frame):
    print("\r程式已結束")
    sys.exit(0)


def waiting(time):
    while(time > 0):
        print(f"\r{'{:.3f}'.format(time)}", end='')
        time -= 0.033
        sleep(0.033)


def checkConfig():
    with open("config.yml", 'r', encoding="utf-8") as stream:
        try:
            _config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print("讀取設定檔失敗！")
            print(exc)
            sys.exit(255)

    print("正在檢查設定檔格式")

    if(_config["token"] == None):
        print("設定錯誤：未填入 token")
        input()
        sys.exit(201)
    if(not isinstance(_config["report"]["period"], int) or _config["report"]["period"] < 30):
        print("設定錯誤： report.period 必須是正整數，且不能小於 30")
        input()
        sys.exit(202)
    if(not isinstance(_config["report"]["warningLevel"], int) or _config["report"]["warningLevel"] < 1 or _config["report"]["warningLevel"] > 3):
        print("設定錯誤： report.warningLevel 必須是 1, 2, 3 其一")
        input()
        sys.exit(203)


# ----------------------- Main ----------------------- #
# 攔截終止訊號
signal.signal(signal.SIGINT, handler)

# 建立資料夾 d
Path("./d").mkdir(parents=True, exist_ok=True)

# 檢查 config.yml 是否存在
if Path("./config1.yml").is_file():
    print()
else:
    print("找不到設定檔 config.yml，程式已終止。")
    input()
    sys.exit(100)

# （主要）自動爬取檔案
crawler(80000, 80002)

# 程式完成
print("\r已完成！按 ENTER 關閉程式")
input()
