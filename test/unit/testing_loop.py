"""Simple test loop for sending user inputted keys"""
from keystroker.sendkeys import sendkeys

print("Testing SendKeys...")

while True:
    line = input("Please input text to print: ")
    sendkeys(line)

    print("\n")
