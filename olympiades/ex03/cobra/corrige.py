#!/bin/python3

correctSentence = "TuuuuUUuuuuuuutuuuuuuutuuuuuuuUUUUUUTUTTUUUUUUUUTttt"
trySentence =     "Pwoiiiiiiinnnnnnnnnnnnnnoiiiiiiiiiiiiiinnnnnnnnnnnnn"

def main() -> None:
    res = 0
    if (len(correctSentence) != len(trySentence)):
        print("Correct sentence and try must have the same lenght")
    for i in range(len(correctSentence)):
        if (correctSentence[i].lower() != trySentence[i].lower()):
            res += abs(ord(correctSentence[i].lower()) - ord(trySentence[i].lower()))
    print(res)

if __name__ == "__main__":
    main()
