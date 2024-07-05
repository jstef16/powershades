import socket
import time

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# seconds
timeout = 5
udp_socket.settimeout(timeout)

# Specify the server address and port
server_address = ("192.168.1.80", 42)

crc_max = 65535

percentages = {
    0: "8fff",
    1: "5cb8",
    2: "2970",
    3: "fa37",
    4: "e2f0",
    5: "31b7",
    6: "447f",
    7: "9738",
    8: "55e1",
    9: "86a6",
    10: "f36e",
    11: "2029",
    12: "38ee",
    13: "eba9",
    14: "9e61",
    15: "4d26",
    16: "3bc2",
    17: "e885",
    18: "9d4d",
    19: "4e0a",
    20: "56cd",
    21: "858a",
    22: "f042",
    23: "2305",
    24: "e1dc",
    25: "329b",
    26: "4753",
    27: "9414",
    28: "8cd3",
    29: "5f94",
    30: "2a5c",
    31: "f91b",
    32: "e784",
    33: "34c3",
    34: "410b",
    35: "924c",
    36: "8a8b",
    37: "59cc",
    38: "2c04",
    39: "ff43",
    40: "3d9a",
    41: "eedd",
    42: "9b15",
    43: "4852",
    44: "5095",
    45: "83d2",
    46: "f61a",
    47: "255d",
    48: "53b9",
    49: "80fe",
    50: "f536",
    51: "2671",
    52: "3eb6",
    53: "edf1",
    54: "9839",
    55: "4b7e",
    56: "89a7",
    57: "5ae0",
    58: "2f28",
    59: "fc6f",
    60: "e4a8",
    61: "37ef",
    62: "4227",
    63: "9160",
    64: "5f09",
    65: "8c4e",
    66: "f986",
    67: "2ac1",
    68: "3206",
    69: "e141",
    70: "9489",
    71: "47ce",
    72: "8517",
    73: "5650",
    74: "2398",
    75: "f0df",
    76: "e818",
    77: "3b5f",
    78: "4e97",
    79: "9dd0",
    80: "eb34",
    81: "3873",
    82: "4dbb",
    83: "9efc",
    84: "863b",
    85: "557c",
    86: "20b4",
    87: "f3f3",
    88: "312a",
    89: "e26d",
    90: "97a5",
    91: "44e2",
    92: "5c25",
    93: "8f62",
    94: "faaa",
    95: "29ed",
    96: "3772",
    97: "e435",
    98: "91fd",
    99: "42ba",
    100: "5a7d",
}
results = {}

for percent in percentages.keys():
    print(f"Starting percentage {percent}")
    hex_percent = hex(percent)[2:].rjust(2, "0")

    hex_crc = percentages.get(percent)
    middle_index = len(hex_crc) // 2
    hex_crc = hex_crc[:middle_index] + " " + hex_crc[middle_index:]
    hex_data = f"0a 00 {hex_crc} 1a 0d 00 00 01 00 {hex_percent} 00 00 00 00 00 00 00"
    data_to_send = bytes.fromhex(hex_data)

    try:
        # Send data
        udp_socket.sendto(data_to_send, server_address)
        response = None

        # Wait for a response (if necessary)
        while response is None or response[4] != 26:
            response, server = udp_socket.recvfrom(50439)
        print(f"CRC {hex_crc} was valid for {percent}")
        # Wait for shade to move
        time.sleep(3)

        # Check shade's state is the correct percentage
        getState = "0a00898f1d0d000001000000000000000000"
        udp_socket.sendto(bytes.fromhex(getState), server_address)

        while response[4] != 29:
            response, server = udp_socket.recvfrom(50439)
        print(f"Received {percent}% state check response {response}")
        # for i in range(len(response), 0, -1):
        #     print(f"{i-1}: {response[i-1]}")
    except socket.timeout:
        print(
            f"Timeout: No response received for {percent}% for crc {hex_crc} after {timeout} seconds."
        )
        results[percent] = f"Percent {percent} may have invalid CRC {hex_crc}"
    except (socket.error, OSError) as e:
        print(f"Error: {e}")
        print("Closing socket after failing")
        udp_socket.close()

print("Closing socket on success")
udp_socket.close()
print(results)
exit()
