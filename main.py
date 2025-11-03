# АВТОМАТ ДЛЯ КАВИИ!!!!!!!!!!!!!!
import time
from pathlib import Path
from random import randint
from datetime import datetime

class jumpBackToMain(Exception): pass

POSITIONS_POS = Path('things') / 'positions.txt'
ADDITIONS_POS = Path('things') / 'additions.txt'
LOG_DIR_POS = Path("Logs")

def getTotal() -> float:
    logPos = LOG_DIR_POS / 'log.txt'
    total = 0
    with open(logPos, 'r') as log:
        for n, line in enumerate(log.readlines()):
            line = line.strip().split()
            if line[-1][-1] == '$':
                line = line[-1][:-1]
                try:
                    line = float(line)
                except ValueError:
                    logEvent(f"Couldn't read price payed at line {n}", error=True, errorMsg="Could not calculate total price!")
                    continue
                total += line
    logEvent(f"Calculated total price! ({total}$)")
    return total





def loadThings(position: Path) -> dict:

    """load positions and additions to them from a file"""

    thing = {}
    errorEvent = ''

    with open(position, 'r') as thg:
        for n, line in enumerate(thg.readlines()):
            line = line.strip()
            name, price = line.split()[0:2]
            price = price.replace(',', '.')
            try:
                price = float(price)
            except ValueError:
                errorEvent += f"Couldn't read price at line {n}\n{price=}{line=}\n"
                continue
            thing[name] = price

    if errorEvent:
        logEvent(errorEvent, error=True, errorMsg="Could not read price from file!")

    return thing


def safeInput(variants: dict = None, yesno: bool = False, message: str = "") -> bool | str:
    """Input(), but if something goes wrong, it doesn't break anything"""

    positions = len(variants) if variants is not None else 0
    while True:
        printMenu(variants)
        userInput = input(f"{message}")
        if userInput == 'q':
            jumpToMain()
        if userInput == 'ihatecoffee':
            print("ok, then no coffee for you >:)))")
            time.sleep(0.5)
            exit(0)
        if userInput == 'calculate':
            print(f"Total earnings: {getTotal()}$")
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
            print(f"({i}: {thing} - {price}$)")

def jumpToMain() -> None:

    """Jumps back to the beginning of the program"""

    print("Returning to main menu...")
    time.sleep(0.5)
    raise jumpBackToMain

def calculatePrice(positions: dict, additions: dict, order: list[str]) -> float:

    """Calculates a total price of an order logs it"""

    totalPrice = 0
    for n in order:
        totalPrice += positions.get(n, 0) + additions.get(n, 0)
    return totalPrice




def logEvent(event: str, error: bool = False, errorMsg: str = None, criticalError: bool = False) -> None:

    """Logs any event you want in a simple txt file"""

    LOG_DIR_POS.mkdir(parents=True, exist_ok=True)
    if not event:
        return


    if error | criticalError:
        error_pos = LOG_DIR_POS / f"[{str(datetime.now())[:22]}].txt".replace(':', '-')
        if errorMsg:
            if criticalError:
                print(errorMsg)
            logEvent(f'ERROR! {errorMsg}{'.' if errorMsg[-1] != '.' else ''} Created error report file at {error_pos}.')
        else:
            logEvent(f'ERROR! Created error report file at {error_pos}')

        with open(error_pos, "a") as errorFile:
            errorFile.write(event + '\n')
            errorFile.flush()
        return

    with open(LOG_DIR_POS / "log.txt", "a") as logFile:
        logFile.write(f"[{str(datetime.now())[:22]}] "+ event + '\n')
        logFile.flush()
    return # so it does it immediately (it does not)

def main():
    """The main program"""
    try:
        POSITIONS = loadThings(POSITIONS_POS)
        ADDITIONS = loadThings(ADDITIONS_POS)
    except FileNotFoundError as e:
        notFoundDir = str(e).split()[-1]
        print()
        logEvent(f"Not found {notFoundDir}", criticalError=True, errorMsg=f"Couldn't find file with such directory: {notFoundDir}")
        exit(3)

    print(f"Welcome! Make your order, please.")
    time.sleep(0.5)
    coffee = safeInput(POSITIONS, message=f"Enter a number between 1 and {len(POSITIONS)}, please: ")
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
    priceToPay = calculatePrice(POSITIONS, ADDITIONS, totalOrder)
    time.sleep(0.2)
    print(f"For you to pay: {priceToPay}$")
    time.sleep(randint(3, 6))
    if randint(0, 100) > 99:
        logEvent("Could not process payment", error=True, errorMsg="OOPS! Payment failed! No drink for you today >:)")
        time.sleep(3)
        exit(1)
    else:
        print("Payment succesfull! Enjoy your drink!")
        logEvent(f"Customer bought {totalOrder} for {priceToPay}$")
    time.sleep(5)

if __name__ == "__main__":
    while True:
        try:
            main()
        except jumpBackToMain:
            pass
        except KeyboardInterrupt:
            pass
