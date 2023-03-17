import numpy as np
from pandas import DataFrame, read_csv
from os import environ as envs
from os import chdir, getcwd, makedirs
from time import sleep, strftime
from datetime import datetime
from dotenv import load_dotenv
from os import system, path
from .colorization import *
from natsort import natsorted, ns
from typing import List, Tuple
import logging

def clear(): Color.ResetAll; system('cls||clear'); Color.ResetAll

def date_str_to_timestamp(_date_str):
    _date_format = '%d.%m.%Y'

    return int(datetime.strptime(_date_str, _date_format).timestamp())

def getUserInput(promptText):
    print()

    userInput = input(greenLight(promptText) + cyanLight(" (type ") + yellowLight("e") + cyanLight(" or ") + yellowLight("q") + cyanLight(" to exit)") + greenLight(": "))

    if userInput == "e" or userInput == "q" or userInput == "exit" or userInput == "quit": quit()

    return str(userInput)

def wrongInput():
    print()
    print(redLight("This is not a valid number, please try again.")), sleep(1.5)

def pickOneFromTheList(header, item_list):
    if not item_list:
        return

    hypens = "-" * (len(header) + 5)

    while True:
        print()
        print(yellowLight(hypens))
        print(yellowLight("|"), greenLight(header), yellowLight("|"))
        print(yellowLight(hypens))

        for i in range(len(item_list)):
            item = item_list[i]
            number_color = magentaLight
            item_color = white if i % 2 else cyanLight
            line = f"{number_color(i + 1)}) {item_color(item)}"
            print(line)

        print()

        user_input = input(
            f"{greenLight('Enter a number between ')}"
            f"{magentaLight('1-' + str(len(item_list)))}"
            f"{white(' (')}"
            f"{cyanLight('type ')}"
            f"{yellowLight('e')}"
            f"{cyanLight(' or ')}"
            f"{yellowLight('q')}"
            f"{cyanLight(' to exit')}"
            f"{white(')')}"
            f"{greenLight(': ')}"
        ).lower()

        if user_input in ("e", "q", "exit", "quit"):
            print(redLight("Terminating..."))
            sleep(0.5)
            quit()

        if not user_input.isnumeric():
            wrongInput()
            continue

        user_input = int(user_input)

        if user_input <= 0 or user_input > len(item_list):
            wrongInput()
        else:
            break

    return item_list[user_input - 1]

if __name__ == "__main__":
    header = "Header"
    item_list = ["Item 1", "Item 2", "Item 3"]
    pickOneFromTheList(header, item_list)
