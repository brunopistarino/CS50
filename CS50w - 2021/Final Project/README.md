# Final Project CS50's Web Programming with Python and JavaScript
## Introduction
My final work is a task application oriented to work environments. Users can create “projects” and add their coworkers. In each “project” users will be able to talk with their colleagues and create tasks for themselves or others, these will be shown in a calendar with all pending tasks of the members of that “project”. In addition to the project view, users will also have a main view, which shows a header with how many pending tasks has for the week, a slider with all the “projects” in which the user is, a list with all pending tasks for the current day and a calendar showing all pending tasks.

## Distinctiveness and Complexity
There are multiple reasons I believe my application satisfies the distinction and complexity requirements.
* Once logged in, the web page will not need to be reloaded. All the functions of the application are programmed using JavaScript and the interactions with the server are made by fetching data.
* The calendar in the main view and in the project view is not included in any template. It is generated on the fly based on the selected month and year.
* When you open the application, it checks if the user is logged in. If he is, he will be redirected to the main page, if he's not, he will be redirected to the landing page where he will be able to register or log in.
* This project uses more models than the previous projects, and they are related to each other with ForeignKeys and ManyToManyFields.
* This project has a modern design based on glassmorphism. It uses transparencies and blurs to highlight on-screen elements.
* It is full responsive, so it could be used with the same user experience in any screen size. The elements will be repositioned depending on the size of the window to give a clear view of all elements.
* I did not use any framework like Bootstrap or Tailwind for the styling and responsiveness of the application.
* All forms will display alert messages if data is entered incorrectly or if a field is empty.

## File structure
* :open_file_folder: `Main Directory`
  * :open_file_folder: `app` - Main application directory.
    * :open_file_folder: `static/app` - Contains all static files.
      * :open_file_folder: `css` - Contains all CSS files.
        * :page_facing_up: `fonts.css` Contains all the sizes, weights and colors of the fonts used in the application.
        * :page_facing_up: `landing-styles.css` - Styles for landing and registration page.
        * :page_facing_up: `main-styles.css` - Styles for the main application.
      * :open_file_folder: `javascript` - Contains all JavaScript files.
        * :page_facing_up: `calendar-script.js` - This script generates the calendar in the main and project view in `main.html` template. It is also responsible for updating the calendar when the year or month is changed and shows the tasks that correspond to each day.
        * :page_facing_up: `landing-script.js` - This script runs in `landing.html` template and gives the functionality to the "Features" button.
        * :page_facing_up: `main-script.js` - This script runs on `layout.html`. It fetches data from `views.py` and generates the "projects", tasks and chats for each user.
        * :page_facing_up: `register-login-script.js` - This script runs in `register-login.html` template and makes it possible to switch between the registration and login views.
      * :open_file_folder: `resources` - Contains all the images, backgrounds and logos used in the application.
        * :star: `favicon.ico` - Website icon displayed in the browser tab.
        * :framed_picture: `landing.png` - Preview image of the application displayed in `landing.html` template.
        * :framed_picture: `landing-bg.svg` - Background for `landing.html` template.
        * :framed_picture: `logo.svg` - Name and logo of the application displayed in `landing.html` and `register-login.html` templates.
        * :framed_picture: `register-login-bg.svg` - Background for `register-login.html` template.
    * :open_file_folder: `templates/app` - Contains all HTML files.
      * :open_file_folder: `landing` - Contains the templates used in the landing page and in the registration page.
        * :page_facing_up: `basic-layout.html` - Base template for `landing.html` and `register-login.html`.
        * :page_facing_up: `landing.html` - This template contains the landing page, and it will be shown the first time you open the application or if you log out.
        * :page_facing_up: `register-login.html` - This template contains the login and registration forms.
      * :open_file_folder: `main` - Contains the templates used in the main page.
        * :page_facing_up: `index.html` - This template contains the main page.
        * :page_facing_up: `layout.html` - Base template for `index.html`.
    * :page_facing_up: `admin.py` - In this file I have registered the four models used by the application.
    * :page_facing_up: `models.py` - Contains the models used in the application. `User` for users profiles, `Projects` for created "projects", `Tasks` for assigned tasks and `Chats` for chats in each "project".
    * :page_facing_up: `urls.py` - Contains all url paths.
    * :page_facing_up: `views.py` - Contains all view functions for the project and functions that provide data for `main-script.js`.
  * :open_file_folder: `finalproject` - Project directory.
  * :page_facing_up: `gitignore` - List of ignored files and folders for git.
  * :page_facing_up: `manage.py`
  * :framed_picture: `preview.gif` - Preview gif displayed in `README.md`.

## How to run the application
1. Clone or download the repository.
1. If you don't have Django installed, install it by running `pip3 install Django`.
1. In your terminal, `cd` into the main directory.
1. Make migrations by running `python manage.py makemigrations app`.
1. Apply migrations by running `python manage.py migrate`.
1. Run `python manage.py runserver` to start the web server.
1. Open the website in your browser, and press the “Start now” button to register for a new account.

## Preview
![Landing](preview.gif)
