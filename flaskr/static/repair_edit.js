$(function() {
// autocomplete

let splitUrl = window.location.pathname.split('/')
let targ = splitUrl[splitUrl.length -1] // jaki obiekt ma być edytowany - do urla
let inputName = document.querySelector('#input-name') // label w formularzu
    if (inputName){
    inputName.innerText = targ.charAt(0).toUpperCase() + targ.slice(1);
    }
    $(".searchItem").autocomplete({
        source:function(request, response) {
            if (targ == "serie"){
                let targetUrl = $SCRIPT_ROOT +'/autocomplete_' + targ
                let publisherId = splitUrl[splitUrl.length -2]
                $.getJSON(targetUrl ,{
                    q: request.term, publisher: publisherId 
                }, function(data) {
                    response(data.matching_results); 
                    console.log(data.matching_results)
                });
                }
            else if (targ == "edit"){
                let targetUrl = $SCRIPT_ROOT +'/autocomplete_person'
                $.getJSON(targetUrl ,{
                    q: request.term, 
                }, function(data) {
                    response(data.matching_results); 
                    console.log(data.matching_results)
                });
            }
            else {
                let targetUrl = $SCRIPT_ROOT +'/autocomplete_' + targ
                $.getJSON(targetUrl ,{
                    q: request.term, 
                }, function(data) {
                    response(data.matching_results); 
                    console.log(data.matching_results)
                });
            }
        },
        search: function(event, ui) {
            console.log(document.querySelector('#' + this.id + '_id').value)
            document.querySelector('#' + this.id + '_id').value = null // przestawia wartość odpowiadającgo polu pola id na zero - resetuje zaczytane z bazy id obiektu
            console.log(document.querySelector('#' + this.id + '_id').value)
        },
        minLength: 3,
        focus: function(event, ui) {
		    event.preventDefault();
				},
        select: function(event, ui) {
            event.preventDefault();
            $(this).val(ui.item.label);
            document.querySelector('#' + this.id + '_id').value = ui.item.value
            let field = $(this).attr('id')
            if (inputName){
                document.querySelector('.choice').classList.remove('invisible');
                document.querySelector('.submit').classList.add('invisible');
                }
        }
    });

// other

let fakeBtns = document.querySelectorAll('.fake');
let changeOne = document.querySelector('#change-one')
let edit = document.querySelectorAll('.edit')
let merge = document.querySelector('.merge')

    if (merge){
        merge.addEventListener('click', e => {
            console.log(document.querySelector('#name_id').value)
            console.log(document.querySelector('#name').value)
        })
    }

    edit.forEach(btn => {
        btn.addEventListener('click', e => {
            let person = btn.closest('tr').querySelector('input').id
            let personId = document.querySelector('#' + person + '_id').value
            let targetUrl = window.location.origin + '/repair/persons/' + personId +'/edit'
            if (personId){
                window.open(targetUrl, "_blank")
            }
            else{
                console.log('trzeba coś zrobić, żeby ten guzik się nie wyświetlał...')
            }

        });
    })

    if (changeOne) { 
    changeOne.addEventListener('click', e => {
            document.querySelector('.submit').classList.remove('invisible');
            });
    };

    fakeBtns.forEach(btn => {
        btn.addEventListener('click', e => {
            e.preventDefault();
            })
        }
    );

})


