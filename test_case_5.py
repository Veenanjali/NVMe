import os
import subprocess

# Define the device and mount point
device = '/dev/nvme0n1'
mount_point = '/mnt/nvme0'
file_path = os.path.join(mount_point, 'test_file.txt')
file_content = "Test data for verification."

# Function to format the device as ext4
def format_device():
    print(f"Formatting {device} as ext4...")
    subprocess.run(['sudo', 'mkfs.ext4', '-F', device], check=True)

# Function to mount the device
def mount_device():
    print(f"Mounting {device} to {mount_point}...")
    os.makedirs(mount_point, exist_ok=True)
    subprocess.run(['sudo', 'mount', device, mount_point], check=True)

# Function to write a file to the mounted device
def write_file():
    with open(file_path, 'w') as f:
        f.write(file_content)
    print("\n<---Write operation successfully completed--->\n")

# Function to read the file from the mounted device
def read_file():
    with open(file_path, 'r') as f:
        content = f.read()
    print("\n<---Read operation successfully completed--->\n")

# Function to unmount the device
def unmount_device():
    print(f"Unmounting {mount_point}...")
    subprocess.run(['sudo', 'umount', mount_point], check=True)

# Main execution
def main():
    format_device()
    mount_device()
    write_file()
    read_file()
    unmount_device()

if __name__ == "__main__":
    main()
