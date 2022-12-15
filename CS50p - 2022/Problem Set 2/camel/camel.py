camel = input("camelCase: ")
snake = ""

for i in range(len(camel)):
    if camel[i].isupper():
        snake += "_"
    snake += camel[i].lower()

print("snake_case:", snake)