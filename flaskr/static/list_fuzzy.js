$(function() {
let fakeBtns = document.querySelectorAll('.fake');
let searchInp = document.querySelector('.search-input')
let searchBtn = document.querySelector('button.search')
let searchLink = document.querySelector('#search-link')
    
    fakeBtns.forEach(btn => {
        btn.addEventListener('click', e => {
            e.preventDefault();
        })
    })
    searchBtn.addEventListener('click', e => {
        let newHref = searchLink.href + searchInp.value;
        searchLink.setAttribute('href', newHref);
        window.open(searchLink.href, "_self");
});


})
