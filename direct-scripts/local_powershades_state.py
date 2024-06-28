import socket

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# seconds
timeout = 0.1
udp_socket.settimeout(timeout)

# Specify the server address and port
server_address = ('192.168.1.80', 42)


#crc_max = 65535
crc_max = 35215

# def determine_percent_from_bytes(bytes[] bytes):
#     hex = bytes.hex()


for i in range(crc_max, -1, -1):
    
    hex_crc = hex(i)[2:].rjust(4, "0")
    middle_index = len(hex_crc) // 2
    hex_crc = hex_crc[:middle_index] + " " + hex_crc[middle_index:]
    hex_data = f'0a 00 {hex_crc} 1d 0d 00 00 01 00 00 00 00 00 00 00 00 00'
    data_to_send = bytes.fromhex(hex_data)
    
    try:
        # Send data
        udp_socket.sendto(data_to_send, server_address)

        # Wait for a response (if necessary)
        response, server = udp_socket.recvfrom(50439)
        print(f'CRC {hex_crc} was valid with response: {response}')
        current_percent = response[8]
        print(f'Current percentage is: {current_percent}%')
        print('Closing socket on success')
        udp_socket.close()
        exit()
    except socket.timeout:
        print(f"Timeout: No response received for crc {i} after {timeout} seconds.")
    except (socket.error, OSError) as e:
        print(f"Error: {e}")
    # finally:
        # Close the socket
print('Closing socket after failing')
udp_socket.close()

# print('Exiting')