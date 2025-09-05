import pytest
from board_action.connection_handler import ConnectionHandler
from utils.test_utils import skip_if_prompt_mismatch

@pytest.fixture(scope="module")
def conn():
    handler = ConnectionHandler()
    shell = handler.detect_shell()
    skip_if_prompt_mismatch(shell)
    if shell != "linux":
        pytest.skip("Detected shell is not Linux, skipping Linux tests")
    yield handler
    handler.close()

def test_eth_linux(conn):
    conn.send_command("ifconfig")
    response = conn.read_response()
    assert "eth0" in response and "ID" in response

