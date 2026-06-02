#!/usr/bin/env python3

import random
import time
from dataclasses import dataclass, field

# ── Constants ────────────────────────────────────────────────────────────────
MIN_NUMBER = 1
MAX_NUMBER = 100

DIFFICULTIES = {
    "1": ("Easy",   10),
    "2": ("Medium",  5),
    "3": ("Hard",    3),
}

# ── Colors ───────────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


# ── State ────────────────────────────────────────────────────────────────────
@dataclass
class GameState:
    number:        int
    total:         int
    attempts_left: int
    attempt_count: int   = 0
    lower_bound:   int   = MIN_NUMBER
    upper_bound:   int   = MAX_NUMBER
    message:       str   = ""


# ── UI helpers ────────────────────────────────────────────────────────────────
def clear() -> None:
    """Clear the terminal using ANSI escape codes (no subprocess)."""
    print("\033[2J\033[H", end="", flush=True)


def progress_bar(remaining: int, total: int) -> str:
    bar = "█" * remaining + "░" * (total - remaining)
    return f"{CYAN}{bar}{RESET} {remaining}/{total}"


def draw_header(state: GameState) -> None:
    clear()
    print(f"{BOLD}{'─' * 42}{RESET}")
    print(f"{BOLD}       NUMBER GUESSING GAME{RESET}")
    print(f"{BOLD}{'─' * 42}{RESET}")
    print(f"  Attempts left: {progress_bar(state.attempts_left, state.total)}")
    print(f"{'─' * 42}\n")


# ── Difficulty selection ──────────────────────────────────────────────────────
def choose_difficulty() -> tuple[str, int]:
    """Prompt the player to choose a difficulty; return (name, attempts)."""
    clear()
    print(f"{BOLD}{'─' * 42}{RESET}")
    print(f"{BOLD}       NUMBER GUESSING GAME{RESET}")
    print(f"{BOLD}{'─' * 42}{RESET}")
    print(f"\n  Select difficulty:\n")
    for key, (name, attempts) in DIFFICULTIES.items():
        print(f"    {key}. {name:<8} ({attempts} attempts)")
    print()

    while True:
        choice = input("  Your choice (1/2/3): ").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print(f"  {YELLOW}Enter 1, 2, or 3.{RESET}")


# ── Core game loop ────────────────────────────────────────────────────────────
def play_round() -> None:
    diff_name, total = choose_difficulty()
    state = GameState(
        number=random.randint(MIN_NUMBER, MAX_NUMBER),
        total=total,
        attempts_left=total,
    )

    clear()
    print(f"{BOLD}{'─' * 42}{RESET}")
    print(f"{BOLD}       NUMBER GUESSING GAME{RESET}")
    print(f"{BOLD}{'─' * 42}{RESET}")
    print(f"\n  Difficulty : {diff_name}")
    print(f"  Guess a number between {MIN_NUMBER} and {MAX_NUMBER}.")
    print(f"  You have {total} attempts.\n")
    input("  Press Enter to start...")

    start = time.perf_counter()

    while state.attempts_left > 0:
        draw_header(state)

        if state.attempt_count > 0:
            print(f"  {YELLOW}Hint: between {state.lower_bound} and {state.upper_bound}.{RESET}\n")

        if state.message:
            print(f"  {state.message}\n")

        user_input = input("  Your guess: ").strip()

        # ── Validation ──────────────────────────────────────────────────────
        if not user_input.lstrip("-").isdigit():
            state.message = f"{YELLOW}Please enter a valid whole number.{RESET}"
            continue

        guess = int(user_input)

        if not (MIN_NUMBER <= guess <= MAX_NUMBER):
            state.message = (
                f"{YELLOW}Please enter a number between "
                f"{MIN_NUMBER} and {MAX_NUMBER}.{RESET}"
            )
            continue                         # ← does NOT cost an attempt

        # ── Valid guess: deduct attempt now ──────────────────────────────────
        state.attempt_count += 1

        if guess == state.number:
            # Deduct AFTER confirming win so header shows correct remaining count
            draw_header(state)
            print(f"  {GREEN}{BOLD}Correct! The number was {state.number}.")
            print(f"  You got it in {state.attempt_count} attempt(s).{RESET}\n")
            break

        state.attempts_left -= 1

        if guess < state.number:
            state.lower_bound = max(state.lower_bound, guess + 1)
            state.message = f"{RED}Too low! Greater than {guess}.{RESET}"
        else:
            state.upper_bound = min(state.upper_bound, guess - 1)
            state.message = f"{RED}Too high! Less than {guess}.{RESET}"

        if state.attempts_left == 0:
            draw_header(state)
            print(f"  {RED}{BOLD}Out of attempts! The number was {state.number}.{RESET}\n")

    elapsed = time.perf_counter() - start
    print(f"  {CYAN}Time: {elapsed:.1f}s{RESET}\n")


# ── Replay loop ───────────────────────────────────────────────────────────────
def play() -> None:
    while True:
        play_round()
        replay = input(f"  {BOLD}Play again? (y/n): {RESET}").strip().lower()
        if replay != "y":
            clear()
            print(f"  {BOLD}Thanks for playing. BYE!{RESET}\n")
            break


if __name__ == "__main__":
    play()
