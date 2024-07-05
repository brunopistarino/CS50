const nav = document.querySelector('nav')

window.addEventListener("scroll", function(){
    if(window.scrollY<60){
        nav.classList.add("top");
    } else {
        nav.classList.remove("top");
    }
});