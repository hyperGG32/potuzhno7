# АВТОМАТ ДЛЯ КАВИИ!!!!!!!!!!!!!!
import time
from random import randint
from time import sleep

def safeInput(variants: dict = None, yesno: bool = False, message: str = "") -> bool | str:
    """Input(), but if something goes wrong, it doesn't break anything"""

    positions = len(variants) if variants else 0
    while True:
        printMenu(variants)
        userInput = input(f"{message}")
        if userInput == 'q':
            jumpToMain()
        if yesno:
            return userInput == 'y'
        try:
            userInput = int(userInput)
        except ValueError:
            print(f"Enter a number between 1 and {positions}!")
            continue

        if 1 <= userInput <= positions:
            return list(variants)[userInput-1]

        print(f"Enter a number between 1 and {positions}")


def printMenu(variants: dict) -> None:

    """Prints out the price list of something"""

    if variants:
        for i, (thing, price) in enumerate(variants.items(), 1):
            print(f"({i}: {thing} - {price}")

def jumpToMain() -> None:

    """Jumps back to the beginning of the program"""

    print("Returning to main menu...")
    time.sleep(0.5)
    return main(back=True)

def calculatePrice(positions: dict, additions: dict, order: list[str]) -> float:

    """Calculates a total price of an order"""

    totalPrice = 0
    for n in order:
        totalPrice += positions.get(n, 0) + additions.get(n, 0)
    return totalPrice


POSITIONS = {'americano': 2.35, "cappuccino": 3.75, "water": 0.2, "latte": 4}
ADDITIONS = {"milk": 1.25, "veg_milk": 1.45, "syrop": 2.6, "sugar": 0.7}

def main(back=False):
    """The main program"""
    print(f"Welcome{" back" if back else ""}! Make your order, please.")
    time.sleep(0.5)
    coffee = safeInput(POSITIONS, message="Enter a number between 1 and 4, please: ")
    time.sleep(0.1)
    additionsmaybe = safeInput(yesno=True, message="Any additions? (y/n): ")
    time.sleep(0.2)
    additions = []
    if additionsmaybe:
        while True:
            additions.append(safeInput(ADDITIONS, message="Order your additions ;) : "))
            time.sleep(0.2)
            if not safeInput(yesno=True, message="More? (y/n): "):
                break
    totalOrder = additions + [coffee]
    time.sleep(0.2)
    print(f"For you to pay: {calculatePrice(POSITIONS, ADDITIONS, totalOrder)}$")
    time.sleep(randint(3, 6))
    if randint(0, 100) > 99:
        print("OOPS! Payment failed! No drink for you today >:)")
        time.sleep(3)
        exit(1)
    else:
        print("Payment succesfull! Enjoy your drink!")
    time.sleep(5)
    jumpToMain()

if __name__ == "__main__":
    main()
