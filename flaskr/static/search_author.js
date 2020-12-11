document.addEventListener("DOMContentLoaded", function(){
    let authorInput = document.querySelector('#name')
//    authorInput.addEventListener("beforeinput", e => {
    authorInput.addEventListener("keyup", e => {
        console.log(this)
    })
})
