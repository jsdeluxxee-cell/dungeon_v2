import os
import time

width = 20
height = 10

ball = {
    "x": 0,
    "y": 0,
    "dx": 1,
    "dy": 1
}

while True:

    os.system("cls")

    for y in range(height):

        row = ""

        for x in range(width):

            if x == ball["x"] and y == ball["y"]:
                row += "O"

            else:
                row += "."

        print(row)

    ball["x"] += ball["dx"]
    ball["y"] += ball["dy"]

    if ball["x"] <= 0 or ball["x"] >= width - 1:
        ball["dx"] = -ball["dx"]

    if ball["y"] <= 0 or ball["y"] >= height - 1:
        ball["dy"] = -ball["dy"]

    time.sleep(0.1)