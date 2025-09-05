#!/usr/bin/python3

import os
import sys
import pytest
from datetime import datetime
from config.config_loader import get_test_prompt_mode, config
from board_action.connection_handler import ConnectionHandler
from loghandler.logger_setup import setup_logger
from utils.email_utils import send_email_with_report

logger = setup_logger()

def get_test_dirs(shell_type, mode):
    """
    Return list of test directories based on detected shell and test mode config.
    """
    base_dir = os.path.abspath("testcases")
    test_dirs = []

    if mode in ["uboot", "both"] and shell_type == "uboot":
        test_dirs.append(os.path.join(base_dir, "uboot"))
    if mode in ["linux", "both"] and shell_type == "linux":
        test_dirs.append(os.path.join(base_dir, "linux"))

    return test_dirs

def run_tests(test_dirs):
    """
    Run pytest on given test directories with HTML report generation.
    Returns the path to the generated HTML report.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join("reports", f"test_report_{timestamp}.html")

    pytest_args = test_dirs + [
        f"--html={report_file}",
        "--self-contained-html",
        "-v"
    ]

    logger.info(f"Running pytest with arguments: {pytest_args}")
    pytest.main(pytest_args)
    return report_file

def get_latest_file(folder_path, extension=None):
    """
    Return the latest file from folder_path optionally filtered by extension.
    """
    try:
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                 if os.path.isfile(os.path.join(folder_path, f))]
        if extension:
            files = [f for f in files if f.endswith(extension)]
        if not files:
            return None
        latest_file = max(files, key=os.path.getmtime)
        return latest_file
    except FileNotFoundError:
        logger.warning(f"Folder not found: {folder_path}")
        return None

def main():
    logger.info("Test framework started.")

    try:
        # Get test mode (uboot/linux/both) from config
        mode = get_test_prompt_mode()
        logger.info(f"Test mode from config: {mode}")

        # Initialize connection handler and detect shell
        conn = ConnectionHandler()
        shell_type = conn.detect_shell()

        if shell_type == "unknown":
            logger.error("Unable to detect shell prompt. Exiting.")
            return

        logger.info(f"Detected shell type: {shell_type}")

        # Get test directories to run
        test_dirs = get_test_dirs(shell_type, mode)
        if not test_dirs:
            logger.warning("No test directories match current shell and mode. Exiting.")
            return

        # Run pytest and get path of HTML report
        report_file = run_tests(test_dirs)
        logger.info(f"Test run complete. Report generated at: {report_file}")

        # Find latest log file in logs folder
        log_file = get_latest_file("logs", extension=".log")
        if log_file:
            logger.info(f"Latest log file found: {log_file}")
        else:
            logger.warning("No log files found in logs folder.")

        # Send email with report and log attached
        send_email_with_report(config, report_file, log_file)
        logger.info("Email with test report sent successfully (if configured).")

    except Exception as e:
        logger.exception(f"Exception occurred during test execution: {e}")

if __name__ == "__main__":
    # Ensure current working directory is in sys.path for imports
    sys.path.append(os.getcwd())
    main()

