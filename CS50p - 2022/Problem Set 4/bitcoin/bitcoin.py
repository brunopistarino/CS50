import requests
import sys

if len(sys.argv) < 2:
    sys.exit("Missing command-line argument")

try:
    amount = float(sys.argv[1])
    r = (
        requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        .json()["bpi"]["USD"]["rate"]
        .replace(",", "")
    )
    print(f"${float(r)*amount:,.4f}")
except requests.RequestException:
    print("a")
except ValueError:
    sys.exit("Command-line argument is not a number")
