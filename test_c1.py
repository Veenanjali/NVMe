import subprocess
import pytest


def get_nvme_initialization_messages():
    try:
        # Run 'dmesg' command and capture output
        dmesg_output = subprocess.check_output(["sudo", "dmesg"], text=True)

        # Filter lines containing 'nvme'
        nvme_init_msgs = [line for line in dmesg_output.splitlines() if 'nvme' in line]
        return nvme_init_msgs

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return []


#@pytest.mark.skipif("os.geteuid() != 0", reason="Requires root privileges")
def test_nvme_initialization():

    nvme_init_msgs = get_nvme_initialization_messages()
    nvme_init_str = '\n'.join(nvme_init_msgs)
    print("OUTPUT:",nvme_init_str)

    assert nvme_init_msgs, "No NVMe initialization messages found in dmesg output."
    assert any("pci function" in msg for msg in nvme_init_msgs), \
        "Expected NVMe PCI function message not found."
    assert any("queues" in msg for msg in nvme_init_msgs), \
        "Expected NVMe queue message not found."

    print("NVMe Initialization completed successfully with expected messages.")
