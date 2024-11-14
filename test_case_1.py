import subprocess

def check_nvme_initialization():
    try:
        # Run 'dmesg' with sudo, no password required due to sudoers configuration
        dmesg_output = subprocess.check_output(["sudo", "dmesg"], text=True)

        # Check for NVMe initialization messages
        nvme_init_msgs = [line for line in dmesg_output.splitlines() if 'nvme' in line]
        if nvme_init_msgs:
            print("NVMe Initialization completed successfully:")
            for msg in nvme_init_msgs:
                print(msg)
        else:
            print("No NVMe initialization messages found.")

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

check_nvme_initialization()

