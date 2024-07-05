document.addEventListener('DOMContentLoaded', function() {
    document.querySelector("#change-view-register").addEventListener('click', () => change_view("register"));
    document.querySelector("#change-view-login").addEventListener('click', () => change_view("login"));
});

function change_view(state) {
    if (state === "register") {
        document.querySelector(".register-view").style.display = "none";
        document.querySelector(".login-view").style.display = "block";
    } else {
        document.querySelector(".login-view").style.display = "none";
        document.querySelector(".register-view").style.display = "block";
    }
}
