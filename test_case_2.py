import subprocess

def list_nvme_devices():
    try:
        # List NVMe devices
        result = subprocess.run(['sudo','nvme', 'list'], capture_output=True, text=True, check=True)
        print("NVMe Devices:\n")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error listing NVMe devices: {e}")
        return False

def identify_nvme_controller(device):
    try:
        # Send Identify Controller command
        result = subprocess.run(['sudo', 'nvme', 'id-ctrl', device], capture_output=True, text=True, check=True)
        print(f"\nIdentify Controller for {device}:\n")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error sending Identify Controller command: {e}")
        return False

def main():
    # Step 1: List NVMe devices
    if list_nvme_devices():
        # Assuming the first NVMe device is to be tested; you can modify as needed
        nvme_device = "/dev/nvme0"  # Change this if necessary
        
        # Step 2: Identify NVMe controller
        identify_nvme_controller(nvme_device)

if __name__ == "__main__":
    main()
