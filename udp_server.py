import socket
import sqlite3
from sqlite3 import Error


class UdpServer:
    SERVER_IP_ADDRESS = "127.0.0.1"
    SERVER_PORT_NUMBER = 5678
    BUFFER_SIZE = 1024

    def __init__(self):
        # Create a datagram socket
        self.udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind to address and ip
        self.udp_server_socket.bind((self.SERVER_IP_ADDRESS, self.SERVER_PORT_NUMBER))
        print("UDP server up and listening")

        # Database connection
        self.conn = None

    def create_database_connection(self):
        try:
            self.conn = sqlite3.connect('sensordata.db')
        except Error as e:
            print(e)

        sql_create_temperature_table = """CREATE TABLE IF NOT EXISTS TEMPERATURE(
                                            LOG_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                            SENSOR_ID INT NOT NULL,
                                            TIME TEXT NOT NULL,
                                            TEMPERATURE INT NOT NULL
                                        );"""

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_create_temperature_table)
        except Error as e:
            print(e)

    def collect_sensor_data(self):
        bytesAddressPair = self.udp_server_socket.recvfrom(self.BUFFER_SIZE)

        received_message = bytesAddressPair[0].decode()
        client_address = bytesAddressPair[1]
        print(f"Received from client {client_address} with message: {received_message}")

        sensor_log_time, temperature = received_message.split(",")

        # assume to take the client port number as sensor id
        sensor_id = client_address[1]

        # save sensor data into sqlite database
        log_data = f"{sensor_id}, '{sensor_log_time}', {temperature}"
        sql_insert_into_table = f"INSERT INTO TEMPERATURE (SENSOR_ID, TIME, TEMPERATURE) VALUES ({log_data})"
        print(sql_insert_into_table)
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_insert_into_table)
            self.conn.commit()
        except Error as e:
            print(e)


if __name__ == '__main__':

    udpServer = UdpServer()
    udpServer.create_database_connection()

    while True:
        udpServer.collect_sensor_data()
