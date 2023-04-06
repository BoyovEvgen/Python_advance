const URL = window.location.href.split('/')
const URL_update = URL.slice(0, -1).join('/') + '/stats/virtual_memory'


function update_stat() {
    fetch(URL_update)
    .then(response => response.json())
    .then(data => {
        const percent = data.percent
        document.getElementsByClassName('data').item('width').innerHTML = percent
        document.querySelector('.bar').style.transform = `translate(${percent}%, 0)`

    })
}

function init (){
    setInterval(update_stat, 1000)
}

init()