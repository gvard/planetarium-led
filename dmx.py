import socket
import struct
import time

 
def create_artnet_dmx_packet(universe=0, dmx_data=b'\x00'*512):
    """
    ArtNet packet structure for DMX (OpCode 0x5000 for output/input)
    - universe: 16-bit (subnet: 0-15 in high 4 bits, universe: 0-15 in low 4 bits); default 0
    - dmx_data: 512 bytes of DMX channel data (0-255 per channel)
    """
    header = b'Art-Net\x00'  # 8 bytes
    opcode = struct.pack('<H', 0x5000)  # Little endian, OpCode for DMX
    version = struct.pack('>H', 14)  # Big endian, Art-Net version 14
    sequence = b'\x00'  # Sequence number (0 for no sequence)
    physical = b'\x00'  # Physical port (0)
    universe_data = struct.pack('<H', universe)  # Little endian universe
    length = struct.pack('>H', 512)  # Big endian length of DMX data (512)

    packet = header + opcode + version + sequence + physical + universe_data + length + dmx_data
    return packet


def send_dmx_packet(sock, controller_ip, port, dmx_data, universe=0):
    packet = create_artnet_dmx_packet(universe=universe, dmx_data=dmx_data)
    sock.sendto(packet, (controller_ip, port))


def turn_off(controller_ip=None, universe=0, port=6454, verbose=False):
    """
    Sends a DMX packet with all channels set to 0 to turn off LEDs.
    - controller_ip: IP address of the controller (if None, broadcast to all)
    - universe: ArtNet universe (default 0)
    - port: ArtNet port (default 6454)
    """
    dmx_data = b'\x00' * 512  # 512 bytes of zeros

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    if not controller_ip:
        controller_ip = '255.255.255.255'

    try:
        send_dmx_packet(sock, controller_ip, port, dmx_data, universe)
        if verbose:
            print("ArtNet DMX packet sent to turn off LEDs.")
    except Exception as e:
        print(f"Error sending packet: {e}")
    finally:
        sock.close()


def fade_to_color(clr, controller_ip=None, port=6454, num_pixels=512//3, fade_steps=200, delay=5, universe=0):
    """
    Gradually changes color to the specified RGB values for all pixels.
    clr must be (r, g, b) tuple: target color values (0-255 each).
    """
    if not all(0 <= val <= 255 for val in clr):
        print("Error: Color values must be between 0 and 255")
        return
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    if not controller_ip:
        controller_ip = '255.255.255.255'

    red, green, blue = clr
    try:
        for step in range(fade_steps + 1):
            r_current = int(red * step / fade_steps)
            g_current = int(green * step / fade_steps)
            b_current = int(blue * step / fade_steps)
            dmx_data = b''.join([bytes([r_current, g_current, b_current]) for _ in range(num_pixels)])
            dmx_data += b'\x00' * (512 - len(dmx_data))
            send_dmx_packet(sock, controller_ip, port, dmx_data, universe)
            time.sleep(delay/100)

        print(f"Faded to color {clr}.")
    except Exception as e:
        print(f"Error during fade to color: {e}")
    finally:
        sock.close()
