// 觸發導入片段檔的事件註冊
document.querySelectorAll("a[data-link]").forEach(each => {
    each.addEventListener("click", () => {
        let link = each.getAttribute("data-link");
        insertPartialHTML(link);
    });
});

// 引入外部片段檔
async function insertPartialHTML(filename) {
    let content = document.querySelector("div#content");
    let targetFile = `pages/${filename}.html`;

    let html = await fetch(targetFile).then(
        r => r.text()
    );

    // 添加非 script 的 HTML
    content.innerHTML = html.replace(/<script>[^]+?<\/script>/, "");


    // 添加 script
    let script = html.match(/<script>([^]+?)<\/script>/);

    if (script != null) {
        let s = document.createElement('script');
        s.type = "text/javascript";

        s.innerHTML = `
        (function(){
            ${script[1]}
        })();
        `;
        content.appendChild(s);
    }

    // 添加 script[src]
    let matches = html.match(/<script.+?src=["'].+?["'].*?><\/script>/g);

    if (matches != null) {
        matches.forEach(async each => {
            let target = each.match(/<script.+?src=["'](.+?)["'].*?><\/script>/);

            let s = document.createElement('script');
            s.type = "text/javascript";

            let script = await fetch(target[1]).then(
                r=>r.text()
            );
            
            s.innerHTML = `
            (function(){
                ${script}
            })();
            `;

            content.appendChild(s);
        });
    }
}

insertPartialHTML("help");