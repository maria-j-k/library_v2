document.addEventListener("DOMContentLoaded", function(){
let inp = document.querySelector('.title')


inp.addEventListener('change', e => {
    console.log("input event")
    console.log(inp.value)
})


})
