import json
import subprocess
import pytest

# Function to run the FIO test and capture IOPS
def run_fio_test(test_name, rw_type, filename):
    command = [
        'fio',
        f'--name={test_name}',
        '--ioengine=libaio',
        f'--rw={rw_type}',
        '--bs=4k',
        '--numjobs=4',
        '--runtime=60',  # Run for 1 minute
        '--iodepth=32',
        '--direct=1',
        f'--filename={filename}',
        '--output-format=json'
    ]

    print(f"Running {test_name} on NVMe device...")

    # Run the Fio command and capture the output
    result = subprocess.run(command, capture_output=True, text=True, check=True)

    # Parse the output as JSON
    output = json.loads(result.stdout)

    # Extract IOPS
    iops = 0
    if rw_type in ['randread', 'read']:
        iops = output['jobs'][0].get('read', {}).get('iops', 0)
    elif rw_type in ['randwrite', 'write']:
        iops = output['jobs'][0].get('write', {}).get('iops', 0)

    return iops

# Define pytest test cases
@pytest.mark.parametrize("test_name, rw_type", [
    ("random-read-test", "randread"),
    ("random-write-test", "randwrite", ),
    ("sequential-read-test", "read",),
    ("sequential-write-test", "write")
])
def test_fio_iops(test_name, rw_type):
    filename = '/dev/nvme0n1'  # Change this to your NVMe device path

    # Run the FIO test
    iops = run_fio_test(test_name, rw_type, filename)

    # Assert that the IOPS are above the expected threshold
    print(f"{test_name} - IOPS: {iops}")
    assert iops > 0, f"IOPS for {test_name} is below expected threshold. Actual: {iops}"

