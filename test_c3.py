import subprocess


def list_nvme_namespaces(nvme_device):
    try:
        # List NVMe namespaces
        result = subprocess.run(['sudo', 'nvme', 'list-ns', nvme_device], capture_output=True, text=True, check=True)
        print("Namespaces for NVMe device:\n")
        print(result.stdout)
        return result.stdout  # Return the output for testing purposes
    except subprocess.CalledProcessError as e:
        print(f"Error listing namespaces: {e}")
        return None


def test_list_nvme_namespaces():
    nvme_device = '/dev/nvme0'  # Change if necessary
    namespaces_output = list_nvme_namespaces(nvme_device)

    # Check if the namespaces are listed
    assert namespaces_output is not None, "Error: No output returned from 'list-ns' command"


if __name__ == "__main__":
    test_list_nvme_namespaces()
