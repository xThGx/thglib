

def factorial(n: int) -> int:
    if n >= 0:
        product = 1
        for i in range(2 , n + 1):
            product *= i
        return product
    raise Exception("Enter a positive Number.")


if __name__ == "__main__":
    n = input("Enter a number you want the factorial of: ")
    print(factorial(int(n)))
