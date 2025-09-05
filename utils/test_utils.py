import pytest
from config.config_loader import get_test_prompt_mode

def skip_if_prompt_mismatch(shell: str):
    mode = get_test_prompt_mode()
    if mode == "uboot" and shell != "uboot":
        pytest.skip(f"Skipping because config test_prompt_mode=uboot but detected shell is '{shell}'")
    elif mode == "linux" and shell != "linux":
        pytest.skip(f"Skipping because config test_prompt_mode=linux but detected shell is '{shell}'")

