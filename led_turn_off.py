import socket
import struct

# ArtNet packet structure for DMX (OpCode 0x5000 for output/input)
def create_artnet_dmx_packet(universe=0, dmx_data=b'\x00'*512):
    """
    Creates an ArtNet DMX packet to send.
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

# Function to turn off LEDs (send all zeros)
def turn_off_leds(controller_ip=None, universe=0, port=6454):
    """
    Sends an ArtNet DMX packet with all channels set to 0 to turn off LEDs.
    - controller_ip: IP address of the controller (if None, broadcast to all)
    - universe: ArtNet universe (default 0)
    - port: ArtNet port (default 6454)
    """
    # Create DMX data: all 512 channels to 0 (RGB 0-255, etc.)
    dmx_data = b'\x00' * 512  # 512 bytes of zeros

    packet = create_artnet_dmx_packet(universe=universe, dmx_data=dmx_data)

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcast

    # If no specific IP, broadcast to Art-Net subnet (255.255.255.255 is default)
    if controller_ip is None:
        controller_ip = '255.255.255.255'  # Broadcast

    try:
        sock.sendto(packet, (controller_ip, port))
        print(f"ArtNet DMX packet sent to {controller_ip}:{port} to turn off LEDs.")
    except Exception as e:
        print(f"Error sending packet: {e}")
    finally:
        sock.close()

# Set controller_ip to your device's IP:
turn_off_leds(controller_ip=None, universe=0)