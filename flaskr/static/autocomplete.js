//document.addEventListener("DOMContentLoaded", function() {  
$(function() {
/*
 * autocomplete functions
 * */
    $(".creator").autocomplete({
        source:function(request, response) {
            $.getJSON($SCRIPT_ROOT + '/autocomplete_person',{
                q: request.term, 
            }, function(data) {
                response(data.matching_persons); 
                console.log(data.matching_persons)
            });
        },

        minLength: 3,
        focus: function(event, ui) {
		event.preventDefault();
        $(this).val(ui.item.label);
				},
        select: function(event, ui) {
            event.preventDefault();
            let nameId = $(this).attr('id').split('-')
            let idsId = nameId[0]+'-'+nameId[1]+'-id_'
            $(this).val(ui.item.label);
//            let thisInputId = $(this).attr('id')
//            $("#" + thisInputId + "_val").val(ui.item.value);
            $('#' + idsId).val(parseInt(ui.item.value));
//            console.log(`this: ${$(this).val()}`)
//            console.log($('#'+idsId))
//            console.log($('#'+idsId).val())
//            console.log(`ui item label: ${ui.item.label}`)
//            console.log(`ui item value: ${ui.item.value}`)
//            console.log(nameId)
//            console.log(idsId)
////            console.log(`thisInputId: ${thisInputId}`)
        }
    });


function findCity(publisher) {
    $.get($SCRIPT_ROOT + '/db_pub_place', {
        q: publisher,
    }).done(function(response) {
       $('#published-city').val(response.city)
        publisher.city = response.city
    $("#published-city").prop("readonly", true);
    $("#published-publisher_name").prop("readonly", true);
    }).fail(function() {
        console.log('nieudane')
    });
};


    $(".publisher").autocomplete({
        source:function(request, response) {
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
            $('#published-id_').val(parseInt(ui.item.value));
//            console.log(`this: ${$(this).val()}`)
//            console.log($('#published-id_').val())
//            console.log(`ui item label: ${ui.item.label}`)
//            console.log(`ui item value: ${ui.item.value}`)
            publisher_id = ui.item.value
//            console.log(`publisher: ${publisher_id}`)
//            findCity(publisher_id)
        }
    });


    $(".serie").autocomplete({
        source:function(request, response) {
            if (publisher_id){
            $.getJSON($SCRIPT_ROOT + '/autocomplete_serie',{
                q: request.term, publisher: publisher_id 
            }, function(data) {
                response(data.matching_results); 
                console.log(publisher_id)
                console.log(data.matching_results)
            });
            }
        },

        minLength: 3,
        focus: function(event, ui) {
		event.preventDefault();
        $(this).val(ui.item.label);
				},
        select: function(event, ui) {
            event.preventDefault();
            $(this).val(ui.item.label);
            $('#published-s_id_').val(parseInt(ui.item.value));
//            console.log(`this: ${$(this).val()}`)
//            console.log($('#published-s_id_').val())
//            console.log(`ui item label: ${ui.item.label}`)
//            console.log(`ui item value: ${ui.item.value}`)
        }
    });

let publisher_id = null
let clear = document.querySelectorAll('.clear')
let serieInp = document.querySelector("#serie")
serieInp.addEventListener('click', e => {
    if (!document.querySelector("#publisher_name").value){
        alert("You must fill publisher field first.")
    }
})


clear.forEach(btn => {
    btn.addEventListener('click', e => {
    let outer = btn.closest('div');
    let inputs = btn.closest('div').querySelectorAll('input')
        inputs.forEach(inp => {
            inp.value = "";
            inp.readOnly = false;
            publisher_id = null
        })
    });
});

/*
 *switching steps 
 **/

//functions
const moveForward = function(btn){
    let currentStep = btn.closest('div.step');
    let nextStep = currentStep.nextElementSibling;
    currentStep.classList.add('invisible');
    nextStep.classList.remove('invisible');
};

const moveBackwards = function(btn){
    let currentStep = btn.closest('div.step');
    let prevStep = currentStep.previousElementSibling;
    currentStep.classList.add('invisible');
    prevStep.classList.remove('invisible');
}

// variables
let nextBtns = document.querySelectorAll('button.step--next');
let prevBtns = document.querySelectorAll('button.step--prev');
let fakeBtns = document.querySelectorAll('.fake');


//events
fakeBtns.forEach(btn => {
    btn.addEventListener('click', e => {
        e.preventDefault();
    });
});

nextBtns.forEach(btn => {
    btn.addEventListener('click', e => {
        moveForward(btn);
    });
});

prevBtns.forEach(btn => {
    btn.addEventListener('click', e => {
        moveBackwards(btn);
    });
});



/* 
 *Step one: addRole, addPerson
 * 
 *
 *TODO przycisk do usuwania niepotrzebnych okienek, dodający z powrotem klasę 'invisible' do add-person
 *TODO validacja: 
 * jeśli dam przy add person, nie będzie się walidowac ostatnia.
 * add person - dodaje do listy 'authors' etc kolejne nazwiska
 * Przy ostatnim nazwisku zrobić event listener do inputa i dodać nazwisko
 * jeśli nazwisko się powtarza: 
 * alert - ta osoba już jest
 * */

//functions
const newPerson = function(btn)  {
    let person = btn.closest('div').querySelector('.active')
    let nextPerson = btn.closest('div').querySelectorAll('.invisible')
    if (nextPerson.length == 1){
    btn.classList.add('invisible')
    }
    if (person.querySelector('input').value){ 
        person.classList.remove('active')
        nextPerson[0].classList.add('active')
        nextPerson[0].classList.remove('invisible')
    }
    else {
        alert('Before adding a new person, please enter a value!')
    };
}




//variables
let addRole = document.querySelectorAll('.add-role button');
let addPerson = document.querySelectorAll('.add-person');
let authors = document.querySelectorAll('#authors .creator')
//events

addRole.forEach(btn=> {
    btn.addEventListener('click', e => {
        console.log(btn.id)
//        let role = $('.'+btn.id)
//        let role = document.querySelector('.'+btn.id)
        let role = document.querySelector(`.${btn.id}`)
        console.log(role)
        role.classList.remove('invisible');
        btn.classList.add('invisible');
    });
});

addPerson.forEach(btn => {
    btn.addEventListener('click', e => {
        newPerson(btn)
    });
});

authors.forEach(inp => {
    inp.addEventListener('change', e => {
        console.log('authors event')
        console.log(inp.value)
    })
});














})
