import time
import paramiko
from loghandler.logger_setup import setup_logger
from config.config_loader import load_config

class SSHConnection:
    def __init__(self):
        self.config = load_config()
        self.logger = setup_logger()
        self.conn = None
        self.shell = None
        self.connect()

    def connect(self):
        try:
            self.conn = paramiko.SSHClient()
            self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.conn.connect(
                hostname=self.config["ssh_host"],
                port=self.config.get("ssh_port", 22),
                username=self.config["ssh_user"],
                password=self.config["ssh_password"],
                timeout=self.config.get("timeout", 2)
            )
            self.shell = self.conn.invoke_shell()
            time.sleep(1)
            self.logger.info("SSH connection established.")
        except Exception as e:
            self.logger.error(f"SSH connection failed: {e}")
            raise

    def send_command(self, cmd):
        self.logger.debug(f"Sending command via SSH: {cmd}")
        self.shell.send(cmd + "\n")
        time.sleep(0.5)

    def read_response(self, timeout=2):
        time.sleep(timeout)
        output = ""
        while self.shell.recv_ready():
            output += self.shell.recv(1024).decode(errors='ignore')
        self.logger.debug(f"SSH response:\n{output}")
        return output.strip()

    def close(self):
        self.logger.info("Closing SSH connection...")
        try:
            self.conn.close()
            self.logger.info("SSH connection closed.")
        except Exception as e:
            self.logger.error(f"Error closing SSH connection: {e}")

