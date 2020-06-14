function makeSVG(tag, attrs) {
    var el = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (var k in attrs) {
        if (k == "xlink:href") {
            el.setAttributeNS("http://www.w3.org/1999/xlink", "href", attrs[k]);
        } else if (k == "text") {
            el.textContent = attrs[k];
        } else {
            el.setAttribute(k, attrs[k]);
        }
    }

    document.querySelector("svg").appendChild(el);
}