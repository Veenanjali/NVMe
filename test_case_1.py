import subprocess


def check_nvme_initialization():
    try:
        dmesg_output = subprocess.check_output(
            ["sudo", "-S", "dmesg"],
            input="debian" + "\n",  # Provide the password
            text=True
        )

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
