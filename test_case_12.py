import json
import subprocess

def run_fio_test(test_name, rw_type, filename):
    command = [
        'fio',
        f'--name={test_name}',
        '--ioengine=libaio',
        f'--rw={rw_type}',
        '--bs=4k',
        '--numjobs=1',
        '--runtime=10',
        '--iodepth=32',
        '--direct=1',
        f'--filename={filename}',
        '--output-format=json',
        #'--write_bw_log=log_write',  # Log write bandwidth
        #'--write_iops_log=log_iops',  # Log IOPS
        #'--write_lat_log=log_lat'     # Log latency
    ]
    
    print(f"Running {test_name} on NVMe device...")

    # Run the Fio command and capture the output
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    
    # Parse the output as JSON
    output = json.loads(result.stdout)

    # Print the output to inspect its structure
    #print(json.dumps(output, indent=4))  # Pretty-print the JSON output

    # Extract job runtime, total I/O operations, IOPS, and latency
    job_runtime_ms = output['jobs'][0]['job_runtime']  # Job runtime in milliseconds
    job_runtime_s = job_runtime_ms / 1000  # Convert to seconds

    # Use 'read' and 'write' keys correctly based on operation type
    if rw_type in ['randread', 'read']:
        total_ios = output['jobs'][0]['read']['total_ios'] if 'read' in output['jobs'][0] else 0
        iops = output['jobs'][0]['read']['iops'] if 'read' in output['jobs'][0] else 0
        latency = output['jobs'][0]['read']['latency']['mean'] if 'latency' in output['jobs'][0]['read'] else 0
    else:
        total_ios = output['jobs'][0]['write']['total_ios'] if 'write' in output['jobs'][0] else 0
        iops = output['jobs'][0]['write']['iops'] if 'write' in output['jobs'][0] else 0
        latency = output['jobs'][0]['write']['latency']['mean'] if 'latency' in output['jobs'][0]['write'] else 0

    return job_runtime_s, total_ios, iops, latency

def main():
    filename = '/dev/nvme0n1'  # Change this to your NVMe device path
    
    # Run tests
    seq_read_runtime, seq_read_ios, seq_read_iops, seq_read_latency = run_fio_test("sequential-read-test", "read", filename)
    seq_write_runtime, seq_write_ios, seq_write_iops, seq_write_latency = run_fio_test("sequential-write-test", "write", filename)
    rand_read_runtime, rand_read_ios, rand_read_iops, rand_read_latency = run_fio_test("random-read-test", "randread", filename)
    rand_write_runtime, rand_write_ios, rand_write_iops, rand_write_latency = run_fio_test("random-write-test", "randwrite", filename)

    # Print results
    print("\nResults:")
    print(f"Sequential Read: {seq_read_ios} I/O operations, {seq_read_iops:.2f} IOPS in {seq_read_runtime:.2f} seconds, Latency: {seq_read_latency:.2f} ms")
    print(f"Sequential Write: {seq_write_ios} I/O operations, {seq_write_iops:.2f} IOPS in {seq_write_runtime:.2f} seconds, Latency: {seq_write_latency:.2f} ms")
    print(f"Random Read: {rand_read_ios} I/O operations, {rand_read_iops:.2f} IOPS in {rand_read_runtime:.2f} seconds, Latency: {rand_read_latency:.2f} ms")
    print(f"Random Write: {rand_write_ios} I/O operations, {rand_write_iops:.2f} IOPS in {rand_write_runtime:.2f} seconds, Latency: {rand_write_latency:.2f} ms")

    # Compare results
    print("\nComparison:")
    print(f"Sequential Read vs Random Read: {'Sequential Read is faster' if seq_read_iops > rand_read_iops else 'Random Read is faster'}")
    print(f"Sequential Write vs Random Write: {'Sequential Write is faster' if seq_write_iops > rand_write_iops else 'Random Write is faster'}")

if __name__ == "__main__":
    main()
