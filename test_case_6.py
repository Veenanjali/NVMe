import subprocess
import os

# Configuration
nvme_device = "/dev/nvme0n1"
start_block = 0
block_count = 1
write_file = "test_data.txt"
read_file = "output_data.txt"

# Create a file with data to write to the NVMe device
with open(write_file, "w") as f:
    f.write("test data for nvme testing")
data_size = os.path.getsize(write_file)

# Function to execute shell commands
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {command}\nError: {result.stderr}")
    else:
        print(result.stdout)
    return result.returncode == 0

# Write data to NVMe device
write_command = (
    f"sudo nvme write {nvme_device} --data={write_file} --data-size={data_size} "
    f"--start-block={start_block} --block-count={block_count}"
)
print("Writing data to NVMe device...")
if not run_command(write_command):
    print("Failed to write data to NVMe device.")
    exit(1)

# Read data back from NVMe device
read_command = (
    f"sudo nvme read {nvme_device} --start-block={start_block} --block-count={block_count} "
    f"--data-size={data_size} --data={read_file}"
)
print("Reading data back from NVMe device...")
if not run_command(read_command):
    print("Failed to read data from NVMe device.")
    exit(1)

# Verify data integrity by comparing files
print("Verifying data integrity...")
with open(write_file, "r") as f1, open(read_file, "r") as f2:
    write_data = f1.read()
    read_data = f2.read()[:data_size]  # Trim read_data to the actual data size

print("Write Data:", repr(write_data))
print("Read Data:", repr(read_data))

if write_data == read_data:
    print("Data integrity test passed: Data read matches data written.")
else:
    print("Data integrity test failed: Data read does not match data written.")

# Cleanup
#os.remove(write_file)
#os.remove(read_file)
