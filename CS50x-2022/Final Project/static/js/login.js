const registerForm = document.querySelector('#registerForm');
const loginForm = document.querySelector('#loginForm');

document.querySelector('.toCreate').addEventListener('click', () => {
    registerForm.style.display = "flex"
    loginForm.style.display = "none"
})

document.querySelector('.toSignin').addEventListener('click', () => {
    loginForm.style.display = "flex"
    registerForm.style.display = "none"
})