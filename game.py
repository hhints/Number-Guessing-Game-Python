#!/usr/bin/env python3

import random
import time
import os

GREEN   = "\033[92m"
RED     = "\033[91m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
MAGENTA = "\033[95m"
BLUE    = "\033[94m"
ORANGE  = "\033[38;5;208m"
WHITE   = "\033[97m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
RESET   = "\033[0m"


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def progress_bar(remaining, total=7):
    if remaining > 4:
        color = GREEN
    elif remaining > 2:
        color = YELLOW
    else:
        color = RED
    filled = "█" * remaining
    empty  = f"{DIM}░{RESET}" * (total - remaining)
    return f"{color}{BOLD}{filled}{RESET}{empty} {color}{remaining}/{total}{RESET}"


def draw_header(attempt, total=7):
    clear()
    print(f"{MAGENTA}{BOLD}{'═' * 42}{RESET}")
    print(f"{CYAN}{BOLD}    🎯  NUMBER GUESSING GAME  🎯{RESET}")
    print(f"{MAGENTA}{BOLD}{'═' * 42}{RESET}")
    print(f"  {WHITE}Attempts left:{RESET} {progress_bar(attempt, total)}")
    print(f"{BLUE}{'─' * 42}{RESET}\n")


def main():
    start = time.perf_counter()
    number = random.randint(1, 100)
    total = 7
    attempt = total
    attemptCount = 0
    lowerBound, upperBound = 1, 100
    message = ""

    clear()
    print(f"{MAGENTA}{BOLD}{'═' * 42}{RESET}")
    print(f"{CYAN}{BOLD}    🎯  NUMBER GUESSING GAME  🎯{RESET}")
    print(f"{MAGENTA}{BOLD}{'═' * 42}{RESET}")
    print(f"\n  {WHITE}I'm thinking of a number between {YELLOW}1{WHITE} and {YELLOW}100{WHITE}.{RESET}")
    print(f"  {WHITE}You have {GREEN}{BOLD}{total}{RESET}{WHITE} attempts to guess it.{RESET}\n")
    print(f"{BLUE}{'─' * 42}{RESET}")
    input(f"\n  {DIM}Press Enter to start...{RESET}")

    while attempt != 0:
        draw_header(attempt, total)

        if attemptCount > 0:
            print(f"  {YELLOW}💡 Hint: It's between {BOLD}{lowerBound}{RESET}{YELLOW} and {BOLD}{upperBound}{RESET}{YELLOW}.{RESET}\n")

        if message:
            print(f"  {message}\n")

        userInput = input(f"  {CYAN}{BOLD}Your guess:{RESET} ").strip()
        if not userInput.isdigit():
            message = f"{YELLOW}⚠️  Please enter a valid whole number.{RESET}"
            continue

        attempt -= 1
        attemptCount += 1
        guess = int(userInput)

        if guess == number:
            draw_header(attempt, total)
            print(f"  {GREEN}{BOLD}🎉 Correct! The number was {number}.{RESET}")
            print(f"  {GREEN}You got it in {BOLD}{attemptCount}{RESET}{GREEN} attempt(s)!{RESET}\n")
            break
        elif guess < number:
            lowerBound = max(lowerBound, guess + 1)
            message = f"{RED}🔺 Too low!  The number is greater than {BOLD}{guess}{RESET}{RED}.{RESET}"
        else:
            upperBound = min(upperBound, guess - 1)
            message = f"{ORANGE}🔻 Too high! The number is less than {BOLD}{guess}{RESET}{ORANGE}.{RESET}"

        if attempt == 0:
            draw_header(0, total)
            print(f"  {RED}{BOLD}💀 Out of attempts! The number was {number}.{RESET}\n")
            break

    end = time.perf_counter()
    print(f"  {DIM}⏱  Time: {end - start:.1f}s{RESET}\n")


def play():
    while True:
        main()
        replay = input(f"  {MAGENTA}{BOLD}Play again? (y/n):{RESET} ").strip().lower()
        if replay != 'y':
            clear()
            print(f"\n  {CYAN}{BOLD}Thanks for playing. BYE! 👋{RESET}\n")
            break


play()
