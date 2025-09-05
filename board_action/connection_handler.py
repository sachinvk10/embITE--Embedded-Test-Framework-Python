import serial
import telnetlib
import paramiko
import time
import re
import socket
from config.config_loader import config
from loghandler.logger_setup import setup_logger

logger = setup_logger()

class ConnectionHandler:
    def __init__(self):
        self.conn = None
        self.method = config['connection']['method'].lower()
        self.shell_type = None
        self.prompt_patterns = {
            "uboot": [r"=>", r"U-Boot>", r"u-boot>"],
            "linux": [r"\$", r"#"]
        }

        logger.info(f"Initializing connection handler for method: {self.method}")
        self.connect()

    def connect(self):
        try:
            if self.method == "serial":
                self.conn = self._connect_serial()
            elif self.method == "ssh":
                self.conn = self._connect_ssh()
            elif self.method == "telnet":
                self.conn = self._connect_telnet()
            else:
                raise ValueError(f"Unsupported connection method: {self.method}")
            logger.info(f"{self.method.capitalize()} connection established successfully.")
        except Exception as e:
            logger.exception(f"Failed to connect using {self.method}: {e}")
            raise

    def _connect_serial(self):
        port = config['connection']['port']
        baudrate = config['connection'].get('baudrate', 115200)
        timeout = config['connection'].get('timeout', 1)

        logger.debug(f"Connecting to serial port {port} with baudrate {baudrate}")
        return serial.Serial(port, baudrate, timeout=timeout)

    def _connect_ssh(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        host = config['connection']['host']
        port = config['connection'].get('port', 22)
        username = config['connection']['username']
        password = config['connection']['password']

        logger.debug(f"Connecting to SSH at {host}:{port} as {username}")
        ssh.connect(host, port=port, username=username, password=password, timeout=10)
        self.ssh_shell = ssh.invoke_shell()
        return ssh

    def _connect_telnet(self):
        host = config['connection']['host']
        port = config['connection'].get('port', 23)
        logger.debug(f"Connecting to Telnet at {host}:{port}")
        tn = telnetlib.Telnet(host, port)
        return tn

    def send_command(self, command):
        logger.debug(f"Sending command: {command}")
        if self.method == "serial":
            self.conn.write((command + "\n").encode())
        elif self.method == "ssh":
            self.ssh_shell.send(command + "\n")
        elif self.method == "telnet":
            self.conn.write(command.encode("ascii") + b"\n")

    def read_response(self, timeout=2):
        logger.debug("Reading response...")
        time.sleep(timeout)
        output = ""

        try:
            if self.method == "serial":
                while self.conn.in_waiting:
                    output += self.conn.read(self.conn.in_waiting).decode(errors="ignore")
            elif self.method == "ssh":
                if self.ssh_shell.recv_ready():
                    output += self.ssh_shell.recv(65535).decode(errors="ignore")
            elif self.method == "telnet":
                output += self.conn.read_very_eager().decode(errors="ignore")
        except Exception as e:
            logger.warning(f"Error reading response: {e}")

        logger.debug(f"Command response: {output.strip()}")
        return output.strip()

    def detect_shell(self):
        logger.info("Detecting active shell prompt...")
        self.send_command("")  # Trigger prompt
        response = self.read_response(timeout=1)

        for shell_type, patterns in self.prompt_patterns.items():
            for pattern in patterns:
                if re.search(pattern, response):
                    logger.info(f"Detected {shell_type.upper()} shell with prompt: '{pattern}'")
                    self.shell_type = shell_type
                    return shell_type

        logger.warning(f"Unknown or unsupported shell: '{response}'")
        self.shell_type = "unknown"
        return "unknown"

    def close(self):
        logger.info("Closing connection")
        try:
            if self.method == "serial":
                self.conn.close()
            elif self.method == "ssh":
                self.ssh_shell.close()
                self.conn.close()
            elif self.method == "telnet":
                self.conn.close()
        except Exception as e:
            logger.warning(f"Error while closing connection: {e}")

