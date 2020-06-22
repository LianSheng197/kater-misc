// 導航欄訊息提示
function msg(string){
    let d = new Date();
    let hh = `0${d.getHours()}`.substr(-2);
    let mm = `0${d.getMinutes()}`.substr(-2);
    let ss = `0${d.getSeconds()}`.substr(-2);
    let time = `${hh}:${mm}:${ss}`;

    let msgArea = document.querySelector("nav#navbar div.right");
    msgArea.innerText = `[${time}] ${string}`;
    console.log(`[${time}] ${string}`);
}

function dateFormat(d){
    let yyyy = d.getFullYear();
    let MM = `0${d.getMonth()+1}`.substr(-2);
    let dd = `0${d.getDate()}`.substr(-2);
    let hh = `0${d.getHours()}`.substr(-2);
    let mm = `0${d.getMinutes()}`.substr(-2);
    let ss = `0${d.getSeconds()}`.substr(-2);
    let datetime = `${yyyy}/${MM}/${dd} ${hh}:${mm}:${ss}`;
    
    return datetime;
}


msg("就緒");

// footer
document.querySelector("span#version").innerText = "v0.7.0";
document.querySelector("span#lastModified").innerText = dateFormat(new Date(document.lastModified));