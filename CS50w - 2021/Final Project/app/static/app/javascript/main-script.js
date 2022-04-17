document.addEventListener('DOMContentLoaded', function() {
    document.querySelector("#back-main-button").addEventListener('click', () => main_view());
    document.querySelector("#back-main-button2").addEventListener('click', () => main_view());
    document.querySelector("#popup-close").addEventListener('click', () => popup_view("close"));
    document.querySelector("#profile").addEventListener('click', () => profile_view());

    document.querySelector("#create-project-form").onsubmit = () => create_project();
    document.querySelector("#edit-project-form").onsubmit = () => edit_project();

    document.querySelector("#create-color-1").addEventListener('click', () => select_color(1));
    document.querySelector("#create-color-2").addEventListener('click', () => select_color(2));
    document.querySelector("#create-color-3").addEventListener('click', () => select_color(3));
    document.querySelector("#create-color-4").addEventListener('click', () => select_color(4));
    document.querySelector("#create-color-5").addEventListener('click', () => select_color(5));

    window.addEventListener('resize', () => show_hide_word_task());

    project_slider = document.querySelector("#projects-container");
    
    project_slider.addEventListener('mousedown', (e) => {
        down = true;
        drag = false;
        startX = e.pageX - project_slider.offsetLeft;
        scrollLeft = project_slider.scrollLeft;
    });
    project_slider.addEventListener('mouseleave', () => {
        down = false;
    });
    project_slider.addEventListener('mouseup', () => {
        down = false;
    });
    project_slider.addEventListener('mousemove', (e) => {
        drag = true;
        if(down == true) {
            e.preventDefault();
            project_slider.scrollLeft = scrollLeft - (e.pageX - project_slider.offsetLeft - startX);
        }
    });

    main_view();
});

var project_slider;
var down = false;
var drag = false;
var startX;
var scrollLeft;

function main_view() {
    document.querySelector("#main-view").style.display = "block";
    document.querySelector("#profile").style.display = "block";
    document.querySelector("#project-view").style.display = "none";
    document.querySelector("#profile-view").style.display = "none";
    document.querySelector("#edit-project-id").value = "";

    document.querySelector("#background").className = "bg-color0";
    document.title = "Brupi - Main";

    const projects_container = document.querySelector("#projects-container");
    const tasks_container = document.querySelector("#tasks-list-container");
    const completed_tasks_container = document.querySelector("#completed-tasks-list-container");

    fetch('/main_view')
    .then(response => response.json())
    .then(main => {
        document.querySelector("#good-morning").innerHTML = `Good morning, ${main.first_name}!`;
        document.querySelector("#good-morning-tasks").innerHTML = `You have ${main.tasks_completed + main.tasks_left} tasks for today and ${main.tasks_for_the_week} tasks for this week.`;

        const projects = JSON.parse(main.projects);
        const tasks = JSON.parse(main.tasks)
        const location = "in_main";
        const project_id = 0;

        load_projects_cards(projects, projects_container);
        load_tasks(tasks, tasks_container, completed_tasks_container, location);
        load_calendar(location, project_id);
        document.querySelector("#profile").innerHTML = "";
        load_profile_picture(main.user_pk, document.querySelector("#profile"));

        document.querySelector("#all-total-daily-tasks").innerHTML = `${main.tasks_completed + main.tasks_left} tasks`;
        document.querySelector("#all-completed-left-daily-tasks").innerHTML = `${main.tasks_completed} completed, ${main.tasks_left} left`;
    })
}

function project_view(project) {
    const location = "in_project";
    const project_id = project.pk;
    load_calendar(location, project_id);

    document.querySelector("#project-view").style.display = "block";
    document.querySelector("#main-view").style.display = "none";

    document.querySelector("#background").className = `bg-color${project.fields.color}`;
    document.title = `Brupi - ${project.fields.name}`;
    
    const project_tasks_container_button = document.querySelector("#project-tasks-container-button");
    const project_send_chat_container = document.querySelector("#send-chat-container");

    project_tasks_container_button.innerHTML = "";
    project_send_chat_container.innerHTML = "";
    document.querySelector("#edit-project-button-div").innerHTML = "";
    document.querySelector("#delete-project-button-div").innerHTML = "";

    const create_task_button = document.createElement("button");
    const send_chat_input = document.createElement("input");
    const send_chat_button = document.createElement("button");

    create_task_button.innerHTML = "Create task";
    send_chat_button.innerHTML = `<i class="fas fa-paper-plane"></i>`;

    create_task_button.id = "project-create-task";
    send_chat_input.id = "send-chat-input";
    send_chat_button.id = "send-chat-button";

    send_chat_input.placeholder = "Type something";

    project_tasks_container_button.appendChild(create_task_button);
    project_send_chat_container.appendChild(send_chat_input);
    project_send_chat_container.appendChild(send_chat_button);

    document.querySelector("#project-view-name").innerHTML = project.fields.name;

    create_task_button.addEventListener('click', () => popup_view("create_task", project));
    send_chat_button.addEventListener('click', () => create_chat(project.pk, send_chat_input));
    document.querySelector("#create-task-form").onsubmit = () => create_task(project.pk);
    document.querySelector("#edit-project-id").value = project.pk;

    fetch(`/get_tasks_by_project/${project.pk}`)
    .then(response => response.json())
    .then(unserialized_tasks => {
        const tasks = JSON.parse(unserialized_tasks.tasks);
        container = document.querySelector("#project-tasks-container-tasks-container");
        container_completed = document.querySelector("#completed-project-tasks-container-tasks-container");
        const location = "in_project";
        const actualdate = unserialized_tasks.actual_date;
        load_tasks(tasks, container, container_completed, location, actualdate);
    })

    fetch(`/get_chats_by_project/${project.pk}`)
    .then(response => response.json())
    .then(unserialized_chats => {
        const chats = JSON.parse(unserialized_chats.chats);
        const current_user_id = unserialized_chats.current_user_id;
        load_chats(chats, current_user_id);
    })

    fetch(`/is_current_user_owner/${project.pk}`)
    .then(response => response.json())
    .then(is_owner => {
        if (is_owner.response === true) {
        const edit_project = document.createElement("button");
        edit_project.innerHTML = `<i class="fas fa-pencil-alt"></i>`;
        edit_project.id = "edit-project-button";
        edit_project.className = "clickeable";
        document.querySelector("#edit-project-button-div").appendChild(edit_project);
        edit_project.addEventListener('click', () => popup_view("edit_project"));

        const delete_project_button = document.createElement("button");
        delete_project_button.innerHTML = "Delete project";
        delete_project_button.id = "delete-project-button";
        delete_project_button.className = "clickeable";
        delete_project_button.type = "button";
        document.querySelector("#delete-project-button-div").appendChild(delete_project_button);
        delete_project_button.addEventListener('click', () => delete_project(project.pk));
        }
    })

    const project_members_section = document.querySelector("#project-members-section");
    project_members_section.innerHTML = "";
    project.fields.members.forEach(member => {
        load_profile_picture(member, project_members_section);
    })
}

function profile_view() {
    document.querySelector("#profile-view").style.display = "block";
    document.querySelector("#main-view").style.display = "none";
    document.querySelector("#project-view").style.display = "none";
    document.querySelector("#profile").style.display = "none";

    document.title = "Brupi - Profile";

    fetch("/get_all_users")
    .then(response => response.json())
    .then(user => {
        document.querySelector("#profile-username").innerHTML = user.current_user_username;
        document.querySelector("#profile-first-name").innerHTML = user.current_user_first_name;
        document.querySelector("#profile-last-name").innerHTML = user.current_user_last_name;
        document.querySelector("#profile-email").innerHTML = user.current_user_email;
        
        document.querySelector("#profile-picture").innerHTML = "";
        load_profile_picture(user.current_user_pk, document.querySelector("#profile-picture"));
    })
}

function popup_view(type, info) {
    document.querySelector("#popup-view").style.display = "grid";
    document.querySelector("#create-task-view").style.display = "none";
    document.querySelector("#create-project-view").style.display = "none";
    document.querySelector("#edit-project-view").style.display = "none";

    document.querySelector(".content").scrollTo(0, 0);
    document.querySelector(".content").classList.add("stop-scrolling");

    switch (type) {
        case "create_task":

            document.querySelector("#create-task-view").style.display = "block";
            document.querySelector("#create-task-options").innerHTML = "";
            document.querySelector("#create-task-title").value = "";
            document.querySelector("#create-task-date").value = "";
            document.querySelector("#create-task-name-alert").style.display = "none";
            document.querySelector("#create-task-member-alert").style.display = "none";
            document.querySelector("#create-task-date-alert").style.display = "none";
            document.querySelector("#create-task-date").setAttribute("min", new Date().toISOString().split("T")[0]);

            const placeholder = document.createElement("option");
            placeholder.innerHTML = "Select a member";
            placeholder.disabled = true;
            placeholder.selected = true;
            placeholder.hidden = true;
            document.querySelector("#create-task-options").appendChild(placeholder);

            info.fields.members.forEach(member => {
                fetch(`/get_user/${member}`)
                .then(response => response.json())
                .then(user => {
                    const option = document.createElement("option");
                    option.innerHTML = `${user.first_name} ${user.last_name}`;
                    option.value = user.id;
                    document.querySelector("#create-task-options").appendChild(option);
                })
            })
            break;

        case "create_project":

            document.querySelector("#create-project-view").style.display = "block";
            document.querySelector("#create-project-members").innerHTML = "";
            document.querySelector("#create-project-name-alert").style.display = "none";
            document.querySelector("#create-project-color-alert").style.display = "none";
            fetch(`/get_all_users`)
            .then(response => response.json())
            .then(unserialized_users => {
                const users = JSON.parse(unserialized_users.users)
                users.forEach(user => {
                    if (user.fields.username != unserialized_users.current_user_username) {
                        const option = document.createElement("option");
                        option.innerHTML = `${user.fields.first_name} ${user.fields.last_name}`;
                        option.value = `${user.fields.username}`;
                        document.querySelector("#create-project-members").appendChild(option);
                    }
                })
            })
            break;

        case "edit_project":

            document.querySelector("#edit-project-view").style.display = "block";
            document.querySelector("#edit-project-members").innerHTML = "";
            fetch(`/get_all_users`)
            .then(response => response.json())
            .then(unserialized_users => {
                const users = JSON.parse(unserialized_users.users);

                fetch(`get_project/${document.querySelector("#edit-project-id").value}`)
                .then(response => response.json())
                .then(unserialized_project => {
                    const project =JSON.parse(unserialized_project.project);

                    users.forEach(user => {
                        if (user.fields.username != unserialized_users.current_user_username) {
                            const option = document.createElement("option");
                            option.innerHTML = `${user.fields.first_name} ${user.fields.last_name}`;
                            option.value = `${user.fields.username}`;
                            fetch(`/get_user_id_by_username/${user.fields.username}`)
                            .then(response => response.json())
                            .then(user_id => {
                                if (project[0].fields.members.includes(user_id.id)) {
                                    option.selected = "true";
                                }
                            })
                            document.querySelector("#edit-project-members").appendChild(option);
                        }
                    })
                })
            })
            break;

        case "close":
            document.querySelector("#popup-view").style.display = "none";
            document.querySelector(".content").classList.remove("stop-scrolling");
            break;
    }
}

function select_color(color) {
    document.querySelector("#create-color-1").classList.remove("selected-color");
    document.querySelector("#create-color-2").classList.remove("selected-color");
    document.querySelector("#create-color-3").classList.remove("selected-color");
    document.querySelector("#create-color-4").classList.remove("selected-color");
    document.querySelector("#create-color-5").classList.remove("selected-color");

    document.querySelector(`#create-color-${color}`).classList.add("selected-color");
    document.querySelector("#create-project-hide-color").value = color;
}

function load_projects_cards(projects, container) {
    container.innerHTML = "";

    projects.forEach(project => {
        const project_container_card = document.createElement("div");
        const project_name = document.createElement("p");
        const project_pending = document.createElement("p");
        const project_members = document.createElement("div");

        const project_members_count = Object.keys(project.fields.members).length;

        project_container_card.className = `project-container-card bg-color${project.fields.color} clickeable`;
        project_name.className = "project-name second-title";
        project_pending.className = "project-pending text-medium";
        project_members.className = "project-members";

        project_name.innerHTML = project.fields.name;

        fetch(`/get_tasks/${project.pk}`)
        .then(response => response.json())
        .then(tasks => {
            project_pending.innerHTML = `${project_members_count} members, ${tasks.pending_tasks} pending tasks`;
        });

        project_container_card.addEventListener('click', () => {
            if (drag == false) {
                project_view(project);
            }
        })

        project_container_card.appendChild(project_name);
        project_container_card.appendChild(project_pending);
        project_container_card.appendChild(project_members);
        container.appendChild(project_container_card);

        project.fields.members.slice(0, 3).forEach(member => {
            load_profile_picture(member, project_members);
        })
        if (project.fields.members.length > 3) {
            const plus_number = document.createElement("div");
            plus_number.className = "project-members-extra-number";
            plus_number.innerHTML = `+ ${project.fields.members.length - 3}`;
            project_members.appendChild(plus_number);
        }
    });

    const project_container_card_create = document.createElement("div");
    const create_project_button = document.createElement("button");
    project_container_card_create.className = "project-container-card-create";
    create_project_button.id = "create-project-button";
    create_project_button.className = "clickeable";
    create_project_button.innerHTML = "<span>+</span>";
    project_container_card_create.appendChild(create_project_button);
    container.appendChild(project_container_card_create);
    create_project_button.addEventListener('click', () => popup_view("create_project"));
}

function load_tasks(tasks, container, container_completed, location, actualdate) {
    container.innerHTML = "";
    container_completed.innerHTML = "";

    tasks.forEach(task => {
        const task_list_item = document.createElement("div");
        const task_check = document.createElement("div");
        const task_text = document.createElement("div");
        const task_title = document.createElement("p");
        const task_project = document.createElement("p");

        const date = Date.parse(task.fields.date);
        const actual_date = Date.parse(actualdate);
        const srt_date = task.fields.date.slice(5, 10).replace("-", "/");

        task_check.className = "task-check";
        task_text.className = "task-text";
        task_title.className = "task-title third-title";
        task_project.className = "task-project text-medium";

        task_title.innerHTML = task.fields.name;

        fetch(`/get_project/${task.fields.project}`)
        .then(response => response.json())
        .then(project => {
            const json_project = JSON.parse(project.project);
            if(location === "in_main") {
                    task_project.innerHTML  = `in ${json_project[0].fields.name}`;
                    task_check.addEventListener('click', () => task_complete_uncomplete(task.fields.completed, task_list_item, task.pk));
            } else if(location === "in_project") {
                fetch(`/get_user/${task.fields.user}`)
                .then(response => response.json())
                .then(user => {
                    if (date < actual_date && task.fields.completed !== true) {
                        task_project.innerHTML  = `<span class="task-late">${srt_date}</span> - ${user.first_name} ${user.last_name}`;
                    } else {
                        task_project.innerHTML  = `${srt_date} - ${user.first_name} ${user.last_name}`;
                    }
                    task_check.addEventListener('click', () => task_complete_uncomplete(task.fields.completed, task_list_item, task.pk, json_project[0].pk));
                })
            }
        });

        if(task.fields.completed === false) {
            task_list_item.className = "task-list-item";
            container.appendChild(task_list_item);
        } else {
            task_list_item.className = "task-list-item-complete";
            container_completed.appendChild(task_list_item);
        }

        task_text.appendChild(task_title);
        task_text.appendChild(task_project);
        task_list_item.appendChild(task_check);
        task_list_item.appendChild(task_text);
    });
}

function load_chats(chats, current_user_id) {
    const container = document.querySelector("#chats-container")
    container.innerHTML = "";

    chats.forEach(chat => {
        const chat_container = document.createElement("div");
        const chat_and_timestamp = document.createElement("div");
        const chat_message = document.createElement("p");
        const chat_timestamp = document.createElement("p");

        const date = Date.parse(chat.fields.timestamp)
        const my_date = new Date(date);
        const date_minutes = my_date.getMinutes();
        const date_hours = my_date.getHours();
        const date_day = my_date.getDate();
        var date_month = ""
        switch (my_date.getMonth()) {
            case 0:
                date_month = "jan";
                break;
            case 1:
                date_month = "feb";
                break;
            case 2:
                date_month = "mar";
                break;
            case 3:
                date_month = "apr";
                break;
            case 4:
                date_month = "may";
                break;
            case 5:
                date_month = "jun";
                break;
            case 6:
                date_month = "jul";
                break;
            case 7:
                date_month = "aug";
                break;
            case 8:
                date_month = "sep";
                break;
            case 9:
                date_month = "oct";
                break;
            case 10:
                date_month = "nov";
                break;
            case 11:
                date_month = "dec";
                break;
        }

        if (current_user_id === chat.fields.user) {
            chat_container.className = "chat-right";
        } else {
            chat_container.className = "chat-left";
        }
        chat_and_timestamp.className = "chat-and-timestamp";
        chat_message.className = "chat-message";
        chat_timestamp.className = "chat-timestamp";

        chat_message.innerHTML = chat.fields.message;
        chat_timestamp.innerHTML = `${date_hours}:${date_minutes}hs`;
        chat_timestamp.addEventListener("mouseover", () => {
            chat_timestamp.innerHTML = `${date_day} ${date_month}. ${date_hours}:${date_minutes}hs`;
            setTimeout(() => {
                chat_timestamp.innerHTML = `${date_hours}:${date_minutes}hs`;
            }, 1500);
        })

        container.appendChild(chat_container);
        chat_container.appendChild(chat_and_timestamp);
        chat_and_timestamp.appendChild(chat_message);
        chat_and_timestamp.appendChild(chat_timestamp);

        load_profile_picture(chat.fields.user, chat_container, true)
    } )
    container.scrollTop = container.scrollHeight;
}

function load_profile_picture(profile_id, pfp_location, chat) {
    fetch(`/get_user/${profile_id}`)
    .then(response => response.json())
    .then(user => {
        const pfp_div = document.createElement("div");
        if (chat == true) {
            pfp_div.className = "chat-profile-img";
        } else {
            pfp_div.className = "pfp-div";
        }
        pfp_div.innerHTML = `${user.first_name.charAt(0)}${user.last_name.charAt(0)}`;
        pfp_div.title = `${user.first_name} ${user.last_name}`;
        pfp_location.appendChild(pfp_div);
    })
}

function refresh_project(project_id) {
    fetch(`/get_project/${project_id}`)
    .then(response => response.json())
    .then(unserialized_project => {
        const project = JSON.parse(unserialized_project.project);
        project_view(project[0])
    })
}

function task_complete_uncomplete(completed, task_list_item, task_id, project_id) {
    if(completed === false) {
        task_list_item.className = "task-list-item-complete";
        fetch(`/task_complete_uncomplete/complete/${task_id}`)
    } else {
        task_list_item.className = "task-list-item";
        fetch(`/task_complete_uncomplete/uncomplete/${task_id}`)
    }

    if(project_id == null) {
        main_view();
    } else {
        refresh_project(project_id);
    }
}

function create_task(project_id) {
    var alert = false;

    if (document.querySelector("#create-task-title").value == "") {
        document.querySelector("#create-task-name-alert").style.display = "block";
        alert = true;
    } else {
        document.querySelector("#create-task-name-alert").style.display = "none";
    }
    if (document.querySelector("#create-task-options").value == "Select a member") {
        document.querySelector("#create-task-member-alert").style.display = "block";
        alert = true;
    } else {
        document.querySelector("#create-task-member-alert").style.display = "none";
    }
    if (document.querySelector("#create-task-date").value == "") {
        document.querySelector("#create-task-date-alert").style.display = "block";
        alert = true;
    } else {
        document.querySelector("#create-task-date-alert").style.display = "none";
    }

    if (alert == false) {
        fetch("/create_task", {
            method: 'POST',
            body: JSON.stringify({
                name: document.querySelector("#create-task-title").value,
                user_id: document.querySelector("#create-task-options").value,
                date: document.querySelector("#create-task-date").value,
                project_id: project_id
            })
        })
        refresh_project(project_id);
        popup_view("close");
    }

    return false
}

function create_chat(project_id, send_chat_input) {
    if (send_chat_input.value !== "") {
        fetch("/create_chat", {
            method: 'POST',
            body: JSON.stringify({
                message: send_chat_input.value,
                project_id: project_id,
            })
        })
        refresh_project(project_id);
    }
}

function create_project() {
    var alert = false

    if (document.querySelector("#create-project-name").value == "") {
        document.querySelector("#create-project-name-alert").style.display = "block";
        alert = true;
    } else {
        document.querySelector("#create-project-name-alert").style.display = "none";
    }
    if (document.querySelector("#create-project-hide-color").value == "") {
        document.querySelector("#create-project-color-alert").style.display = "block";
        alert = true;
    } else {
        document.querySelector("#create-project-color-alert").style.display = "none";
    }
    
    if (alert == false) {
        fetch("/create_project", {
            method: 'POST',
            body: JSON.stringify({
                name: document.querySelector("#create-project-name").value,
                members: getSelectValues(document.querySelector("#create-project-members")),
                color: document.querySelector("#create-project-hide-color").value,
            })
        })
        refresh_project(project_id);
        popup_view("close");
    }
    return false
}

function getSelectValues(select) {
    var result = [];
    var options = select && select.options;
    var opt;
  
    for (var i=0, iLen=options.length; i<iLen; i++) {
      opt = options[i];
  
      if (opt.selected) {
        result.push(opt.value || opt.text);
      }
    }
    return result;
}

function is_overflown(element) {
    return element.scrollHeight > element.clientHeight || element.scrollWidth > element.clientWidth;
}

function show_hide_word_task() {
    if (document.getElementById("calendarday_0").offsetWidth < 63) {
        document.querySelectorAll(".word-tasks").forEach(word => {
            word.style.display = "none";
        })
    } else {
        document.querySelectorAll(".word-tasks").forEach(word => {
            word.style.display = "inline";
        })
    }
}

function delete_project(project_id) {
    fetch("/delete_project", {
        method: 'POST',
        body: JSON.stringify({
            project_id: project_id,
        })
    })
    main_view();
    popup_view("close");
}

function edit_project() {
    project_id = document.querySelector("#edit-project-id").value
    fetch("/edit_project", {
        method: 'POST',
        body: JSON.stringify({
            project_id: project_id,
            members: getSelectValues(document.querySelector("#edit-project-members")),
        })
    })
    refresh_project(project_id);
    popup_view("close");
    return false
}