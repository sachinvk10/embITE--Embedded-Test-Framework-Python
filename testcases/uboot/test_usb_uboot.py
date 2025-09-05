import pytest
from board_action.connection_handler import ConnectionHandler

conn = None

@pytest.fixture(scope="module", autouse=True)
def setup_connection():
    global conn
    conn = ConnectionHandler()
    shell = conn.detect_shell()
    if shell != "uboot":
        pytest.skip("Not in U-Boot shell, skipping U-Boot tests.")
    yield
    conn.close()

def test_new_uboot_feature():
    conn.send_command("usb start")
    output = conn.read_response()
    # Add your asserts here based on expected output
    assert "bus" in output, "Test failed: expected output not found"
    print(output)

