#!/usr/bin/env python3

import random
import time



def main():
    start = time.perf_counter()
    number = random.randint(1, 100)
    attempt = 7
    attemptCount = 0
    lowerBound, upperBound = 1, 100
    print(
        f"I'm thinking of a number between 1 and 100.\nYou have {attempt} chances to guess the correct number.\n")

    while attempt != 0:
        if (attempt < 7):
            print(f" Hint: It's between {lowerBound} and {upperBound}.\n")

        userInput = input("Please Guess the number:\t")
        userInput = userInput.strip()
        if not userInput.isdigit():
            continue
        attempt -= 1
        attemptCount += 1
        print("attempt left: ", attempt)
        guess = int(userInput)
        if guess == number:
            print(f"Congratulations! You guessed the correct number in {attemptCount} attempt(s).")
            break
        elif guess < number:
            lowerBound = max(lowerBound, guess + 1)
            print("Incorrect! The number is greater than", guess)
        else:
            upperBound = min(upperBound, guess - 1)
            print("Incorrect! The number is less than", guess)
        if attempt == 0:
            print(
                f"Oh no, you are out of attempts. The correct number was {number}. GOOD BYE \n")
            break

    end = time.perf_counter()
    elapsed = end - start
    print(f" Time took: {elapsed:.1f} seconds")


def play():
    while True:
        main()
        replay = input("Play Again? (y/n): ").strip().lower()
        if replay != 'y':
            print("BYE!")
            break


play()
