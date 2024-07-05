document.addEventListener('DOMContentLoaded', function() {
    document.querySelector(".features").addEventListener('click', () => scroll_to_bottom());
});

function scroll_to_bottom() {
    window.scrollTo({
        top: document.body.scrollHeight,
        left: 0,
        behavior: "smooth"
      })
}