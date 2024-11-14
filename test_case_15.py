import subprocess
import re

def run_fio_test(test_name, rw_type, block_size="4k", size="1G", runtime="60"):
    # Construct the fio command with the specified parameters
    fio_command = [
        "fio", 
        f"--name={test_name}", 
        f"--rw={rw_type}", 
        f"--bs={block_size}", 
        f"--size={size}", 
        "--numjobs=1", 
        "--time_based", 
        f"--runtime={runtime}", 
        "--group_reporting"
    ]

    try:
        # Run the fio command and capture the output
        result = subprocess.run(fio_command, capture_output=True, text=True)
        
        # Check if the command was successful
        if result.returncode != 0:
            print(f"Error running {test_name} test: {result.stderr}")
            return None
        
        # Extract throughput information using a regular expression
        throughput_match = re.search(r'bw=([\d.]+)([A-Z]+)', result.stdout)
        if throughput_match:
            throughput = throughput_match.group(1)
            unit = throughput_match.group(2)
            print(f"{test_name} ({rw_type}) Throughput: {throughput} {unit}")
            return float(throughput), unit
        else:
            print(f"No throughput found for {test_name} test.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Run sequential and random tests
run_fio_test("Sequential_Read", "read")
run_fio_test("Sequential_Write", "write")
run_fio_test("Random_Read", "randread")
run_fio_test("Random_Write", "randwrite")
