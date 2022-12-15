import keyboard
import csv
import os
import uuid
import sys


def main():
    if not os.path.exists("tasks.csv"):
        with open("tasks.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "task", "done"])
            writer.writeheader()

    while True:
        os.system('cls||clear')
        tasks = get_tasks("pending")
        print("Pending:")
        show_tasks(tasks)
        print()
        show_menu()


def add_task():
    os.system('cls||clear')
    task = input("Task: ")
    if task:
        with open("tasks.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "task", "done"])
            writer.writerow(
                {"id": uuid.uuid1(), "task": task, "done": "False"})


def remove_task():
    tasks = get_tasks()
    if task_id := select_task(tasks, "Select the task and press enter to remove it"):
        tasks = list(filter(lambda t: t["id"] != task_id, tasks))
        with open("tasks.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "task", "done"])
            writer.writeheader()
            for task in tasks:
                writer.writerow(task)


def show_tasks(tasks):
    for task in tasks:
        if task["done"] == "False":
            print(f"- {task['task']}")
        else:
            print(f"- {strike(task['task'])}")


def show_menu():
    print("What do you want to do next?")
    print("1) Add task")
    print("2) Remove task")
    print("3) Mark task as done")
    print("4) View all tasks")
    print("5) Exit")

    key = input("\nAction: ")
    if key == "1":
        add_task()
    if key == "2":
        remove_task()
    if key == "3":
        mark_task()
    if key == "4":
        view_tasks()
    if key == "5":
        sys.exit()


def get_tasks(type="all"):
    tasks = []
    with open("tasks.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tasks.append(row)

    if type == "all":
        return tasks
    if type == "done":
        return list(filter(lambda t: t["done"] == "True", tasks))
    if type == "pending":
        return list(filter(lambda t: t["done"] == "False", tasks))


def mark_task():
    tasks = get_tasks("pending")
    msg = "Select the task and press enter to mark it as done"
    if task_id := select_task(tasks, msg):
        all_taks = get_tasks()
        all_taks = list(map(lambda t: t if t["id"] != task_id else {
            "id": t["id"], "task": t["task"], "done": "True"}, all_taks))
        with open("tasks.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "task", "done"])
            writer.writeheader()
            for task in all_taks:
                writer.writerow(task)


def select_task(tasks, message=""):
    cursor = 0
    while True:
        os.system('cls||clear')
        if message:
            print(message)

        for i, task in enumerate(tasks):
            if i == cursor:
                if is_pending(task):
                    print(color(">"), task['task'])
                else:
                    print(color(">"), strike(task['task']))
            else:
                if is_pending(task):
                    print(f"- {task['task']}")
                else:
                    print(f"- {strike(task['task'])}")

        print("\nPress esc to cancel", end="")

        key = keyboard.read_key()
        if key == "up" and cursor > 0 and keyboard.is_pressed("up"):
            cursor -= 1
        if key == "down" and cursor < len(tasks) - 1 and keyboard.is_pressed("down"):
            cursor += 1
        if key == "enter" and keyboard.is_pressed("enter"):
            return tasks[cursor]['id']
        if key == "esc" and keyboard.is_pressed("esc"):
            return None


def view_tasks():
    os.system('cls||clear')
    tasks = get_tasks("pending")
    print("Pending:")
    show_tasks(tasks)
    print()

    print("Done:")
    tasks = get_tasks("done")
    show_tasks(tasks)
    print()
    input("Press enter to continue")


def color(s):
    return "\33[92m" + s + '\033[0m'


def strike(s):
    r = ""
    for c in s:
        r += c + "\u0336"
    return r


def is_pending(task):
    return task["done"] == "False"


if __name__ == "__main__":
    main()
