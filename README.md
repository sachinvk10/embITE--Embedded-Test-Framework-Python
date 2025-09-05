<<<<<<< HEAD
Serial Communication Testing Framework
======================================

Overview
--------
This Python framework provides automated testing capabilities for embedded target boards via multiple connection methods: Serial, SSH, and Telnet. It detects whether the target is in U-Boot shell or Linux shell and executes relevant test cases accordingly.

It supports:
- Modular connection handling (serial, ssh, telnet)
- Configurable via JSON file (config/config.json)
- Structured logging with timestamps (console + file)
- Pytest-based test execution with selective runs for U-Boot or Linux shells
- HTML test reports (pytest-html)
- Emailing test reports with logs attached
- Separate test folders for U-Boot and Linux
- Easy extension with new tests and connection methods

Folder Structure
----------------
.
├── board_action/
│   ├── connection_handler.py   # Handles serial/ssh/telnet connections and shell detection
│   └── serial_console.py       # Serial-specific console communication
│
├── config/
│   ├── config.json             # Configuration file with connection, email, and test settings
│   └── config_loader.py        # Loads and parses config.json
│
├── loghandler/
│   └── logger_setup.py         # Logger setup with timestamp formatting
│
├── logs/                      # Log files with timestamps for console and framework logs
│
├── reports/                   # Generated HTML reports and saved logs
│
├── testcases/
│   ├── uboot/
│   │   ├── test_usb_uboot.py          # U-Boot specific USB tests (e.g., nyxes_bdinfo)
│   │   └── conftest.py                 # Shared fixture for U-Boot tests (optional)
│   │
│   ├── linux/
│   │   └── test_usb_linux.py           # Linux specific USB tests (e.g., lsusb)
│   │
│   └── ...                            # Other test folders as needed
│
├── utils/                     # Utility scripts/helpers if any
│
├── main.py                   # Entry point to run tests and send reports
└── README.txt                # This documentation file

Prerequisites
-------------
- Python 3.8+
- Pytest (`pip install pytest`)
- pytest-html (`pip install pytest-html`)
- pyserial (`pip install pyserial`)
- paramiko (`pip install paramiko`) — for SSH support
- telnetlib (built-in) — for Telnet support

Configuration (config/config.json)
----------------------------------
Configure connection details, email settings, and test run mode:

{
  "connection": {
    "method": "serial",             // serial / ssh / telnet
    "serial_port": "/dev/ttyUSB0",
    "baudrate": 115200,
    "timeout": 2,
    "ssh_host": "192.168.1.100",
    "ssh_port": 22,
    "ssh_user": "user",
    "ssh_password": "password",
    "telnet_host": "192.168.1.101",
    "telnet_port": 23,
    "telnet_user": "user",
    "telnet_password": "password"
  },
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "youremail@gmail.com",
    "receiver_email": "receiveremail@gmail.com",
    "email_password": "yourpassword",
    "subject": "Serial Framework Test Report"
  },
  "test_prompt_mode": "both"  // options: "uboot", "linux", "both"
}

Running Tests
-------------
Run the main script which detects the shell, runs tests accordingly, generates HTML reports, and emails the results:

python main.py

Running Pytest Manually
----------------------
To run all tests (both Linux and U-Boot):

pytest testcases/ --html=reports/report.html --self-contained-html

To run only U-Boot tests:

pytest testcases/uboot/ --html=reports/uboot_report.html --self-contained-html

To run only Linux tests:

pytest testcases/linux/ --html=reports/linux_report.html --self-contained-html

Writing Tests
-------------
- Place U-Boot specific tests under testcases/uboot/
- Place Linux specific tests under testcases/linux/
- Use the shared ConnectionHandler to send commands and read responses
- Use pytest fixtures for setup and teardown to reuse connection efficiently
- Example U-Boot test snippet:

def test_nyxes_bdinfo_uboot(uboot_connection):
    uboot_connection.send_command("nyxes_bdinfo")
    output = uboot_connection.read_response()
    assert "Board" in output or "info" in output.lower()

Logging
-------
- Logs with timestamps saved in logs/ folder.
- Console logs also printed with timestamps.
- Logger configuration handled in loghandler/logger_setup.py

Email Reports
-------------
- After test run, HTML report and logs are emailed.
- Email settings configured in config.json.

Extending Framework
-------------------
- Add new connection types by extending board_action/connection_handler.py
- Add new tests as pytest files in appropriate test folders
- Customize prompt detection logic in connection_handler.py

Troubleshooting
---------------
- ModuleNotFoundError: Ensure PYTHONPATH includes project root or run from root directory.
- JSONDecodeError: Validate config.json syntax (commas, brackets).
- Connection errors: Check connectivity and credentials in config.json.
- Shell detection issues: Adjust regex in connection_handler.py for your board prompts.


=======
# embITE--Embedded-Test-Framework-Python
This is a lightweight automation framework designed for validating embedded SoC features (BIOS and OS) such as  UART, GPIO, and I2C . Developed using Python, it supports modular test creation, logging, and HTML reporting.
>>>>>>> 5c9f509c489317b9cb721856a56d27a94bf5028c
