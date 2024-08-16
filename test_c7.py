import subprocess
import re
import pytest

# Helper function to run shell commands and capture the output
def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Error executing command: {e}")  # Fail the test on command failure

# Function to check queue initialization
def get_queue_sizes(nvme_device="/dev/nvme0"):
    # Run `nvme id-ctrl` command to get controller properties
    cmd = f"sudo nvme id-ctrl {nvme_device}"
    output = run_command(cmd)
    
    # Parse for Submission Queue Entry Size (SQES) and Completion Queue Entry Size (CQES)
    sqes_match = re.search(r"sqes\s+:\s+0x(\w+)", output)
    cqes_match = re.search(r"cqes\s+:\s+0x(\w+)", output)

    if sqes_match and cqes_match:
        sqes = int(sqes_match.group(1), 16)
        cqes = int(cqes_match.group(1), 16)
        return sqes, cqes
    else:
        pytest.fail("Could not find SQES or CQES information.")  # Fail the test if values are not found

# Pytest test to check queue initialization
def test_queue_initialization():
    sqes, cqes = get_queue_sizes("/dev/nvme0")
    
    # Assert that the queues are initialized by verifying non-zero sizes
    assert sqes != 0, f"\nSubmission Queue Entry Size (SQES) is not initialized, found: {sqes}"
    assert cqes != 0, f"\nCompletion Queue Entry Size (CQES) is not initialized, found: {cqes}"

    # If both assert statements pass, it means queues are initialized correctly
    print(f"Submission Queue Entry Size (SQES): {sqes}")
    print(f"Completion Queue Entry Size (CQES): {cqes}")
