# To-Do List
#### Video Demo: https://youtu.be/v3Vir7bsEMQ
#### Description:

This program is a command line to-do list manager that allows the user to add, remove, and mark tasks as done. The tasks are saved to a CSV file called "tasks.csv" in the same directory as the program. If the file does not exist, it will be created automatically.

The program begins by checking if the tasks.csv file exists. If it doesn't, a new file is created and the "id", "task", and "done" field names are written to the first row. Then enters an infinite loop in which it displays the pending tasks and shows the main menu with the following options:

- **Add task:** allows the user to add a new task to the list by typing it in and pressing enter
- **Remove task:** lets the user select a task from the list and remove it
- **Mark task as done:** allows the user to select a task from the list and mark it as done
- **View all tasks:** shows the user a list of all tasks, including pending and completed tasks
- **Exit:** exits the program

## Design choices
One of the design choices made with this program is the use of a CSV file to store the tasks. This allows the user to easily view and edit the tasks using a spreadsheet program like Microsoft Excel or Google Sheets. It also allows the tasks to be easily transferred to another program or system that can read CSV files.

Another design choice is the use of unique IDs for each task. This allows the program to easily identify and manipulate individual tasks without relying on their position in the list or their content. It also ensures that tasks with the same content are treated as distinct tasks.

The program also uses an infinite loop to constantly display the pending tasks and the main menu. This allows the user to easily add, remove, and mark tasks as done without having to repeatedly run the program. It also makes it easy for the user to view the updated list of tasks after performing an action.

The program uses the `keyboard` and `csv` modules to handle user input and read/write to the tasks.csv file. The `uuid` module is used to generate unique IDs for each task. The `sys` module is used to exit the program when the user chooses the "Exit" option from the main menu.

## Possible improvements
- Implement object-oriented programming to improve the design of the program.
- Add additional features, such as the ability to prioritize tasks, categorize tasks, and set deadlines for tasks.
- Optimize the program for performance, for example by using more efficient algorithms for storing and accessing the tasks.

## How to run the application
1. Make sure you have Python installed on your computer.
2. Clone or download the repository.
3. Open a terminal and navigate to the folder where you saved the program.
4. Run the command `pip install -r requirements.txt`.
5. Run the command `python3 project.py`.
6. The program will run and present a menu of options. Follow the on-screen instructions to add, remove, and manage tasks.
