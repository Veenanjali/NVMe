import subprocess

def list_nvme_namespaces(nvme_device):
    try:
        # List NVMe namespaces
        result = subprocess.run(['sudo', 'nvme', 'list-ns', nvme_device], capture_output=True, text=True, check=True)
        print("Namespaces for NVMe device:\n")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error listing namespaces: {e}")
        return False

def main():
    nvme_device = '/dev/nvme0'  # Change if necessary
    list_nvme_namespaces(nvme_device)

if __name__ == "__main__":
    main()
