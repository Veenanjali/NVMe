import subprocess
import time

def perform_controller_reset():
    # Perform a controller reset using nvme-cli (requires root privileges)
    print("Simulating NVMe controller reset...")
    subprocess.run(['sudo', 'nvme', 'reset', '/dev/nvme0'], check=True)

def test_controller_reset_recovery():
    # Run an I/O test (for example, fio) to simulate normal operation
    fio_process = subprocess.Popen(['fio', '--name=test', '--rw=randwrite', '--ioengine=libaio', '--bs=4k', '--numjobs=4', '--iodepth=32', '--runtime=60', '--direct=1', '--filename=/dev/nvme0n1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Simulate a controller reset while fio is running
    perform_controller_reset()

    # Allow some time for the reset and reinitialization to complete
    time.sleep(5)

    # Check if fio encounters any errors after the reset
    stdout, stderr = fio_process.communicate()
    if "I/O error" in stderr.decode():
        print("I/O error detected after reset. Testing recovery.")
        # Check if the device is back online
        recovery_test = subprocess.run(['lsblk', '/dev/nvme0n1'], capture_output=True, text=True)
        assert recovery_test.returncode == 0, "Device not accessible after reset"
        print("Device successfully reinitialized.")
    else:
        print("I/O operations were successful after controller reset.")
