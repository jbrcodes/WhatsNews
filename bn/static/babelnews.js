/* /bn/static/babelnews.js */

function doDateStr(isoDateStr) {
    let span = document.createElement('span');
    span.textContent = dayjs(isoDateStr).format('D MMM YYYY');
    document.currentScript.after(span);
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

function showLang(event, siteId) {
    let lang = event.target.value;
    for (let elem of document.querySelectorAll(`#site_${siteId} .lang-src`)) {
        elem.style.display = (lang === 'src') ? 'block' : 'none';
    }
    for (let elem of document.querySelectorAll(`#site_${siteId} .lang-dest`)) {
        elem.style.display = (lang === 'src') ? 'none' : 'block';
    }
}