#!/bin/python3

def main() -> None:
    n = int(input("Enter a number : "))
    res = 0
    start = 1
    counter = 1

    if (n % 2):
        start = 1
        counter = 2
    for i in range(start, n + 1, counter):
        if n % i == 0:
            res += i
    print(f"Result : {res}")

if __name__ == "__main__":
    main()
