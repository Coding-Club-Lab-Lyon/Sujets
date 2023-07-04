#!/bin/python3

def main() -> None:
    with open("distances.txt") as file:
        content = file.read().split("\n")
    content = [[int(i) for i in line.split(" ")] for line in content]
    times = [line[0] / line[1] * 60 for line in content]
    minTime = int(min(times))
    print(f"Minumum time: {minTime} minutes")

if __name__ == "__main__":
    main()
