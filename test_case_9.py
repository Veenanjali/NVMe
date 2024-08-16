import json
import subprocess

def run_fio_test():
    command = [
        'fio', 
        '--name=random-write-test',  # Change the job name to indicate it's a write test
        '--ioengine=libaio', 
        '--rw=randwrite',  # Change to randwrite for random writes
        '--bs=4k', 
        '--numjobs=1', 
        '--runtime=10', 
        '--iodepth=32', 
        '--direct=1', 
        '--filename=/dev/nvme0n1', 
        '--output-format=json'
    ]
    print("Running random write tests on NVMe device")
    # Run the Fio command and capture the output
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    
    # Parse the output as JSON
    output = json.loads(result.stdout)
    
    # Extract job runtime, total I/O operations, and IOPS
    job_runtime_ms = output['jobs'][0]['job_runtime']  # Job runtime in milliseconds
    job_runtime_s = job_runtime_ms / 1000  # Convert to seconds
    total_ios = output['jobs'][0]['write']['total_ios']  # Total I/O operations for write
    iops = output['jobs'][0]['write']['iops']  # IOPS for write

    # Print the results
    print(f"Job Runtime: {job_runtime_s:.2f} seconds")
    print(f"Total I/O Operations: {total_ios}")
    print(f"I/O Operations Per Second (IOPS): {iops:.2f}")

if __name__ == "__main__":
    run_fio_test()