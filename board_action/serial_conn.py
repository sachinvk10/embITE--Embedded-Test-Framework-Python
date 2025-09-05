import time
import serial
from loghandler.logger_setup import setup_logger
from config.config_loader import load_config

class SerialConnection:
    def __init__(self):
        self.config = load_config()
        self.logger = setup_logger()
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = serial.Serial(
                port=self.config["serial_port"],
                baudrate=self.config["baud_rate"],
                timeout=self.config["timeout"]
            )
            time.sleep(2)
            self.conn.reset_input_buffer()
            self.logger.info("Serial connection established.")
        except serial.SerialException as e:
            self.logger.error(f"Serial connection failed: {e}")
            raise

    def send_command(self, cmd):
        self.logger.debug(f"Sending command via Serial: {cmd}")
        self.conn.write((cmd + "\n").encode())
        time.sleep(0.5)

    def read_response(self, timeout=2):
        self.conn.timeout = timeout
        output = self.conn.read_until(b'# ', 1024).decode(errors='ignore')
        self.logger.debug(f"Serial response:\n{output}")
        return output.strip()

    def close(self):
        self.logger.info("Closing Serial connection...")
        try:
            self.conn.close()
            self.logger.info("Serial connection closed.")
        except Exception as e:
            self.logger.error(f"Error closing Serial connection: {e}")

