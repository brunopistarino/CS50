def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    if len(s) < 2 or len(s) > 6:
        return False

    if not (s[0].isalpha() and s[1].isalpha()):
        return False

    if "." in s or "," in s or " " in s:
        return False

    first_num = True
    for i in range(len(s)):
        if not s[i].isalpha():
            if first_num and s[i] == "0":
                return False
            first_num = False
            for j in range(i, len(s)):
                if s[j].isalpha():
                    return False

    return True


main()