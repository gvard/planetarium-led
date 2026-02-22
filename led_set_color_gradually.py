"""
Gradually increase the brightness of given color of the LED lighting.
Example usage: python led_set_color_gradually.py maxlight desc 1 -s 300
"""

from argparse import ArgumentParser

from config import IP, PXL_NUM, COLORS
from dmx import fade_to_color


parser = ArgumentParser(
    description="Python script for working with an LED lighting controller"
)
parser.add_argument("color", type=str, default="white",
                    help="Set color name")
parser.add_argument("mode", type=str, default="asc",
                    help="Set mode: ascending (asc) or descending (desc)")
parser.add_argument("delay", type=float, default=5,
                    help="Set delay in seconds, default is 5")
parser.add_argument("-s", "--steps", type=int, default=200,
                    help="Set the number of steps, default is 200")
args = parser.parse_args()


if __name__ == "__main__":
    if args.color in COLORS:
        COLOR = COLORS[args.color]
    else:
        print("Unknown color, switch to white")
        COLOR = COLORS["white"]
    fade_to_color(COLOR, controller_ip=IP, num_pixels=PXL_NUM, mode=args.mode, fade_steps=args.steps, delay=args.delay)
