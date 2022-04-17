document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Detect when submit an email
  document.querySelector('#compose-form').onsubmit = () => send_email();

  // Detect colors button
  document.querySelector('#colors').addEventListener('click', () => colors());
  document.querySelector('#background').setAttribute("class", `color-${localStorage.getItem('color')}`);
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emails-list').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#colors-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function colors() {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emails-list').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#colors-view').style.display = 'block';

  document.querySelector('.color-a').addEventListener('click', () => setcolor('a'));
  document.querySelector('.color-b').addEventListener('click', () => setcolor('b'));
  document.querySelector('.color-c').addEventListener('click', () => setcolor('c'));
  document.querySelector('.color-d').addEventListener('click', () => setcolor('d'));
}

function setcolor(color) {
  document.querySelector('#background').setAttribute("class", `color-${color}`);
  localStorage.setItem('color', color);
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#emails-list').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#colors-view').style.display = 'none';
  
  // Show the mailbox name
  document.querySelector('#emails-list').innerHTML = "";
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Request the mailbox emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    var first = true

    emails.forEach((email) => {
      if (first == false) {
        const line = document.createElement("div");
        line.innerHTML = '<hr>';
        document.querySelector("#emails-list").appendChild(line);
      } else {
        first = false
      }
      
      console.log(email);
      const container = document.createElement("div");
      if (email.read == 1) {
        container.className = "email read";
      } else {
        container.className = "email unread";
      }

      if (mailbox == "sent") {
        var sender = `For: ${email.recipients}`;
      } else {
        var sender = email.sender;
      }
      console.log(sender);
      container.innerHTML = `<div style="display: flex;">${sender} <div style="margin-left: 10px">${email.subject}</div><div id="email-time">${email.timestamp}</div></div>`;
      container.addEventListener('click', () => load_email(email.id))
      document.querySelector("#emails-list").appendChild(container);

      if (mailbox != "sent") {
        const archive = document.createElement("button");
        archive.setAttribute("id", "archive");
        archive.setAttribute("class", "btn btn-sm btn-outline-dark");
        archive.textContent = email.archived ? "Unarchive" : "Archive";
        archive.addEventListener('click', () => archive_mail(email.id))
        document.querySelector('#emails-list').appendChild(archive);
      }
    })
  })
}

// Load individual email
function load_email(email_id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emails-list').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    document.querySelector('#email-sender').innerHTML = email.sender;
    document.querySelector('#email-recipients').innerHTML = email.recipients;
    document.querySelector('#email-subject').innerHTML = email.subject;
    document.querySelector('#email-timestamp').innerHTML = email.timestamp;
    document.querySelector('#email-body').innerHTML = email.body;
    document.querySelector('#email-reply').addEventListener('click', () => {
      compose_email()
        document.querySelector('#compose-recipients').value = email.sender;
        if(email.subject.search("Re:") == 0) {
          document.querySelector('#compose-subject').value = email.subject;
        } else {
          document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
        }
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`
        console.log('datos cargados');
    });
  })

  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}

// Reply
function send_email() {
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
    .then(() => load_mailbox('sent'))
  })
  .then(response => response.json())
  .then(result =>{
    console.log(result);
  });
  return false;
}

// Archive
function archive_mail(email_id) {
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    if(email.archived == true) {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: false
        })
      })
      .then(() => load_mailbox('inbox'))
    } else {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: true
        })
      })
      .then(() => load_mailbox('inbox'))
    }
  })
}
