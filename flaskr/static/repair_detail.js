$(function() {

let fakeBtns = document.querySelectorAll('.fake');
let edit = document.querySelectorAll('.edit')
let editPer = document.querySelectorAll('.edit-p')

    fakeBtns.forEach(btn => {
        btn.addEventListener('click', e => {
            e.preventDefault();
            })
        }
    );
    
    edit.forEach(btn => {
        btn.addEventListener('click', e => {
//            let baseHref = btn.querySelector('a').href
            let model = btn.closest('tr').querySelector('input').id
            if (model == "serie"){
                let pubId = document.querySelector('#publisher_id').value
                let targetUrl = window.location.pathname + '/' +  pubId + '/' + model
                window.open(targetUrl, "_self")
            }
            else {
            let targetUrl = window.location.pathname + '/' + model
            window.open(targetUrl, "_self")
            }
        })
    })

    editPer.forEach(btn => {
        btn.addEventListener('click', e => {
            let model = btn.closest('tr').querySelector('th').innerText.toLowerCase()
            let targetUrl = window.location.pathname + '/' + model + '/person'
            window.open(targetUrl, "_self")
        })

    })
})


