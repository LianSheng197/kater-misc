let pagePrevBtn = document.querySelector("#pagePrev");
let pageNextBtn = document.querySelector("#pageNext");
let pageNowSpan = document.querySelector("#pageNow");
let userTotalSpan = document.querySelector("#userTotal");
let pageTotalSpan = document.querySelector("#pageTotal");

let list = document.querySelector("tbody#userlist");

const limit = 500;
let nowPage = 1;
let nowTotalPage = 0;

async function renderContent(page = 1) {
    pagePrevBtn.setAttribute("disabled", "disabled");
    pagePrevBtn.classList.add("disabled");
    pageNextBtn.setAttribute("disabled", "disabled");
    pageNextBtn.classList.add("disabled");

    let _limit = limit;
    let _offset = (page - 1) * _limit;

    let baseURL = "https://script.google.com/macros/s/AKfycbxejz2Zqgt1VyWM-0jWXdi8fIj9Nff4fLEjSj8FDS-CBG9Bu5bE/exec";

    msg("正在請求資料");
    let rawData = await fetch(`${baseURL}?getHasAvatarUser=[${_limit}, ${_offset}]`).then(
        r => r.text()
    ).catch(
        e => "ERROR"
    );

    msg("正在繪製資料");
    if (rawData == "ERROR") {
        alert("取得資料時出錯，請再試一次");
    } else {
        let data = rawData.split(",");

        let html = "";
        let userTotal = data[4 * 2 - 1];
        let pageTotal = Math.ceil(userTotal / _limit);
        userTotalSpan.innerText = ` ${userTotal} `;
        pageTotalSpan.innerText = ` ${pageTotal} `;

        nowTotalPage = pageTotal;

        for (let i = 4; i < data.length; i += 4) {
            html += `<tr><td>${data[i]}</td><td><img src="${data[i+2]}"></img></td><td>${data[i+1]}</td></tr>`;
        }

        list.innerHTML = html;
    }

    msg("就緒");

    if (nowPage > 1) {
        pagePrevBtn.removeAttribute("disabled");
        pagePrevBtn.classList.remove("disabled");
    }
    if (nowTotalPage > 1 && nowPage < nowTotalPage) {
        pageNextBtn.removeAttribute("disabled");
        pageNextBtn.classList.remove("disabled");
    }

    pageNowSpan.innerText = nowPage;
}

function pageNextFunc() {
    if (nowPage >= nowTotalPage) {
        return;
    } else {
        renderContent(++nowPage);
    }
}

function pagePrevFunc() {
    if (nowPage <= 1) {
        return;
    } else {
        renderContent(--nowPage);
    }
}

let target = document.querySelector("div#pageControl");
let offsetTarget = target.offsetTop;
let navbarHeight = 60;
function scrollAlign() {
    let nowTop = document.documentElement.scrollTop;

    if(nowTop > offsetTarget - navbarHeight){
        target.style.position = "fixed";
        target.style.top = `${navbarHeight}px`;
        target.style.backgroundColor = "#cbeaffbb";
    } else {
        target.style.position = "absolute";
        target.style.top = `${offsetTarget}px`;
        target.style.backgroundColor = "#cbeaff44";
    }
}

document.addEventListener('scroll', scrollAlign);

pagePrevBtn.addEventListener("click", pagePrevFunc);
pageNextBtn.addEventListener("click", pageNextFunc);

renderContent();