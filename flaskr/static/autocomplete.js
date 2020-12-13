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
            console.log(`this: ${$(this).val()}`)
            console.log($('#'+idsId).val())
            console.log(`ui item label: ${ui.item.label}`)
            console.log(`ui item value: ${ui.item.value}`)
            console.log(nameId)
            console.log(idsId)
//            console.log(`thisInputId: ${thisInputId}`)
        }
    });
    $(".title").autocomplete({
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
            $(this).val(ui.item.label);
            let thisInputId = $(this).attr('id')
            $("#" + thisInputId + "_val").val(ui.item.value);
        }
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
 *TODO przycisk do usuwania niepotrzebnych okienek, dodający z powrotem klasę 'invisible' do add-person, jeśli jej nie ma
 *TODO validacja: 
 * jeśli dam przy add person, nie będzie się walidowac ostatnia.
 * add person - dodaje do listy 'authors' etc kolejne nazwiska
 * Przy ostatnim nazwisku zrobić event listener do inputa i dodać nazwisko
 * jeśli nazwisko się powtarza: 
 * alert - ta osoba już jest
 * */

//functions



//variables
let addRole = document.querySelectorAll('.add-role');
let addPerson = document.querySelectorAll('.add-person');
//events

addRole.forEach(role=> {
    role.querySelector('button').addEventListener('click', e => {
        role.nextElementSibling.classList.remove('invisible');
        role.classList.add('invisible');
    });
});

addPerson.forEach(btn => {
    btn.addEventListener('click', e => {
        let nextPerson = btn.closest('div').querySelector('.invisible') 
        let person = nextPerson.previousElementSibling.querySelector('input')
        console.log(person.value)
        if (person.value != ''){ 
            nextPerson.classList.remove('invisible')
        if (!nextPerson.nextElementSibling.classList.contains('invisible')) {
            btn.classList.add('invisible')
        };
        }
        else {
            alert('Before adding a new person, please enter a value!')
        }
    });
});
















})
