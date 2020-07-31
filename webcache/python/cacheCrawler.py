#!/usr/bin/env python3

import os
import sys
import requests
import signal
import yaml
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from pathlib import Path
from random import randint


def crawler(dmin, dmax, wmin, wmax, emin, emax, UA):
    """
        討論串編號      dmin ~ dmax
        例常等待間隔    wmin ~ wmax
        意外等待間隔    emin ~ emax
    """
    print(UA)
    logger(UA)

    # 為了讓 429 能夠重試，只好改用這種寫法
    i = dmin
    while i < dmax:
        logtemp = ""
        now = str(time.strftime("%m/%d %H:%M:%S", time.localtime()))
        print(f"\r[{now}] 編號 {i}: ", end='')
        logtemp += f"\r[{now}] 編號 {i}: "

        headers = {
            "User-Agent": UA
        }
        Html = f"http://webcache.googleusercontent.com/search?q=cache:https://kater.me/d/{str(i)}"

        res = requests.get(Html, headers=headers, timeout=30)
        res.encoding = "utf-8"

        status = res.status_code

        print(f"[{status}] ", end='')
        logtemp += f"[{status}] "

        soup = BeautifulSoup(res.text, 'html.parser')

        # 只存有內容的快取
        if status in [200, 404]:
            if(status == 200):
                filename = f"./d/{str(i)}.html"
                print(f"({filename}) ", end='')
                logtemp += f"({filename}) "

                with open(filename, 'w', encoding="utf-8") as file:
                    file.write(soup.prettify())
            else:
                print(f"(狀態 404 不存檔) ", end='')
                logtemp += f"(狀態 404 不存檔) "

            s = randint(wmin, wmax) / 1000
            print(f"等待請求間隔 {s} 秒")
            logtemp += f"等待請求間隔 {s} 秒"
            logger(logtemp)

            waiting(s)
        else:
            if(status == 429):
                print(f"(狀態 429 更換 User-Agent 並等待一段時間) ", end='')
                s = randint(emin, emax) / 1000
                print(f"等待請求間隔 {s} 秒")

                logtemp += f"(狀態 429 更換 User-Agent 並等待一段時間) 等待請求間隔 {s} 秒"
                logger(logtemp)

                UA = ua.random
                print(UA)
                logger(UA)

                waiting(s)
                i -= 1
            else:
                print(f"(非預期狀態，目前版本不採取動作)", end='')
                s = randint(wmin, wmax) / 1000
                print(f"等待請求間隔 {s} 秒")

                logtemp += f"(非預期狀態，目前版本不採取動作) 等待請求間隔 {s} 秒"
                logger(logtemp)

                waiting(s)

        i += 1


def handler(sig, frame):
    print("\r程式已被使用者中止")
    logger("\n程式已被使用者中止\n\n")
    sys.exit(0)


def waiting(remaining):
    while(remaining > 0):
        print(f"\r{'{:.3f}    '.format(remaining)}", end='')
        remaining -= 0.033
        time.sleep(0.033)


def logger(log):
    with open("log.txt", 'a', encoding="utf-8") as file:
        file.write(log)


def checkConfig():
    print("正在讀取設定檔...")
    logger("正在讀取設定檔...\n")
    with open("config.yml", 'r', encoding="utf-8") as stream:
        try:
            _config = yaml.safe_load(stream)
        except yaml.YAMLError as error:
            print("讀取設定檔失敗！程式已終止。")
            logger("讀取設定檔失敗！程式已終止。\n\n")
            print(error)
            input()
            sys.exit(255)

    print("正在檢查設定檔格式")
    logger("正在檢查設定檔格式\n")

    try:
        dmin = _config["range"]["min"] + 0
        dmax = _config["range"]["max"] + 0
        wmin = _config["interval"]["routine"]["min"] + 0
        wmax = _config["interval"]["routine"]["max"] + 0
        emin = _config["interval"]["exception"]["min"] + 0
        emax = _config["interval"]["exception"]["max"] + 0
    except error:
        print("檢查格式失敗，請確定格式與 config.example.yml 一致，並且皆爲數值。程式已終止。")
        logger("檢查格式失敗，請確定格式與 config.example.yml 一致，並且皆爲數值。程式已終止。\n\n")
        print(error)
        input()
        sys.exit(254)

    print(f"已讀取設定：\n    討論編號     {dmin} ~ {dmax}\n    例常等待時間 {wmin / 1000} ~ {wmax / 1000} 秒\n    例外等待時間 {emin / 1000} ~ {emax / 1000} 秒\n")
    logger(f"已讀取設定：\n    討論編號     {dmin} ~ {dmax}\n    例常等待時間 {wmin / 1000} ~ {wmax / 1000} 秒\n    例外等待時間 {emin / 1000} ~ {emax / 1000} 秒\n\n")
    return [dmin, dmax, wmin, wmax, emin, emax]


# ----------------------- Main ----------------------- #
logger("--------------------------------\n\n")
now = str(time.strftime("%m/%d %H:%M:%S", time.localtime()))
print(now)
logger(f"{now} 程式開始\n\n")

# 攔截終止訊號
signal.signal(signal.SIGINT, handler)

# 建立資料夾 d
Path("./d").mkdir(parents=True, exist_ok=True)

# 從檔案取得 UA
ua = UserAgent(path="./fake-useragent.json")

# 檢查 config.yml 是否存在
if Path("./config.yml").is_file():
    config = checkConfig()
else:
    print("找不到設定檔 config.yml，程式已終止。")
    logger("找不到設定檔 config.yml，程式已終止。\n\n")
    input()
    sys.exit(100)

# （主要）自動爬取檔案
crawler(config[0], config[1], config[2],
        config[3], config[4], config[5], ua.random)

# 程式完成
print("\r        \n已完成！按 ENTER 關閉程式")
logger("\n已完成！\n\n")
input()
