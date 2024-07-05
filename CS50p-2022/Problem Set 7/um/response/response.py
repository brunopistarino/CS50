from validator_collection import validators

def main():
    try:
        validators.email(input("What's your email address? "))
    except:
        print("Invalid")
    else:
        print("Valid")

if __name__ == "__main__":
    main()