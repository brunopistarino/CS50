students = []

with open("students.csv") as file:
    for line in file:
        name, house = (line.strip().split(","))
        students.append({"name": name, "house": house})


for student in sorted(students, key=lambda student: student["name"], reverse=True):
    print(f"{student['name']} is in {student['house']}")
