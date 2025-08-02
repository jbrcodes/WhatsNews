function doDateStr(dateStr) {
    let re = /(\d\d?) (\w{3}) (20\d{2})/;
    let arr = dateStr.match(re);
    document.write( `${arr[1]} ${arr[2]} ${arr[3]}` );
}

function toggleOrigLang(siteId) {
    for (let elem of document.querySelectorAll(`#site_${siteId} .orig-lang`)) {
        elem.classList.toggle('show-orig');
    }
    let but = document.getElementById(`but_${siteId}`);
    but.textContent = (but.textContent == 'show') ? 'hide' : 'show';
}