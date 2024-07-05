const head = document.querySelector('.head')
const mainTitle = document.querySelector('.mainTitle');
const placeholder = document.querySelector('.placeholder');
const cardContainer = document.querySelector('.card-container');
const sectionContainer = document.querySelector('#section-container');
const modal = document.querySelector('#modal');
const cardPOST = document.querySelector('#cardPOST');
const sectionPOST = document.querySelector('#sectionPOST');
const sectionDELETE = document.querySelector('#sectionDELETE');
const currentSection = document.querySelector('#section-id');

const inputCardName = document.querySelector('#cardName')
inputCardName.addEventListener('input', () => {
    document.querySelector('.example-text').innerText = inputCardName.value;
})

const inputCardImg = document.querySelector('#link')
inputCardImg.addEventListener('input', () => {
    document.querySelector('.example-img').src = `https://s2.googleusercontent.com/s2/favicons?domain=${inputCardImg.value}&sz=256`;
})

fetch('/section', {method: 'GET'})
    .then(response => response.json())
    .then(data => loadSections(data));

function loadEmpty() {
    head.style.display = "none";
    cardContainer.style.display = "none";
    mainTitle.innerHTML = "";
    cardContainer.innerHTML = "";

    placeholder.style.display = "flex";
}

function loadCards(sectionId) {
    head.style.display = "flex"
    cardContainer.style.display = "flex"
    placeholder.style.display = "none"
    cardContainer.innerHTML = '<div class="card add-card" onclick="showModal(cardPOST)"><div>+</div></div>'

    fetch(`/card?id=${sectionId}`, {method: 'GET'})
        .then(response => response.json())
        .then(data => {
            mainTitle.innerHTML = `<span class="emoji">${data.emoji}</span>${data.name}`;
            data.links.forEach(link => {
                const a = document.createElement('a');
                const div = document.createElement('div');
                const img = document.createElement('img');
                const p = document.createElement('p');
                const img2 = document.createElement('img');
        
                if (link.link.substring(0, 4) != 'http') {
                    a.href = `https://${link.link}`;
                } else {
                    a.href = link.link;
                }
                a.target = "_blank"
                div.className = "card";
        
                img.src = `https://s2.googleusercontent.com/s2/favicons?domain=${link.link}&sz=256`;

                img.className = "icon";

                p.innerHTML = link.name;
                img2.src = "../static/icon/trash.svg";
                img2.className = "trash";
                img2.addEventListener('click', () => {cardDELETE(link.id, link.section_id)})

                div.appendChild(a);
                a.appendChild(img);
                a.appendChild(p);
                div.appendChild(img2);
                cardContainer.appendChild(div);
            })
        });

    for (let i = 0; i < 6; i++) {
        const div = document.createElement('div');
        div.className = "card";
        cardContainer.appendChild(div);
    }
}

function loadSections(sections) {
    sectionContainer.innerHTML = '';
    sections.forEach(section => {
        const div = document.createElement('div');
        div.innerText = section.emoji;
        div.addEventListener('click', () => {
            currentSection.value = section.id;
            loadCards(section.id);
        })
        sectionContainer.appendChild(div);
    })
}

function showModal(target) {
    modal.style.display = 'grid';
    cardPOST.style.display = 'none';
    sectionPOST.style.display = 'none';
    
    target.style.display = 'block';

    document.querySelectorAll('.clear').forEach(element => {
        element.value = "";
    })
    document.querySelector('.example-img').removeAttribute('src');
    document.querySelector('.example-text').innerHTML = "";
}

sectionPOST.addEventListener('submit', (e) => {
    e.preventDefault()

    var formData = new FormData();
    formData.append('emoji', e.target[0].value);
    formData.append('section_name', e.target[1].value);

    fetch('/section', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => loadSections(data));

    modal.style.display = 'none';
});

cardPOST.addEventListener('submit', (e) => {
    e.preventDefault()

    var formData = new FormData();
    formData.append('card_name', e.target[0].value);
    formData.append('link', e.target[1].value);
    formData.append('section_id', currentSection.value);

    fetch('/card', {
        method: 'POST',
        body: formData
    })
        .then(modal.style.display = 'none')
        .then(setTimeout(() => {loadCards(currentSection.value)}, 100));
});

sectionDELETE.addEventListener('click', () => {
    var formData = new FormData();
    formData.append('section_id', currentSection.value);

    fetch('/section', {
        method: 'DELETE',
        body: formData
    })
        .then(response => response.json())
        .then(data => loadSections(data))

    loadEmpty()
})

function cardDELETE(cardId, section_id) {
    var formData = new FormData();
    formData.append('card_id', cardId);
    formData.append('section_id', section_id);

    fetch('/card', {
        method: 'DELETE',
        body: formData
    })
        .then(response => response.json())
        .then(data => console.log(data))
        .then(setTimeout(() => {loadCards(section_id)}, 100));
}

loadEmpty()