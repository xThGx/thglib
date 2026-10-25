

def exponentiate(d: int, e: int) -> int:
    return d ** e


if __name__ == "__main__":
    d = input("Enter the base: ")
    e = input("Enter the exponent: ")
    print(exponentiate(int(d), int(e)))
