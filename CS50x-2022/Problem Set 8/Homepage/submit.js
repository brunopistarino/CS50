const form = document.querySelector('#form')
const inputFn = document.querySelector('#input-fn')
const inputLn = document.querySelector('#input-ln')
const inputEa = document.querySelector('#input-ea')
const inputM = document.querySelector('#input-m')

form.addEventListener("submit", function(e){
    e.preventDefault();
    if (inputFn.value && inputLn.value && inputEa.value && inputM.value) {
        alert("Form submitted!")
    } else {
        alert("Entries cannot be empty")
    }
});