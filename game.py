#!/usr/bin/env python3

import random
import time
import os

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def progress_bar(remaining, total=7):
    bar = "█" * remaining + "░" * (total - remaining)
    return f"{CYAN}{bar}{RESET} {remaining}/{total}"


def draw_header(attempt, total=7):
    clear()
    print(f"{BOLD}{'─' * 42}{RESET}")
    print(f"{BOLD}       NUMBER GUESSING GAME{RESET}")
    print(f"{BOLD}{'─' * 42}{RESET}")
    print(f"  Attempts left: {progress_bar(attempt, total)}")
    print(f"{'─' * 42}\n")


def main():
    start = time.perf_counter()
    number = random.randint(1, 100)
    total = 7
    attempt = total
    attemptCount = 0
    lowerBound, upperBound = 1, 100
    message = ""

    clear()
    print(f"{BOLD}{'─' * 42}{RESET}")
    print(f"{BOLD}       NUMBER GUESSING GAME{RESET}")
    print(f"{BOLD}{'─' * 42}{RESET}")
    print(f"\n  Guess a number between 1 and 100.")
    print(f"  You have {total} attempts.\n")
    input("  Press Enter to start...")

    while attempt != 0:
        draw_header(attempt, total)

        if attemptCount > 0:
            print(f"  {YELLOW}Hint: It's between {lowerBound} and {upperBound}.{RESET}\n")

        if message:
            print(f"  {message}\n")

        userInput = input("  Your guess: ").strip()
        if not userInput.isdigit():
            message = f"{YELLOW}Please enter a valid whole number.{RESET}"
            continue

        attempt -= 1
        attemptCount += 1
        guess = int(userInput)

        if guess == number:
            draw_header(attempt, total)
            print(f"  {GREEN}{BOLD}Correct! The number was {number}.")
            print(f"  You got it in {attemptCount} attempt(s).{RESET}\n")
            break
        elif guess < number:
            lowerBound = max(lowerBound, guess + 1)
            message = f"{RED}Too low! The number is greater than {guess}.{RESET}"
        else:
            upperBound = min(upperBound, guess - 1)
            message = f"{RED}Too high! The number is less than {guess}.{RESET}"

        if attempt == 0:
            draw_header(0, total)
            print(f"  {RED}{BOLD}Out of attempts! The number was {number}.{RESET}\n")
            break

    end = time.perf_counter()
    print(f"  {CYAN}Time: {end - start:.1f}s{RESET}\n")


def play():
    while True:
        main()
        replay = input(f"  {BOLD}Play again? (y/n):{RESET} ").strip().lower()
        if replay != 'y':
            clear()
            print(f"  {BOLD}Thanks for playing. BYE!{RESET}\n")
            break


play()
