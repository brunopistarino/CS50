x, y, z = input("Expression: ").strip().split(" ")
x = int(x)
z = int(z)

match y:
    case "+":
        r = x + z
    case "-":
        r = x - z
    case "*":
        r = x * z
    case "/":
        r = x / z

print(f"{r:.1f}")