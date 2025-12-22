import socket
import struct

from config import IP
from dmx import turn_off


turn_off(controller_ip=IP, universe=0)
