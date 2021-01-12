$(function() {
// autocomplete

    $(".publisher").autocomplete({
        source:function(request, response) {
            document.querySelector('#name_id').value = null
            $.getJSON($SCRIPT_ROOT + '/autocomplete_publisher',{
                q: request.term, 
            }, function(data) {
                response(data.matching_results); 
                console.log(data.matching_results)
            });
        },

        minLength: 3,
        focus: function(event, ui) {
		    event.preventDefault();
            $(this).val(ui.item.label);
				},
        select: function(event, ui) {
            event.preventDefault();
            $(this).val(ui.item.label);
            $(this).prop("readonly", true);
            let field = $(this).attr('id')
            document.querySelector('#name_id').value = parseInt(ui.item.value)
            publisher_id = ui.item.value
            document.querySelector('.choice').classList.remove('invisible')
            document.querySelector('.submit').classList.add('invisible')
        }
    });

// other

let clear = document.querySelectorAll('.clear')
let fakeBtns = document.querySelectorAll('.fake');
let toggleInc = document.querySelectorAll('.toggle-inc')
let changeOne = document.querySelector('#change-one')

    changeOne.addEventListener('click', e => {
            document.querySelector('.submit').classList.remove('invisible')
            })
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


