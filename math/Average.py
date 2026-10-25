

def average(numbers: list) -> float:
    result = sum(numbers) / len(numbers)
    return result


if __name__ == "__main__":
    numbers = []
    while True:
        a = input("Enter numbers ('y' to finish): ")
        if a in ['y', '', None]:
            print(f"The average is: {average(numbers)}")
            break         
        numbers.append(int(a))
        print(numbers)
        print(len(numbers))
        #print(sum(numbers))

