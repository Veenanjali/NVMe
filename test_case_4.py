import subprocess

def verify_nvme_driver(expected_driver):
    try:
        # Execute the lspci command to get PCI devices and their drivers
        lspci_output = subprocess.check_output(["lspci", "-k"], text=True)
        print("Full lspci Output:\n", lspci_output)  # Print the full output for debugging purposes

        # Split the output into lines for easier processing
        lines = lspci_output.splitlines()

        # Track whether the NVMe device and its driver were found
        nvme_device_found = False
        driver_found = False
        actual_driver = None

        # Loop through the lines to find the NVMe controller and its driver
        for i in range(len(lines)):
            # Look for NVMe controllers
            if "Non-Volatile memory controller" in lines[i]:
                nvme_device_found = True
                print(f"NVMe Controller Found: {lines[i]}")

                # Look for the next lines for driver information
                for j in range(i + 1, min(i + 4, len(lines))):  # Check next few lines
                    if "Kernel driver in use" in lines[j]:
                        actual_driver = lines[j].split(":")[-1].strip()
                        print(f"Actual NVMe Driver: '{actual_driver}'")  # Debugging output

                        # Check if the actual driver matches the expected driver
                        if actual_driver == expected_driver:
                            driver_found = True
                            print("Driver verification successful: Correct NVMe driver is attached.")
                        else:
                            print(f"Driver verification failed: Expected '{expected_driver}', but found '{actual_driver}'.")
                        break  # Exit the inner loop once we've found the driver information

                if actual_driver is None:
                    print("Driver information not found for the NVMe controller.")
                break  # Exit the outer loop once we've found the NVMe controller

        if not nvme_device_found:
            print("No NVMe controller found.")

        if nvme_device_found and not driver_found:
            print("Driver verification failed: No matching driver found for NVMe controller.")

    except subprocess.CalledProcessError as e:
        print(f"Error executing lspci: {e}")

# Example usage:
if __name__ == "__main__":
    expected_nvme_driver = "nvme"  # Expected NVMe driver
    verify_nvme_driver(expected_nvme_driver)
