"""
Launches a running fragment of a given color along an LED strip on a given background color.
"""

import socket
import struct
import time
from argparse import ArgumentParser

from config import IP, PXL_NUM, COLORS
from dmx import turn_off, fade_to_color, run_chasing_fragment


parser = ArgumentParser(
    description="Python script for working with an LED lighting controller"
)
parser.add_argument("color", type=str, default="red",
                    help="Set color name")
parser.add_argument("bkgcolor", type=str, default="blue",
                    help="Set color name")
parser.add_argument("-s", "--steps", type=int, default=200,
                    help="Set the number of steps, default is 200")
parser.add_argument("-b", "--startled", type=int, default=0,
                    help="Set the starting LED number, default is 0")
parser.add_argument("-l", "--length", type=int, default=5,
                    help="Set the number of LEDs in the fragment, default is 5")
parser.add_argument("-d", "--duration", type=int, default=10,
                    help="Set the total time to run the function in seconds, default is 10")
parser.add_argument("-p", "--speed", type=float, default=0.1,
                    help="Set the delay between steps in seconds (lower = faster), default is 0.1")
args = parser.parse_args()


if __name__ == "__main__":
    if args.color in COLORS:
        COLOR = COLORS[args.color]
    else:
        print("Unknown color, switch to red")
        COLOR = COLORS["red"]

    if args.bkgcolor in COLORS:
        BKG_COLOR = COLORS[args.color]
    else:
        print("Unknown color for bkgcolor, switch to blue")
        BKG_COLOR = COLORS["blue"]

    turn_off(controller_ip=IP, universe=0)

    UNIVERSE = 0  # Set the universe manually to control individual LED strips
    run_chasing_fragment(start_led=args.startled, fragment_length=args.length, color=COLOR,
                         background_color=BKG_COLOR, speed=args.speed, duration=args.duration,
                         controller_ip=IP, universe=UNIVERSE, num_pixels=PXL_NUM)

    DELAY = 4
    fade_to_color(COLOR, controller_ip=IP, num_pixels=PXL_NUM, fade_steps=args.steps, delay=DELAY)
