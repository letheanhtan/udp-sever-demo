import random
import socket
import time


class UdpClient:
    SERVER_IP_ADDRESS = "127.0.0.1"
    SERVER_PORT_NUMBER = 5678
    BUFFER_SIZE = 1024
    SERVER_ADDRESS_PORT = (SERVER_IP_ADDRESS, SERVER_PORT_NUMBER)

    def __init__(self):
        # Create a UDP socket at client side
        self.udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def send_sensor_data(self):
        start_time = time.time()
        while True:
            # send temperature log every 2 seconds
            # random temperature value between 20 and 40
            time.sleep(2.0 - ((time.time() - start_time) % 2.0))
            current_time = time.strftime("%d/%m/%Y-%H:%M:%S", time.localtime())
            sensor_temperature = random.randint(20, 40)

            send_message = f"{current_time},{sensor_temperature}"

            # Send to server using created UDP socket
            self.udp_client_socket.sendto(str(send_message).encode(), self.SERVER_ADDRESS_PORT)
            print(f"Send to server message: {send_message}")


if __name__ == '__main__':
    udpClient = UdpClient()
    udpClient.send_sensor_data()
