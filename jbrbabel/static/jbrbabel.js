function foo(dateStr) {
    let dateObj = new Date(dateStr);
    document.write( dateObj.toLocaleString() );
}

function showOrigLang(divId) {
    let elem = document.getElementById(divId);
    elem.style.display = (elem.style.display === 'none') ? 'block' : 'none';
}