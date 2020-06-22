let condition = document.querySelector("div#condition input[type=text]");
let searchBtn = document.querySelector("div#condition input[type=button]");
let downloadBtn = document.querySelector("input#download");

let pagePrevBtn = document.querySelector("#pagePrev");
let pageNextBtn = document.querySelector("#pageNext");
let pageNowSpan = document.querySelector("#pageNow");
let userTotalSpan = document.querySelector("#userTotal");
let pageTotalSpan = document.querySelector("#pageTotal");

let nowCondition = "";
let nowPage = 0;
let nowTotalPage = 0;

// 查詢按鈕：點擊事件
searchBtn.addEventListener("click", translate);

// 下載按鈕：點擊事件
downloadBtn.addEventListener("click", downloadImage);

// 快速新增按鈕：非數字
document.querySelectorAll("div.fast2add span:not(.number)").forEach(each => {
    each.addEventListener("click", () => {
        condition.value += ` ${each.innerText} `;
    });
});

// 快速新增按鈕：數字
document.querySelectorAll("div.fast2add span.number").forEach(each => {
    each.addEventListener("click", () => {
        condition.value += each.innerText;
    });
});

function translate() {
    msg("正在檢查格式");

    const FIELD_HUMAN = {
        UID: "A",
        總推數: "C",
        改名次數: "F",
        討論數: "G",
        貼文數: "H",
        平均每篇貼文推數: "(C/H)",
        且: "AND",
        或: "OR"
    };

    let translated = condition.value;
    let notEmpty = translated.match(/[^\ ]/) != null ? true : false;

    if (notEmpty) {
        for (let [key, value] of Object.entries(FIELD_HUMAN)) {
            translated = translated.replace(new RegExp(key, "g"), value);
        }

        translated = `WHERE ${translated}`;
        translated = translated.replace(/\ +/g, " ");

        // 基本檢查：只能抓出非法字元，無法檢查結構
        let checkLegal = translated.match(/([^\ \/\-\.A-Z0-9<>=!\(\)])/);

        if (checkLegal != null) {
            condition.focus();
            alert(`過濾條件錯誤：含有非法字元 "${checkLegal[1]}"`);
            msg("就緒");
            return;
        }
    } else {
        translated = "";
    }

    console.log(translated);
    nowCondition = translated;
    renderContent(translated);
}


async function renderContent(condition, page = 0) {
    searchBtn.setAttribute("disabled", "disabled");
    searchBtn.classList.add("disabled");
    pagePrevBtn.setAttribute("disabled", "disabled");
    pagePrevBtn.classList.add("disabled");
    pageNextBtn.setAttribute("disabled", "disabled");
    pageNextBtn.classList.add("disabled");

    let count = 1;
    let orderColumn = document.querySelector("div#orderColumn select").value;
    let orderType = document.querySelector("div#orderType select").value == "asc" ? "" : "-";
    let _sortBy = `${orderType}${orderColumn}`;
    let _limit = document.querySelector("div#limit select").value;
    let _condition = condition;
    let _offset = page * _limit;

    let baseURL = "https://script.google.com/macros/s/AKfycbxejz2Zqgt1VyWM-0jWXdi8fIj9Nff4fLEjSj8FDS-CBG9Bu5bE/exec";

    msg("正在請求資料");
    let rawData = await fetch(`${baseURL}?rankSortBy=${_sortBy}&rankLimit=${_limit}&rankOffset=${_offset}&rankCondition=${_condition}`).then(
        r => r.text()
    ).catch(
        e => "ERROR"
    );

    msg("正在繪製資料");
    if (rawData == "ERROR") {
        alert("取得資料時出錯，請再試一次");
    } else if (rawData == "#VALUE!") {
        alert("取得資料失敗，請檢查過濾條件格式");
    } else {
        // 背景
        makeSVG("rect", {
            fill: "#e6fbff",
            width: "100%",
            height: "100%"
        });

        // 欄位名稱
        makeSVG("text", {
            text: "排名",
            fill: "black",
            x: 10,
            y: 40
        });
        makeSVG("text", {
            text: "縮圖",
            fill: "black",
            x: 80,
            y: 40
        });
        makeSVG("text", {
            text: "（UID）目前暱稱",
            fill: "black",
            x: 150,
            y: 40
        });
        makeSVG("text", {
            text: "總推數",
            fill: "black",
            x: 450,
            y: 40
        });
        makeSVG("text", {
            text: "改名次數",
            fill: "black",
            x: 520,
            y: 40
        });
        makeSVG("text", {
            text: "總討論",
            fill: "black",
            x: 590,
            y: 40
        });
        makeSVG("text", {
            text: "總貼文",
            fill: "black",
            x: 660,
            y: 40
        });
        makeSVG("text", {
            text: "平均每篇貼文推數",
            fill: "black",
            x: 730,
            y: 40
        });

        let data = rawData.split(",");

        document.querySelector("svg").setAttribute("height", (data.length / 9) * 50 + 20);

        if (window.innerWidth >= 768) {
            document.querySelector("svg").setAttribute("width", document.querySelector("#svgContainer").clientWidth);
        }

        let userTotal = data[9 * 2 - 1];
        let pageTotal = Math.ceil(userTotal / _limit);
        userTotalSpan.innerText = ` ${userTotal} `;
        pageTotalSpan.innerText = ` ${pageTotal} `;

        nowTotalPage = pageTotal;

        // 跳過第一列（標題）
        for (let i = 9; i < data.length; i += 9) {
            let y = 40 + 50 * count;
            let username = `（${data[i]}） ${data[i+1]}`;

            // 暫時無法排除 CORS 錯誤
            // let avatar = data[i + 6] != undefined ? toDataURL(data[i + 6], "png") : "";
            let avatar = data[i + 6] != undefined ? data[i + 6] : "";

            if (measureText(username) >= 290) {
                username = username.substr(0, username.length - 2);
                while (measureText(username + "...") >= 290) {
                    username = username.substr(0, username.length - 2);
                }

                username += "...";
            }

            makeSVG("text", {
                text: count + (_offset),
                fill: "black",
                x: 10,
                y: y
            });

            makeSVG("image", {
                "xlink:href": avatar,
                width: "50px",
                height: "50px",
                x: 80,
                y: y - 30
            });

            makeSVG("text", {
                text: username,
                fill: "black",
                x: 150,
                y: y
            });

            makeSVG("text", {
                text: data[i + 2],
                fill: "black",
                x: 450,
                y: y
            });

            makeSVG("text", {
                text: data[i + 3],
                fill: "black",
                x: 520,
                y: y
            });

            makeSVG("text", {
                text: data[i + 4],
                fill: "black",
                x: 590,
                y: y
            });

            makeSVG("text", {
                text: data[i + 5],
                fill: "black",
                x: 660,
                y: y
            });

            makeSVG("text", {
                text: parseFloat(data[i + 7]).toFixed(3).toString(),
                fill: "black",
                x: 730,
                y: y
            });

            count++;
        }
    }

    msg("就緒");
    searchBtn.removeAttribute("disabled");
    searchBtn.classList.remove("disabled");

    if (nowPage > 1) {
        pagePrevBtn.removeAttribute("disabled");
        pagePrevBtn.classList.remove("disabled");
    }
    if (nowTotalPage > 1) {
        pageNextBtn.removeAttribute("disabled");
        pageNextBtn.classList.remove("disabled");
    }

    pageNowSpan.innerText = nowPage + 1;

    // 暫時無法排除 CORS 錯誤
    // downloadBtn.style.display = "initial";
}

function pageNextFunc() {
    if (nowPage >= nowTotalPage) {
        return;
    } else {
        renderContent(nowCondition, ++nowPage);
    }
}

function pagePrevFunc() {
    if (nowPage <= 1) {
        return;
    } else {
        renderContent(nowCondition, --nowPage);
    }
}

pagePrevBtn.addEventListener("click", pagePrevFunc);
pageNextBtn.addEventListener("click", pageNextFunc);

// 判斷文字寬度
function measureText(pText, pFontSize = "1rem") {
    let lDiv = document.createElement('div');

    document.body.appendChild(lDiv);

    lDiv.style.fontSize = pFontSize;
    lDiv.style.position = "absolute";
    lDiv.style.left = -1000;
    lDiv.style.top = -1000;

    lDiv.innerHTML = pText;

    let lResult = {
        width: lDiv.clientWidth,
        height: lDiv.clientHeight
    };

    document.body.removeChild(lDiv);
    lDiv = null;

    return lResult.width;
}

function toDataURL(src, outputFormat) {
    let img = new Image();

    img.onload = function () {
        let canvas = document.createElement('CANVAS');
        let ctx = canvas.getContext('2d');
        let dataURL;
        canvas.height = this.naturalHeight;
        canvas.width = this.naturalWidth;
        ctx.drawImage(this, 0, 0);
        dataURL = canvas.toDataURL(outputFormat);
        return dataURL;
    };

    img.onerror = function () {
        return "data:image/png;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";
    };

    img.crossOrigin = "";
    img.src = src;
}

// 將 SVG 結果圖下載成 JPG 格式圖片
function downloadImage() {
    let svg = document.querySelector("svg").outerHTML;
    if (svg) {
        svg = svg.replace(/\r?\n|\r/g, '').trim();
    }
    let canvas = document.createElement('canvas');

    canvg(canvas, svg);

    let link = document.createElement('a');
    link.download = `${Date.now()}.jpg`;
    link.href = canvas.toDataURL("image/jpeg", 0.7);
    link.click();
}