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
    print(f"Running {rw} test on {filename} with block size {bs}")
    
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    output = json.loads(result.stdout)
    
    # Extract relevant data from the FIO output
    iops = output['jobs'][0]['write']['iops'] if rw in ['randwrite', 'write'] else output['jobs'][0]['read']['iops']
    job_runtime_ms = output['jobs'][0]['job_runtime']
    job_runtime_s = job_runtime_ms / 1000  # Convert to seconds
    
    io_ops = output['jobs'][0]['read']['ioops'] if rw in ['read', 'randread'] else output['jobs'][0]['write']['ioops']
    latency_ms = output['jobs'][0]['read']['lat_ns'] / 1e6 if rw in ['read', 'randread'] else output['jobs'][0]['write']['lat_ns'] / 1e6
    
    return job_runtime_s, iops, io_ops, latency_ms

# Run tests for different I/O operations
@pytest.mark.parametrize("operation, rw, expected_rw, filename", [
    ('Sequential Read', 'read', 'seq read', '/mnt/nvme0/test_file'),
    ('Random Read', 'randread', 'rand read', '/mnt/nvme0/test_file'),
    ('Sequential Write', 'write', 'seq write', '/mnt/nvme0/test_file'),
    ('Random Write', 'randwrite', 'rand write', '/mnt/nvme0/test_file')
])
def test_io_operations(operation, rw, expected_rw, filename):
    runtime_s, iops, io_ops, latency_ms = run_fio_test(ioengine="libaio", rw=rw, bs="4k", numjobs=1, iodepth=32,
                                                       filename=filename, size="1G", runtime=10)
    
    # Print out the results for each test for comparison
    print(f"Running {operation} test on {filename} with block size 4k")
    print(f"{operation}: {io_ops} I/O operations, {iops:.2f} IOPS in {runtime_s:.2f} seconds, Latency: {latency_ms:.2f} ms")
    
    # Return results for further comparison
    return io_ops, iops, latency_ms, operation

# Function to compare IOPS and latency
def test_best_io_operation():
    operations = [
        ('Sequential Read', 'read', 'seq read', '/mnt/nvme0/test_file'),
        ('Random Read', 'randread', 'rand read', '/mnt/nvme0/test_file'),
        ('Sequential Write', 'write', 'seq write', '/mnt/nvme0/test_file'),
        ('Random Write', 'randwrite', 'rand write', '/mnt/nvme0/test_file')
    ]

    results = []
    
    # Run tests for all operations and collect results
    for operation, rw, expected_rw, filename in operations:
        runtime_s, iops, io_ops, latency_ms = run_fio_test(ioengine="libaio", rw=rw, bs="4k", numjobs=1, iodepth=32,
                                                           filename=filename, size="1G", runtime=10)
        results.append((operation, iops, io_ops, latency_ms))
        print(f"{operation}: {io_ops} I/O operations, {iops:.2f} IOPS in {runtime_s:.2f} seconds, Latency: {latency_ms:.2f} ms")
    
    # Compare IOPS and latency to find the best operations
    sequential_ops = [result for result in results if 'Read' in result[0] and 'Sequential' in result[0]]
    random_ops = [result for result in results if 'Read' in result[0] and 'Random' in result[0]]

    seq_read = sequential_ops[0]
    rand_read = random_ops[0]
    seq_write = [result for result in results if 'Write' in result[0] and 'Sequential' in result[0]][0]
    rand_write = [result for result in results if 'Write' in result[0] and 'Random' in result[0]][0]

    # Comparison logic for best performance
    print("\nComparison:")
    print(f"Sequential Read vs Random Read: {'Random Read is faster' if rand_read[1] > seq_read[1] else 'Sequential Read is faster'}")
    print(f"Sequential Write vs Random Write: {'Random Write is faster' if rand_write[1] > seq_write[1] else 'Sequential Write is faster'}")
