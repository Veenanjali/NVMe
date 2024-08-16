import json
import subprocess
import pytest

# Run the FIO test and return performance metrics
def run_fio_test(ioengine, rw, bs, numjobs, iodepth, filename, size, runtime):
    command = [
        'fio',
        '--name=test',
        '--ioengine=' + ioengine,
        '--rw=' + rw,
        '--bs=' + bs,
        '--numjobs=' + str(numjobs),
        '--runtime=' + str(runtime),
        '--iodepth=' + str(iodepth),
        '--direct=1',
        '--filename=' + filename,
        '--size=' + size,
        '--output-format=json'
    ]
    print(f"\nRunning {rw} test on {filename} with block size {bs}")
    
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    output = json.loads(result.stdout)
    
    # Extract relevant data from the FIO output
    job_runtime_ms = output['jobs'][0]['job_runtime']
    job_runtime_s = job_runtime_ms / 1000  # Convert to seconds
    
    if rw in ['read', 'randread']:
        io_ops = output['jobs'][0]['read']['total_ios']
        iops = output['jobs'][0]['read']['iops']
    else:  # write operations
        io_ops = output['jobs'][0]['write']['total_ios']
        iops = output['jobs'][0]['write']['iops']
    
    return job_runtime_s, iops, io_ops


# Function to compare IOPS and determine the best read and write operation
def test_best_io_operation():
    operations = [
        ('Sequential Read', 'read', '/mnt/nvme0/test_file'),
        ('Random Read', 'randread', '/mnt/nvme0/test_file'),
        ('Sequential Write', 'write', '/mnt/nvme0/test_file'),
        ('Random Write', 'randwrite', '/mnt/nvme0/test_file')
    ]

    read_results = []
    write_results = []

    # Run tests for all operations and collect results directly
    for operation, rw, filename in operations:
        runtime_s, iops, io_ops = run_fio_test(ioengine="libaio", rw=rw, bs="4k", numjobs=1, iodepth=32,
                                                filename=filename, size="1G", runtime=10)
        
        # Print out the results for each test for comparison
        print(f"Running {operation} test on {filename} with block size 4k")
        print(f"{operation}: {io_ops} I/O operations, {iops:.2f} IOPS in {runtime_s:.2f} seconds")

        # Store results in appropriate lists based on read/write type
        if rw in ['read', 'randread']:
            read_results.append((iops, operation))
        else:
            write_results.append((iops, operation))
    
    # Sort results by IOPS in descending order to get the best performance
    read_results.sort(reverse=True, key=lambda x: x[0])
    write_results.sort(reverse=True, key=lambda x: x[0])
    
    # The best read operation based on IOPS
    best_read_iops, best_read_operation = read_results[0]
    print(f"\nBest read operation based on IOPS: {best_read_operation} with {best_read_iops:.2f} IOPS")
    
    # The best write operation based on IOPS
    best_write_iops, best_write_operation = write_results[0]
    print(f"\nBest write operation based on IOPS: {best_write_operation} with {best_write_iops:.2f} IOPS")
