function doDateStr(dateStr) {
    let re = /(\d\d?) (\w{3}) (20\d{2})/;
    let arr = dateStr.match(re);
    document.write( `${arr[1]} ${arr[2]} ${arr[3]}` );
}

// function toggleOrigLangs() {
//     document.querySelector('body').classList.toggle('show-orig-langs')
// }