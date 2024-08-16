import json
import subprocess

def run_fio_test(test_name, rw_type, filename):
    command = [
        'fio',
        f'--name={test_name}',
        '--ioengine=libaio',
        f'--rw={rw_type}',
        '--bs=4k',
        '--numjobs=4',
        '--runtime=60',  # Run for 1 second
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

    # Extract IOPS and handle missing data gracefully
    iops = 0
    if rw_type in ['randread', 'read']:
        iops = output['jobs'][0].get('read', {}).get('iops', 0)
    elif rw_type in ['randwrite', 'write']:
        iops = output['jobs'][0].get('write', {}).get('iops', 0)

    return iops

def main():
    filename = '/dev/nvme0n1'  # Change this to your NVMe device path
    
    # Run tests
    rand_read_iops = run_fio_test("random-read-test", "randread", filename)
    rand_write_iops = run_fio_test("random-write-test", "randwrite", filename)
    seq_read_iops = run_fio_test("sequential-read-test", "read", filename)
    seq_write_iops = run_fio_test("sequential-write-test", "write", filename)

    # Print results
    print("\nResults:")
    print(f"Random Read IOPS: {rand_read_iops:.2f}")
    print(f"Random Write IOPS: {rand_write_iops:.2f}")
    print(f"Sequential Read IOPS: {seq_read_iops:.2f}")
    print(f"Sequential Write IOPS: {seq_write_iops:.2f}")

if __name__ == "__main__":
    main()
