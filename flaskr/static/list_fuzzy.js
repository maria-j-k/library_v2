$(function() {
// other

let fakeBtns = document.querySelectorAll('.fake');
let searchInp = document.querySelector('.search-input')
let searchBtn = document.querySelector('button.search')
let searchLink = document.querySelector('#search-link')
let toggleInc = document.querySelectorAll('.toggle-inc')


    fakeBtns.forEach(btn => {
        btn.addEventListener('click', e => {
            e.preventDefault();
            })
        }
    );
    if (searchBtn){
        searchBtn.addEventListener('click', e => {
            let newHref = searchLink.href + searchInp.value;
            searchLink.setAttribute('href', newHref);
            window.open(searchLink.href, "_self");
            }
        );
    }
    toggleInc.forEach(btn => {
        btn.addEventListener('click', e => {
            let thisUrl = btn.querySelector('a').href
            console.log(thisUrl)
            $.ajax({
                type: "POST",
                url: thisUrl,
                success: function(data){
                    if (data.incorrect == true){
                    btn.closest('td').innerText = 'True';
                    btn.remove(); }
                } 
            });
       }); 
    });


})


