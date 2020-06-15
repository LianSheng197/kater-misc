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

msg("就緒");