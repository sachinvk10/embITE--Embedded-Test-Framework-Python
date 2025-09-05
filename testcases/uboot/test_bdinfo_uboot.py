import pytest
from board_action.connection_handler import ConnectionHandler

@pytest.fixture(scope="module")
def connection():
    conn = ConnectionHandler()
    shell = conn.detect_shell()
    if shell != "uboot":
        pytest.skip("Not in U-Boot shell, skipping U-Boot tests.")
    yield conn
    conn.close()

def test_bdinfo_uboot(connection):
    connection.send_command("bdinfo")
    output = connection.read_response()
    assert "Board" in output or "info" in output.lower(), "bdinfo failed or no output"
    print(output)

def test_memcheck_uboot(connection):
    connection.send_command("memcheck")
    output = connection.read_response()
    assert "mem" in output.lower(), "memcheck failed or no output"
    print(output)

