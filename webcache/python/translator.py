import json
import re
import sys
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

def DFSParser(element):
    global md

    if not hasChildren(element):
        if isinstance(element, Tag):
            md += f"{nospace(element.text)}"
        else:
            md += nospace(element)
        return
    else:
        for e in getChildrenList(element):
            if isinstance(element, Tag):
                if(isLinkImage(e)):
                    md += f"![]({getImageUrl(e)})"
                elif(e.name == "a"):
                    if(e.has_attr("class") and e["class"][0] == "PostMention"):
                        md += f"[回覆：{e.text}](#)\n"
                    else:
                        md += f"[{e.text}]({getLinkUrl(e)})"
                elif(e.name == "p"):
                    DFSParser(e)
                    md += "\n\n"
                elif(e.name == "iframe"):
                    if e.has_attr("src"):
                        src = e["src"]

                        if("www.youtube.com" in src):
                            src = src.replace("embed/", "watch?v=")
                            md += src
                        elif("twitter.min.html" in src):
                            # 推特原連結被 s9e 格式化了。僅知道 id 的狀況，不曉得如何反推原始連結
                            md += src
                        else:
                            md += src

                elif(e.name == "blockquote"):
                    md += "[quote]\n"
                    DFSParser(e)
                    md += "[/quote]\n\n"
                elif(e.name == "br"):
                    md += "\n"
                elif(e.name == "strong"):
                    md += "**"
                    DFSParser(e)
                    md += "**"
                else:
                    DFSParser(e)
            
            else:
                md += nospace(element)


originHtml = "./d"
translatedJson = "./translated/json"
translatedMarkdown = "./translated/markdown"
translatedHtml = "./translated/html"

files = [f for f in listdir(originHtml) if isfile(join(originHtml, f))]

filenames = list(map(lambda x: x.split(".")[0], files))

Path("./translated/json").mkdir(parents=True, exist_ok=True)
Path("./translated/markdown").mkdir(parents=True, exist_ok=True)
Path("./translated/html").mkdir(parents=True, exist_ok=True)

index = 1
if not Path(f"./translated/json/{filenames[index]}").is_file():
    raw = ""
    # with open(f"{originHtml}/{filenames[index]}.html", "r", encoding="utf-8") as file:
    # 僅測試用
    with open(f"{originHtml}/60866.html", "r", encoding="utf-8") as file:
        raw = file.read()

    soup = BeautifulSoup(raw, "html.parser")

    baseUrl = soup.find("base")["href"]
    title = soup.find("title").text.replace("- 卡特 Kater", "").replace("\n", "")
    title = re.sub(r"\ +", " ", title)

    content = []

    flarumContent = soup.find("noscript", {"id": "flarum-content"})

    postAuthor = flarumContent.findAll("h3")
    postBody = flarumContent.findAll("div", {"class": "Post-body"})

    index = 0
    while(index < len(postAuthor)):
        body = postBody[index]

        body = body.decode_contents().replace("\n", "")
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
        "baseUrl": baseUrl,
        "title": title,
        "content": content
    }

    # Translated: JSON
    with open("data.json", "w") as f:
        json.dump(data, f, ensure_ascii=False)

    # Translated: Markdown
    # 採用 DFS 解析元素
    md = f"### {data['title']} `{data['baseUrl']}`\n\n"
    i = 0
    while i < len(data["content"]):
        element = BeautifulSoup(data["content"][i]["body"], "html.parser")
        md += f"\n***\n#### {data['content'][i]['author']}\n"
        DFSParser(element)
        i += 1

    with open("data.md", "w") as f:
        f.write(md)

    # Translated: HTML
