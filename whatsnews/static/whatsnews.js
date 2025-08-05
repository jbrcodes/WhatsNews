/* /whatsnews/static/whatsnews.js */

function doDateStr(isoDateStr) {
    let re = /(\d\d?) (\w{3}) (20\d{2})/;
    let arr = isoDateStr.match(re);
    let myDateStr = `${arr[1]} ${arr[2]} ${arr[3]}`

    let span = document.createElement('span');
    span.textContent = myDateStr;
    document.currentScript.after(span);
}

function toggleOrigLang(siteId) {
    for (let elem of document.querySelectorAll(`#site_${siteId} .orig-lang`)) {
        elem.classList.toggle('show-orig');
    }
    let but = document.getElementById(`but_${siteId}`);
    but.textContent = (but.textContent == 'show') ? 'hide' : 'show';
}

function ecorreo() {
	let addr = "in" + "fo" + String.fromCharCode(32 * 2) + "jb";
	addr += "rcodes" + ".c";
	addr += 'om';
	let href = "mai" + "lto:" + addr;

    let link = document.createElement('a');
    link.textContent = addr;
    link.href = href;
    document.currentScript.after(link);
}