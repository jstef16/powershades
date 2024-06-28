import socket

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# seconds
timeout = 0.1
udp_socket.settimeout(timeout)

# Specify the server address and port
server_address = ('192.168.1.80', 42)

crc_max = 65535

percentages = [79, 78, 77, 76, 74, 73, 72, 71]
results = {}

for percent in percentages:

    print(f'Starting percentage {percent}')
    hex_percent = hex(percent)[2:].rjust(2, "0")

    for i in range(crc_max, -1, -1):
        
        hex_crc = hex(i)[2:].rjust(4, "0")
        middle_index = len(hex_crc) // 2
        hex_crc = hex_crc[:middle_index] + " " + hex_crc[middle_index:]
        hex_data = f'0a 00 {hex_crc} 1a 0d 00 00 01 00 {hex_percent} 00 00 00 00 00 00 00'
        data_to_send = bytes.fromhex(hex_data)
        
        try:
            # Send data
            udp_socket.sendto(data_to_send, server_address)

            # Wait for a response (if necessary)
            response, server = udp_socket.recvfrom(50439)
            results[percent] = f"this.crcMap.set({percent}, '{hex_crc}')"
            print(f'CRC {hex_crc} was valid for {hex_percent} with response:{response}')
        except socket.timeout:
            print(f"Timeout: No response received for {percent}% for crc {i} after {timeout} seconds.")
        except (socket.error, OSError) as e:
            print(f"Error: {e}")
            print('Closing socket after failing')
            udp_socket.close()

print('Closing socket on success')
udp_socket.close()
print(results)
exit()
