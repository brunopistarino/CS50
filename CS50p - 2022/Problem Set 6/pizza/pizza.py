from tabulate import tabulate
import sys, csv

if len(sys.argv) < 2:
    sys.exit("Too few command-line arguments")
if len(sys.argv) > 2:
    sys.exit("Too many command-line arguments")
if sys.argv[1][-4:] != ".csv":
    sys.exit("Not a CSV file")

headers = []
table = []
try:
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            headers = list(row)
            trow = []
            for header in headers:
                trow.append(row[header])
            table.append(trow)
except FileNotFoundError:
    sys.exit("File not found")


print(tabulate(table, headers, tablefmt="grid"))