import json 
import subprocess 
import pytest

def run_fio_test():
    command = [
        'fio', 
        '--name=sequential-read-test', 
        '--ioengine=libaio', 
        '--rw=read', 
        '--bs=4k', 
        '--numjobs=1', 
        '--runtime=10', 
        '--iodepth=32', 
        '--direct=1', 
        '--filename=/dev/nvme0n1', 
        '--output-format=json'
    ]
    print("\nRunning sequential read tests on NVMe device")
    
    # Run the Fio command and capture the output
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    
    # Parse the output as JSON
    output = json.loads(result.stdout)
    
    # Extract job runtime, total I/O operations, and IOPS
    job_runtime_ms = output['jobs'][0]['job_runtime']  # Job runtime in milliseconds
    job_runtime_s = job_runtime_ms / 1000  # Convert to seconds
    total_ios = output['jobs'][0]['read']['total_ios']  # Total I/O operations
    iops = output['jobs'][0]['read']['iops']  # IOPS

    # Return the results for use in the test
    return job_runtime_s, total_ios, iops


@pytest.fixture(scope="module", autouse=True)
def fio_test_setup():
    # This fixture will ensure that the fio test is executed before the tests
    print("\nStarting Fio sequential read test...\n")
    yield run_fio_test()
    print("\nFio sequential read test completed.\n")


# Pytest test function to check if random read operation is successful
def test_sequential_read_operation(fio_test_setup):
    # Unpack results from the fixture
    job_runtime_s, total_ios, iops = fio_test_setup
    
    # Check if the results are valid (non-zero)
    assert total_ios > 0, "Total I/O operations should be greater than 0"
    assert iops > 0, "IOPS should be greater than 0"
    
    # Optionally, you can check the runtime to ensure it falls within a reasonable range
    assert job_runtime_s > 0, "Job runtime should be greater than 0 seconds"
    
    # Print the results for the user
    print(f"Job Runtime: {job_runtime_s:.2f} seconds")
    print(f"Total I/O Operations: {total_ios}")
    print(f"I/O Operations Per Second (IOPS): {iops:.2f}")
