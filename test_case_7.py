import subprocess
import re

def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None

def check_queue_initialization(nvme_device="/dev/nvme0"):
    # Run `nvme id-ctrl` command to get controller properties
    cmd = f"sudo nvme id-ctrl {nvme_device}"
    output = run_command(cmd)
    
    if output is None:
        print("Failed to retrieve NVMe controller info.")
        return

    # Parse for Submission Queue Entry Size (SQES) and Completion Queue Entry Size (CQES)
    sqes_match = re.search(r"sqes\s+:\s+0x(\w+)", output)
    cqes_match = re.search(r"cqes\s+:\s+0x(\w+)", output)

    if sqes_match and cqes_match:
        sqes = int(sqes_match.group(1), 16)
        cqes = int(cqes_match.group(1), 16)
        print(f"Submission Queue Entry Size (SQES): {sqes}")
        print(f"Completion Queue Entry Size (CQES): {cqes}")
        
        # Validate queue sizes based on expected controller setup
        if sqes == 0x66 and cqes == 0x44:
            print("Queues are correctly initialized with the expected entry sizes.")
        else:
            print("Queue initialization error: Unexpected SQ or CQ entry size.")
    else:
        print("Could not find SQES or CQES information.")

    # Additional I/O test to validate queue functionality
    print("Running I/O test to validate queue functionality...")
    fio_command = (
        "sudo fio --filename=/dev/nvme0n1 --name=queue_test "
        "--rw=randread --bs=4k --numjobs=4 --time_based --runtime=10 --group_reporting"
    )
    fio_output = run_command(fio_command)
    
    if fio_output:
        print("I/O test completed successfully, indicating that queues are functional.")
    else:
        print("I/O test failed, suggesting an issue with queue functionality.")

if __name__ == "__main__":
    check_queue_initialization()
