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
            let targetUrl = $SCRIPT_ROOT +'/autocomplete_' + targ
            if (targ == "serie"){
                let publisherId = splitUrl[splitUrl.length -2]
                $.getJSON(targetUrl ,{
                    q: request.term, publisher: publisherId 
                }, function(data) {
                    response(data.matching_results); 
                    console.log(data.matching_results)
                });
                
                }
            else {
                $.getJSON(targetUrl ,{
                    q: request.term, 
                }, function(data) {
                    response(data.matching_results); 
                    console.log(data.matching_results)
                });
            }
        },
        search: function(event, ui) {
            console.log('search')
            console.log(document.querySelector('#' + this.id + '_id').value)
            document.querySelector('#' + this.id + '_id').value = null
            console.log(document.querySelector('#' + this.id + '_id').value)
        },
        minLength: 3,
        focus: function(event, ui) {
		    event.preventDefault();
            console.log(ui.item.label);
//            $(this).val(ui.item.label);
				},
        select: function(event, ui) {
            event.preventDefault();
            console.log('label')
            console.log(ui.item.label)
            console.log('value')
            console.log(ui.item.value)
            $(this).val(ui.item.label);
//            $(this).prop("readonly", true);
            console.log('value before change')
            console.log(document.querySelector('#' + this.id + '_id').value)
            document.querySelector('#' + this.id + '_id').value = ui.item.value
            console.log('value after change')
            console.log(document.querySelector('#' + this.id + '_id').value)
            let field = $(this).attr('id')
            console.log('hej')
            console.log(field)
//            publisher_id = ui.item.value
            if (inputName){
                document.querySelector('.choice').classList.remove('invisible');
                document.querySelector('.submit').classList.add('invisible');
                }
        }
    });

// other

let clear = document.querySelectorAll('.clear')
let fakeBtns = document.querySelectorAll('.fake');
let toggleInc = document.querySelectorAll('.toggle-inc')
let changeOne = document.querySelector('#change-one')
let edit = document.querySelectorAll('.edit')

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
    clear.forEach(btn => {
        btn.addEventListener('click', e => {
            btn.closest('tr').querySelector('input').value = "";
            btn.closest('tr').querySelector('input').readOnly=false;
            document.querySelector('.choice').classList.add('invisible')
            document.querySelector('.submit').classList.remove('invisible')
//            btn.closest('tr').firstElementChild.lastElementChild.value = "";
    });
});
//    toggleInc.forEach(btn => {
//        btn.addEventListener('click', e => {
//            let thisUrl = btn.querySelector('a').href
//            $.ajax({
//                type: "POST",
//                url: thisUrl,
//                success: function(data){
//                    if (data.incorrect == true){
//                    btn.closest('td').innerText = 'True';
//                    btn.remove(); }
//                } 
//            });
//       }); 
//    });
//

})


