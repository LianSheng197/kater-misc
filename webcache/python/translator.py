import json
import re
import sys
import time
import datetime
from pathlib import Path
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup, Tag


def getChildrenList(element):
    if isinstance(element, Tag):
        return list(element.children)
    else:
        return list()


def hasChildren(element):
    return isinstance(element, Tag) and len(getChildrenList(element)) > 0


def isLinkImage(element):
    child = getChildrenList(element)
    return len(child) == 1 and child[0].name == "img"


def getLinkUrl(element):
    return element["href"]


def getImageUrl(element):
    if(element.name == "img"):
        return element["src"]
    elif(element.name == "a"):
        return getChildrenList(element)[0]["src"]


def nospace(string):
    string = re.sub(r"^\ +", "", string)
    string = re.sub(r"\ +$", "", string)
    return string


def mdParser(element, noBreakLine=True):
    global md

    # 沒有子節點
    if not hasChildren(element):
        if isinstance(element, Tag):
            content = nospace(element.text)
            if noBreakLine:
                content = content.replace("\n", "")
                content = nospace(content)
                md += f"{content}"
            else:
                md += f"{content}"
        else:
            content = nospace(element)
            if noBreakLine:
                content = content.replace("\n", "")
                content = nospace(content)
                md += f"{content}"
            else:
                md += f"{content}"
        return
    # 有子節點
    else:
        for e in getChildrenList(element):
            # e 為節點
            if isinstance(e, Tag):
                if e.name not in ["script", "style"]:
                    if(isLinkImage(e)):
                        md += f"![]({getImageUrl(e)})"
                    elif(e.name == "a"):
                        if(e.has_attr("class") and e["class"][0] == "PostMention"):
                            content = nospace(e.text).replace("\n", "")
                            md += f"[回覆：{content}](#)\n"
                        else:
                            content = nospace(e.text).replace("\n", "")
                            md += f"[{content}]({getLinkUrl(e)})"
                    elif(e.name == "p"):
                        mdParser(e)
                        md += "\n\n"
                    elif(e.name == "iframe"):
                        if e.has_attr("src"):
                            src = e["src"]

                            if("www.youtube.com" in src):
                                # https://www.youtube.com/watch?v=<id>
                                src = src.replace("embed/", "watch?v=")
                                md += src
                            elif("twitter.min.html" in src):
                                # https://twitter.com/x/status/<id>
                                id = src.split("#")[1]
                                md += f"https://twitter.com/x/status/{id}"
                            elif("facebook.min.html" in src):
                                # https://www.facebook.com/x/posts/<id>
                                # https://www.facebook.com/watch/?v=<id>
                                id = src.split("#")[1]

                                if "video" in id:
                                    id = id.replace("video", "")
                                    md += f"https://www.facebook.com/watch/?v={id}"
                                elif "post" in id:
                                    id = id.replace("post", "")
                                    md += f"https://www.facebook.com/x/posts/{id}"
                                else:
                                    md += f"https://www.facebook.com/x/posts/{id}"
                            else:
                                # SoundCloud 無須轉換
                                md += src

                            md += "\n"

                    elif(e.name == "blockquote"):
                        md += "[quote]\n"
                        mdParser(e)
                        md += "[/quote]\n\n"
                    elif(e.name in ["code", "pre"]):
                        if(e.name == "pre"):
                            mdParser(e, noBreakLine=False)
                        else:
                            if(e.parent.name == "pre"):
                                if(e.has_attr("class")):
                                    lang = e["class"][0].split("-")[1]
                                    md += f"```{lang}\n"
                                    mdParser(e, noBreakLine=False)
                                    md += "\n```\n"
                            else:
                                md += f" `"
                                mdParser(e)
                                md += "` "
                    elif(e.name == "br"):
                        md += "\n"
                    elif(e.name == "strong"):
                        md += "**"
                        mdParser(e)
                        md += "**"
                    else:
                        mdParser(e)

            # e 不是節點（只是文字）
            else:
                content = nospace(e)
                if noBreakLine:
                    content = content.replace("\n", "")
                    md += f"{content}"
                else:
                    md += f"{content}"


originHtml = "./d"
translatedJson = "./translated/json"
translatedMarkdown = "./translated/markdown"
translatedHtml = "./translated/html"

files = [f for f in listdir(originHtml) if isfile(join(originHtml, f))]

filenames = list(map(lambda x: x.split(".")[0], files))
filenames = sorted(filenames)

Path("./translated/json").mkdir(parents=True, exist_ok=True)
Path("./translated/markdown").mkdir(parents=True, exist_ok=True)

for filename in filenames:
    if not Path(f"./translated/json/{filename}.json").is_file():
        raw = ""
        with open(f"{originHtml}/{filename}.html", "r", encoding="utf-8") as file:
            raw = file.read()

        soup = BeautifulSoup(raw, "html.parser")

        baseUrl = ""
        try:
            baseUrl = soup.find("base")["href"]
        except:
            baseUrl = f"https://kater.me/d/{filename}"

        
        cacheTime = ""
        try:    
            cacheTime = soup.select_one("div#bN015htcoyT__google-cache-hdr span:nth-child(2)").text.replace("\n", "")

            if(re.findall(r'[\u4e00-\u9fff]+', cacheTime)):
                cacheTime = re.search(r"2020.+?GMT", cacheTime).group(0)
                cacheTime = int(time.mktime(datetime.datetime.strptime(cacheTime, "%Y年%m月%d日 %H:%M:%S GMT").timetuple()))
            else:
                cacheTime = re.search(r"appeared\ on\ (.+?GMT)", cacheTime).group(1)
                cacheTime = int(time.mktime(datetime.datetime.strptime(cacheTime, "%b %d, %Y %H:%M:%S GMT").timetuple()))
        except:
            cacheTime = "undefined"
        
        title = soup.find("h2").text.replace("\n", "")
        title = re.sub(r"^\ +", "", title)
        title = re.sub(r"\ +$", "", title)

        content = []

        flarumContent = soup.find("noscript", {"id": "flarum-content"})

        postBody = flarumContent.findAll("div", {"class": "Post-body"})
        postAuthor = list(map(lambda x: x.find_previous_sibling("h3"), postBody))

        index = 0
        while(index < len(postBody)):
            body = postBody[index]

            body = body.decode_contents()
            body = re.sub(r"\ +", " ", body)
            author = postAuthor[index]
            author = author.text.replace(" ", "").replace("\n", "")

            temp = {
                "author": author,
                "body": body
            }

            content.append(temp)

            index += 1

        #### All data ####
        data = {
            "cacheTime": cacheTime,
            "baseUrl": baseUrl,
            "title": title,
            "content": content
        }

        # Translated: JSON
        with open(f"./translated/json/{filename}.json", "w") as f:
            json.dump(data, f, ensure_ascii=False)

        # Translated: Markdown
        # 採用 DFS 解析元素
        md = f"### {data['title']} `{data['baseUrl']}`\n\n"
        i = 0
        while i < len(data["content"]):
            element = BeautifulSoup(data["content"][i]["body"], "html.parser")
            md += f"\n***\n#### {data['content'][i]['author']}\n"
            mdParser(element)
            i += 1

        with open(f"./translated/markdown/{filename}.md", "w") as f:
            f.write(md)
