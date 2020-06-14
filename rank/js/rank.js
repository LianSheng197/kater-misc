let condition = document.querySelector("div#condition input[type=text]");
let searchBtn = document.querySelector("div#condition input[type=button]");

// 查詢按鈕：點擊事件
searchBtn.addEventListener("click", translate);

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
    const FIELD = {
        uid: "A",
        username: "B",
        points: "C",
        changeNameCount: "F",
        discussions: "G",
        posts: "H",
        avatarUrl: "I",
        rate: "(C/H)"
    };

    const FIELD_HUMAN = {
        UID: "A",
        總推數: "C",
        改名次數: "F",
        討論數: "G",
        貼文數: "H",
        "貼文數 / 總推數": "(C/H)",
        且: "AND",
        或: "OR"
    };

    let translated = condition.value;
    let notEmpty = translated.match(/[^\ ]/) != null ? true : false;

    if (notEmpty) {
        for (let [key, value] of Object.entries(FIELD_HUMAN)) {
            translated = translated.replace(new RegExp(key, "g"), value);
        }

        translated = translated.replace(/\ +/g, " ");

        // 基本檢查：只能抓出非法字元，無法檢查結構
        let checkLegal = translated.match(/([^\ A-Z0-9<>=!\(\)])/);

        if (checkLegal != null) {
            condition.focus();
            alert(`過濾條件錯誤：含有非法字元 "${checkLegal[1]}"`);
            return;
        }
    } else {
        translated = "";
    }

    console.log(translated);
    renderContent(condition);
}


async function renderContent(condition, offset = 0) {
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
        text: "目前暱稱",
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
        text: "總推數 / 貼文",
        fill: "black",
        x: 730,
        y: 40
    });

    let count = 2;
    let orderColumn = document.querySelector("div#orderColumn select").value;
    let orderType = document.querySelector("div#_orderType select").value == "asc" ? "" : "-";
    let _sortBy = `${orderType}${orderColumn}`;
    let _limit = document.querySelector("div#limit select").value;
    let _condition = condition;
    let _offset = offset;

    let baseURL = "https://script.google.com/macros/s/AKfycbxejz2Zqgt1VyWM-0jWXdi8fIj9Nff4fLEjSj8FDS-CBG9Bu5bE/exec";

    let rawData = await fetch(`${baseURL}?rankSortBy=${_sortBy}&rankLimit=${_limit}&rankOffset=${_offset}&rankCondition=${_condition}`).then(
        r => r.text()
    ).catch(
        e => "ERROR"
    );

    if (rawData == "ERROR") {
        alert("取得資料時出錯，請再試一次");
    } else {
        let data = rawData.split(",");
    }
}
// makeSVG("image", {
//     "xlink:href": "https://kater.me/assets/avatars/lK37NSjp4n45nrh8.png",
//     width: "50px",
//     height: "50px",
//     x: "10",
//     y: "10"
// });

// makeSVG("text", {
//     text: "熱狗",
//     fill: "black",
//     x: "70",
//     y: "40"
// });