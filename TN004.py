import subprocess

def verify_nvme_driver(expected_driver):
    try:
        # Execute the lspci command to get PCI devices and their drivers
        lspci_output = subprocess.check_output(["lspci", "-k"], text=True)
        #print("OUTPUT:\n", lspci_output)

        # Split the output into lines for easier processing
        lines = lspci_output.splitlines()

        # Track whether the NVMe device and its driver were found
        nvme_device_found = False
        driver_found = False
        actual_driver = None
        nvme_lines = []

        # Loop through the lines to find the NVMe controller and its driver
        for i in range(len(lines)):
            # Look for NVMe controllers
            if "Non-Volatile memory controller" in lines[i]:
                nvme_device_found = True
                nvme_lines.append(lines[i])
                print(f"\nDetected NVMe controller: {lines[i]}")

                # Look in the next few lines for driver information
                for j in range(i + 1, min(i + 4, len(lines))):
                    if "Kernel driver in use" in lines[j]:
                        actual_driver = lines[j].split(":")[-1].strip()
                        print(f"\nActual driver found: {actual_driver}")

                        # Check if the actual driver matches the expected driver
                        if actual_driver == expected_driver:
                            driver_found = True
                        break  # Exit inner loop once we've found the driver info

        if nvme_lines:
            print("\nFiltered NVMe Output:")
            for line in nvme_lines:
                print(line)
        else:
            print("No NVMe controller found.")

        # Return the verification result
        return nvme_device_found, driver_found, actual_driver

    except subprocess.CalledProcessError as e:
        print(f"Error executing lspci: {e}")
        return False, False, None

# Test function to verify the NVMe driver using pytest
def test_verify_nvme_driver():
    expected_driver = "nvme"  # Expected NVMe driver

    # Call the function to get results
    nvme_device_found, driver_found, actual_driver = verify_nvme_driver(expected_driver)
    
    # Assertions for pytest
    assert nvme_device_found, "No NVMe controller found in the system."
    assert driver_found, f"Expected driver '{expected_driver}' not found. Actual driver: '{actual_driver}'"
    assert actual_driver == expected_driver, f"Driver mismatch: Expected '{expected_driver}', but found '{actual_driver}'"
    print(f"Assertion passed: NVMe driver '{actual_driver}' is correctly loaded.")
