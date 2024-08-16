import subprocess
import time
import pytest

def perform_controller_reset():
    # Perform a controller reset using nvme-cli (requires root privileges)
    print("\nSimulating NVMe controller reset...")
    subprocess.run(['sudo', 'nvme', 'reset', '/dev/nvme0'], check=True)

def check_dmesg_for_reset():
    # Check if the controller reset is present in dmesg logs
    print("\nChecking dmesg logs for controller reset...")
    result = subprocess.run("sudo dmesg | grep nvme", capture_output=True, text=True,shell=True)
    #print(result)
    # Filter for controller reset related logs
    reset_logs = [line for line in result.stdout.splitlines() if "resetting controller" in line.lower()]
    
    if reset_logs:
        print("\nController reset detected in dmesg:")
        for log in reset_logs:
            print(log)
        return True
    else:
        print("\nController reset not found in dmesg.")
        return False

def check_queue_reinitialization():
    # Check if queues are reinitialized after the reset
    print("\nChecking if NVMe queues are reinitialized...")
    result = subprocess.run("sudo dmesg | grep nvme", capture_output=True, text=True,shell=True)
    # Filter for queue reinitialization logs
    queue_logs = [line for line in result.stdout.splitlines() if "read/poll queues" in line.lower()]
    
    if queue_logs:
        print("\nQueue reinitialization detected in dmesg:")
        for log in queue_logs:
            print(log)
        return True
    else:
        print("Queue reinitialization not detected.")
        return False

def test_controller_reset_recovery():
    # Run an I/O test (for example, fio) to simulate normal operation
    fio_process = subprocess.Popen(['fio', '--name=test', '--rw=randwrite', '--ioengine=libaio', '--bs=4k', '--numjobs=4', '--iodepth=32', '--runtime=60', '--direct=1', '--filename=/dev/nvme0n1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Simulate a controller reset while fio is running
    perform_controller_reset()

    # Allow some time for the reset and reinitialization to complete
    time.sleep(5)

    # Check if the controller reset is logged in dmesg
    assert check_dmesg_for_reset(), "Controller reset not found in dmesg"

    # Check if the queues are reinitialized
    assert check_queue_reinitialization(), "Queue reinitialization not detected in dmesg"

    # Check if fio encounters any errors after the reset
    stdout, stderr = fio_process.communicate()
    if "I/O error" in stderr.decode():
        print("I/O error detected after reset. Testing recovery.")
        # Check if the device is back online
        recovery_test = subprocess.run(['lsblk', '/dev/nvme0n1'], capture_output=True, text=True)
        assert recovery_test.returncode == 0, "Device not accessible after reset"
        print("Device successfully reinitialized.")
    else:
        print("\nI/O operations were successful after controller reset.")

# Run the test with pytest
if __name__ == "__main__":
    pytest.main()
