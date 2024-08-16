import json
import subprocess

def run_fio_test(test_name, rw_type, filename, runtime=60):
    command = [
        'fio',
        f'--name={test_name}',
        '--ioengine=libaio',
        f'--rw={rw_type}',
        '--bs=4k',
        '--numjobs=1',
        f'--runtime={runtime}',
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

    # Extract job runtime, total bytes transferred, and calculate throughput
    job_runtime_s = output['jobs'][0]['job_runtime'] / 1000  # Convert ms to seconds
    if rw_type in ['randread', 'read']:
        total_bytes = output['jobs'][0]['read']['total_bytes']
    else:
        total_bytes = output['jobs'][0]['write']['total_bytes']

    # Calculate throughput in MB/s
    throughput = total_bytes / (job_runtime_s * 1024 * 1024)
    iops = output['jobs'][0][rw_type]['iops']

    return job_runtime_s, total_bytes, throughput, iops

def main():
    filename = '/dev/nvme0n1'  # Path to NVMe device
    
    # Define expected performance metrics for comparison (MB/s)
    expected_metrics = {
        "random_read": 100,  # Replace with expected random read throughput in MB/s
        "random_write": 100, # Replace with expected random write throughput in MB/s
        "sequential_read": 500,  # Replace with expected sequential read throughput in MB/s
        "sequential_write": 500  # Replace with expected sequential write throughput in MB/s
    }
    
    # Run tests
    tests = [
        ("random-read-test", "randread", "random_read"),
        ("random-write-test", "randwrite", "random_write"),
        ("sequential-read-test", "read", "sequential_read"),
        ("sequential-write-test", "write", "sequential_write")
    ]
    
    for test_name, rw_type, metric_key in tests:
        runtime, total_bytes, throughput, iops = run_fio_test(test_name, rw_type, filename, runtime=60)
        
        # Print test results
        print(f"\n{test_name.capitalize()}:")
        print(f"Total Bytes: {total_bytes / (1024 * 1024):.2f} MB")
        print(f"Throughput: {throughput:.2f} MB/s")
        print(f"IOPS: {iops:.2f}")
        
        # Compare with expected metrics
        expected_throughput = expected_metrics[metric_key]
        print(f"Expected Throughput: {expected_throughput} MB/s")
        print(f"Status: {'Meets expectation' if throughput >= expected_throughput else 'Below expectation'}")

if __name__ == "__main__":
    main()
