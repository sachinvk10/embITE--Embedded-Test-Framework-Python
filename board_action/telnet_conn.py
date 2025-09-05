import time
import telnetlib
from loghandler.logger_setup import setup_logger
from config.config_loader import load_config

class TelnetConnection:
    def __init__(self):
        self.config = load_config()
        self.logger = setup_logger()
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = telnetlib.Telnet(
                self.config["telnet_host"],
                self.config.get("telnet_port", 23),
                timeout=self.config.get("timeout", 2)
            )
            self.conn.read_until(b"login: ")
            self.conn.write(self.config["telnet_user"].encode('ascii') + b"\n")
            self.conn.read_until(b"Password: ")
            self.conn.write(self.config["telnet_password"].encode('ascii') + b"\n")
            time.sleep(1)
            self.logger.info("Telnet connection established.")
        except Exception as e:
            self.logger.error(f"Telnet connection failed: {e}")
            raise

    def send_command(self, cmd):
        self.logger.debug(f"Sending command via Telnet: {cmd}")
        self.conn.write(cmd.encode('ascii') + b"\n")
        time.sleep(0.5)

    def read_response(self, timeout=2):
        time.sleep(timeout)
        output = self.conn.read_very_eager().decode('ascii', errors='ignore')
        self.logger.debug(f"Telnet response:\n{output}")
        return output.strip()

    def close(self):
        self.logger.info("Closing Telnet connection...")
        try:
            self.conn.write(b"exit\n")
            self.conn.close()
            self.logger.info("Telnet connection closed.")
        except Exception as e:
            self.logger.error(f"Error closing Telnet connection: {e}")

