var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var week_days = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"]
var month = 0;
var year = 0;

function load_calendar(location, project_id) {

    var calendar_container
    if(location == "in_main") {
        calendar_container = document.querySelector("#calendar");
    } else {
        calendar_container = document.querySelector("#project-calendar-container");
    }

    document.querySelector("#calendar").innerHTML = "";
    document.querySelector("#project-calendar-container").innerHTML = "";

    const calendar_top = document.createElement("div");
    const calendar_months = document.createElement("div");
    const current_month_span = document.createElement("span");
    const months_container = document.createElement("div");
    const calendar_years = document.createElement("div");
    const current_year_span = document.createElement("span");
    const years_container = document.createElement("div");
    const clear = document.createElement("div");
    const calendar_days = document.createElement("div");
    const days_label = document.createElement("div");
    const days_container = document.createElement("div");

    calendar_top.id = "calendar-top";
    calendar_months.id = "calendar-months";
    current_month_span.id = "current-month";
    current_month_span.className = "second-title clickeable";
    months_container.id = "months";
    calendar_years.id = "calendar-years";
    current_year_span.id = "current-year";
    current_year_span.className = "second-title clickeable";
    years_container.id = "years";
    clear.className = "clear";
    calendar_days.id = "calendar-days";
    days_label.id = "days-label";
    days_container.id = "days";

    calendar_container.appendChild(calendar_top);
    calendar_top.appendChild(calendar_months);
    calendar_months.appendChild(current_month_span);
    calendar_months.appendChild(months_container);
    calendar_top.appendChild(calendar_years);
    calendar_years.appendChild(current_year_span);
    calendar_years.appendChild(years_container);
    calendar_container.appendChild(clear);
    calendar_container.appendChild(calendar_days);
    calendar_days.appendChild(days_label);
    calendar_days.appendChild(days_container);

    var date = new Date();
    month = date.getMonth();
    year = date.getFullYear();
    current_month_span.innerHTML = months[month];
    current_year_span.innerHTML = year;

    months_container.style.display = "none";
    years_container.style.display = "none";

    current_month_span.addEventListener('click', () => toggle_view(months_container));
    current_year_span.addEventListener('click', () => toggle_view(years_container));

    for (var i = 0; i < week_days.length; i++) {
        var doc = document.createElement("div");
        doc.innerHTML = week_days[i];
        doc.className = "day label";
        days_label.appendChild(doc);
    }

    load_months(months_container, project_id);
    load_years(years_container, project_id);
    load_days(project_id);
}

function load_months(months_container, project_id) {
    for (var i = 0; i < months.length; i++) {
        var doc = document.createElement("div");
        doc.innerHTML = months[i];
        doc.className = "dropdown-item";

        doc.onclick = (function () {
            var selected_month = i;
            return function () {
                month = selected_month;
                months_container.style.display = "none";
                document.querySelector("#current-month").innerHTML = months[month]
                load_days(project_id);
                return month;
            }
        })();
        
        months_container.appendChild(doc)
    }
}

function load_years(years_container, project_id) {
    var start_year = new Date().getFullYear() - 1;
    var end_year = new Date().getFullYear() + 5;

    for(var i = start_year; i <= end_year; i++) {
        var doc = document.createElement("div");
        doc.innerHTML = i;
        doc.className = "dropdown-item";

        doc.onclick = (function () {
            var selected_year = i;
            return function () {
                year = selected_year;
                years_container.style.display = "none";
                document.querySelector("#current-year").innerHTML = year;
                load_days(project_id);
                return year;
            }
        })();

        years_container.appendChild(doc);
    }
}

function load_days(project_id) {
    document.querySelector("#days").innerHTML = "";
    
    var tmp_date = new Date(year, month, 0);
    var num = daysInMonth(year, month);
    var day_of_week = tmp_date.getDay();

    for(var i = 0; i <= day_of_week; i++) {
        var d = document.createElement("div");
        d.className = "day blank";
        document.querySelector("#days").appendChild(d);
    }

    for(var i = 0; i < num; i++) {
        var tmp = i + 1;
        var d = document.createElement("div");
        d.id = "calendarday_" + i;
        d.className = "day";
        d.innerHTML = tmp;
        document.querySelector("#days").appendChild(d);
    }

    var clear = document.createElement("div");
    clear.className = "clear";
    document.querySelector("#days").appendChild(clear);

    load_calendar_tasks(project_id);
    show_current_day();
}

function daysInMonth(year, month) {
    let d = new Date(year, month+1, 0);
    return d.getDate();
}

function toggle_view(container) {
    if (container.style.display === "none") {
        container.style.display = "block";
    } else {
        container.style.display = "none";
    }
}

function load_calendar_tasks(project_id) {
    if (project_id == 0) {
        fetch('/get_user_all_tasks')
        .then(response => response.json())
        .then(unserialized_tasks => {
            create_calendar_tasks(unserialized_tasks);
        })
    } else {
        fetch(`/get_tasks_by_project/${project_id}`)
        .then(response => response.json())
        .then(unserialized_tasks => {
            create_calendar_tasks(unserialized_tasks);
        })
    }
}

function create_calendar_tasks(unserialized_tasks) {
    const tasks = JSON.parse(unserialized_tasks.tasks)
    tasks.forEach(task => {
        const date = Date.parse(task.fields.date)
        my_date = new Date(date);
        const date_day = my_date.getDate();
        const date_month = my_date.getMonth();
        const date_year = my_date.getFullYear();
        if (month == date_month && year == date_year && task.fields.completed == false) {
            if (document.querySelector(`#calendarday_${date_day}_task`) === null) {
                const element = document.createElement("p");
                element.innerHTML = `<span id="calendarday_${date_day}_task_number">1</span><span class="word-tasks" id="word-tasks-${date_day}"> task</span>`;
                element.id = `calendarday_${date_day}_task`;
                element.className = "calendar-task-low calendar-task";
                document.querySelector(`#calendarday_${date_day}`).appendChild(element);
            } else {
                task_number = document.querySelector(`#calendarday_${date_day}_task_number`).innerHTML;
                int_task_number = parseInt(task_number) + 1;
                document.querySelector(`#calendarday_${date_day}_task_number`).innerHTML = int_task_number;
                document.querySelector(`#word-tasks-${date_day}`).innerHTML = " tasks"
                if (int_task_number <= 2) {
                    document.querySelector(`#calendarday_${date_day}_task`).className = "calendar-task-low calendar-task"
                } else if (int_task_number <= 4) {
                    document.querySelector(`#calendarday_${date_day}_task`).className = "calendar-task-medium calendar-task"
                } else {
                    document.querySelector(`#calendarday_${date_day}_task`).className = "calendar-task-high calendar-task"
                }
            }
        }
    })
    show_hide_word_task();
}

function show_current_day() {
    my_date = new Date();
    const date_day = my_date.getDate();
    const date_month = my_date.getMonth();
    const date_year = my_date.getFullYear();
    if (month == date_month && year == date_year) {
        document.querySelector(`#calendarday_${date_day - 1}`).className = "day current-day";
    }
}